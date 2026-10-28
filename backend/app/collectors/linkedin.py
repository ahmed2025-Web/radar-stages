"""Collecteur LinkedIn via l'API publique « guest » des offres.

Cette API renvoie les cartes d'offres en HTML sans authentification :
https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search

On reste respectueux : pagination limitée, un User-Agent explicite, et tolérance
aux erreurs (si LinkedIn bloque ou change son HTML, on renvoie ce qu'on a).
"""
from __future__ import annotations

import re
import time

import httpx
from bs4 import BeautifulSoup

from .. import config
from ..models import Offer
from ..tagging import infer_tags

# Id numérique LinkedIn en fin d'URL d'offre (…-4461575934 ou /view/4482138321/).
_JOB_ID = re.compile(r"(\d{6,})/?$")

GUEST_API = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    )
}
# f_JT=I : type d'emploi = stage (Internship)
_RESULTS_PER_PAGE = 10


def _job_id(url: str) -> str:
    match = _JOB_ID.search(url)
    return match.group(1) if match else ""


def parse_jobs(html: str) -> list[Offer]:
    """Extrait les offres d'une page de cartes LinkedIn. Pur (testable sans réseau)."""
    soup = BeautifulSoup(html, "html.parser")
    offers: list[Offer] = []
    for card in soup.select("li"):
        title_el = card.select_one("h3.base-search-card__title")
        link_el = card.select_one("a.base-card__full-link, a.base-search-card__link")
        if not title_el or not link_el or not link_el.get("href"):
            continue
        company_el = card.select_one("h4.base-search-card__subtitle")
        loc_el = card.select_one(".job-search-card__location")
        time_el = card.select_one("time")

        title = title_el.get_text(strip=True)
        url = link_el["href"].split("?")[0]
        offers.append(
            Offer(
                company=company_el.get_text(strip=True) if company_el else "",
                title=title,
                url=url,
                source="linkedin",
                external_id=_job_id(url),
                location=loc_el.get_text(strip=True) if loc_el else "",
                posted=time_el.get_text(strip=True) if time_el else "",
                tags=infer_tags(title),
                apply_mode="site",
            )
        )
    return offers


def _fetch_page(keywords: str, location: str, start: int) -> str:
    resp = httpx.get(
        GUEST_API,
        params={"keywords": keywords, "location": location, "f_JT": "I", "start": start},
        headers=_HEADERS,
        timeout=20,
    )
    resp.raise_for_status()
    return resp.text


def collect(pages: int = 1) -> list[Offer]:
    """Collecte les offres pour chaque mot-clé x lieu configurés. Dédoublonne par id."""
    found: dict[str, Offer] = {}
    for keyword in config.SEARCH_KEYWORDS:
        for location in config.SEARCH_LOCATIONS:
            for page in range(pages):
                try:
                    html = _fetch_page(keyword, location, start=page * _RESULTS_PER_PAGE)
                except httpx.HTTPError:
                    break  # source indisponible : on passe au couple suivant
                page_offers = parse_jobs(html)
                for offer in page_offers:
                    found[offer.id] = offer
                if not page_offers:
                    break
                time.sleep(1)  # courtoisie : on n'inonde pas LinkedIn
    return list(found.values())
