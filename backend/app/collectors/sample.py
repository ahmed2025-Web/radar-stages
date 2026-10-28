"""Collecteur de démo — offres réelles collectées sur LinkedIn (28 oct. 2026).

Permet à l'app de tourner et d'afficher des données sans scraper. Les vrais
collecteurs (linkedin, wttj, jobteaser) remplaceront progressivement cette source.
"""
from __future__ import annotations

from ..models import Offer
from .base import linkedin_search_url

# (company, title, location, country, remote, posted, salary, tags, apply_mode, applied, url)
_RAW = [
    ("Natixis CIB", "Stage 6 mois – Développeur Full Stack & IA – Support Applicatif", "Paris · Sur site", "France", False, "il y a 3 semaines", None, ["Full-Stack", "IA", "Dev"], "site", False, None),
    ("MaiaSpace", "Stage – Software Crafter 3.0 (DevOps + AI)", "Paris · Sur site", "France", False, "il y a 2 semaines", None, ["Software", "DevOps", "IA"], "site", False, None),
    ("Thales", "Stage – Ingénieur IA Générative et Développement Logiciel", "Paris", "France", False, "récent", None, ["GenAI", "Dev"], "site", False, "https://www.linkedin.com/jobs/view/4480356907/"),
    ("Dassault Systèmes", "Stage – Ingénieur.e IA – Assistants et Plateforme Agentique", "Paris · Sur site", "France", False, "il y a 2 semaines", None, ["IA", "Agents", "LLM"], "site", False, None),
    ("Dassault Systèmes", "Stage – Ingénieur Développement IA – Agent IA 3DVIA", "Paris · Sur site", "France", False, "il y a 1 semaine", None, ["IA", "Agents", "Dev"], "site", False, "https://www.linkedin.com/jobs/view/4482138321/"),
    ("Wiremind", "Software Engineer (H/F) – Stage", "Paris · Hybride", "France", True, "récent", None, ["Software", "Dev"], "site", False, None),
    ("Dokhan Luxury Hotels", "Développeur(se) Outils IA & Data (H/F)", "Paris · Sur site", "France", False, "récent", None, ["Dev", "IA", "Data"], "mail", True, None),
    ("Silae", "Stage de fin d'études – Ingénieur IA / LLM", "Paris", "France", False, "il y a 1 semaine", None, ["IA", "LLM"], "site", False, None),
    ("Equancy | Groupe EDG", "Stage AI Engineer – IA générative & agentique – 6 mois", "Paris · Hybride", "France", True, "il y a 3 semaines", "1 500 €/mois", ["GenAI", "Agents"], "easy_apply", False, None),
    ("Artefact", "Stage Software Engineer", "Paris", "France", False, "récent", None, ["Software", "Dev"], "site", False, None),
    ("Wavestone", "Stage fin d'études – Consultant·e Agentic & GenAI Engineer", "Paris · Hybride", "France", True, "il y a 1 mois", "1 800–2 000 €/mois", ["GenAI", "Agents", "Conseil"], "site", False, None),
    ("Louis Vuitton", "Stage – Assistant.e AI / GenAI Engineer", "Paris · Sur site", "France", False, "il y a 6 jours", None, ["GenAI", "IA"], "site", False, None),
    ("Novartis", "Stage – AI Solutions & Automation Engineer", "Paris", "France", False, "il y a 4 jours", None, ["IA", "Automatisation"], "site", False, None),
    ("Xpollens", "Stage – AI Engineer", "Paris · Sur site", "France", False, "il y a 1 semaine", None, ["IA"], "site", False, None),
    ("Kering", "Stage Ingénieur Automatisation IT4IT & AIOps", "Paris · Sur site", "France", False, "récent", None, ["DevOps", "AIOps", "Automatisation"], "site", True, None),
    ("ODDO BHF", "AI Engineer Intern", "Paris · Hybride", "France", True, "il y a 1 semaine", None, ["IA"], "site", False, None),
    ("BPCE Solutions informatiques", "Stage – Développeur Solutions Technologiques du SI", "Paris · Sur site", "France", False, "il y a 1 semaine", None, ["Dev", "SI"], "site", False, None),
    ("Valtech", "FR – Stage Intelligence Artificielle (Talent Program)", "Paris · Hybride", "France", True, "il y a 2 semaines", None, ["IA"], "site", False, None),
    ("Sharp DX France", "Développeur Junior – Stage Fin d'études (H/F)", "Paris · Hybride", "France", True, "récent", None, ["Dev"], "site", False, None),
    ("Lazard", "Stage – Ingénieur IA Multi-Équipes", "Paris", "France", False, "récent", None, ["IA"], "site", False, None),
    ("Colombus Consulting", "Ingénieur.e IA – Stage", "Paris", "France", False, "il y a 2 semaines", None, ["IA", "Conseil"], "site", False, None),
    ("Wiremind", "AI Product Owner (M/F) – Internship", "Paris · Hybride", "France", True, "il y a 2 semaines", None, ["IA", "Product"], "site", False, None),
    ("Danone", "Stage – Data, IA & Automatisation – Janvier 2027", "Paris", "France", False, "il y a 6 jours", None, ["Data", "IA"], "site", False, None),
    ("AXA", "Stage – M365 Power Platform, Data & AI", "Paris", "France", False, "il y a 6 jours", None, ["Low-code", "Data"], "site", False, None),
]


def collect() -> list[Offer]:
    offers = []
    for (company, title, location, country, remote, posted, salary, tags, mode, applied, url) in _RAW:
        offers.append(
            Offer(
                company=company,
                title=title,
                url=url or linkedin_search_url(title, company),
                source="sample",
                location=location,
                country=country,
                remote=remote,
                posted=posted,
                salary=salary,
                tags=tags,
                apply_mode=mode,
                applied=applied,
            )
        )
    return offers
