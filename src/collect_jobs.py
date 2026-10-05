import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

if not APP_ID or not APP_KEY:
    raise ValueError("ADZUNA_APP_ID and ADZUNA_APP_KEY must be set in the .env file.")

de_cities = [
    "Aachen",
    "Köln",
    "Düsseldorf",
    "Bonn",
    "Dortmund",
    "Essen"
]

nl_cities = [
    "Maastricht",
    "Heerlen",
    "Sittard",
    "Venlo",
    "Eindhoven"
]

tech_roles = [
    "Data Science",
    "Data Analyst",
    "Machine Learning",
    "Artificial Intelligence",
    "Software Engineering",
    "Backend",
    "DevOps",
    "Cloud",
    "Cybersecurity"
]

jobs = []

print("---")
print(f"Searching for jobs in {len(de_cities)} German cities for {len(tech_roles)} roles.")
print("---")

for city in de_cities:
    for role in tech_roles:

        print(f"Searching: {role} in {city}")

        url = "https://api.adzuna.com/v1/api/jobs/de/search/1"

        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": role,
            "where": city,
            "results_per_page": 50
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        de_data = response.json()

        for job in de_data.get("results", []):

            jobs.append({
                "search_role": role,
                "search_city": city,
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "description": job.get("description"),
                "created": job.get("created")
            })

print("---")
print(f"Searching for jobs in {len(nl_cities)} Dutch cities for {len(tech_roles)} roles.")
print("---")

for city in nl_cities:
    for role in tech_roles:

        print(f"Searching: {role} in {city}")

        url = "https://api.adzuna.com/v1/api/jobs/nl/search/1"

        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": role,
            "where": city,
            "results_per_page": 50
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        nl_data = response.json()

        for job in nl_data.get("results", []):

            jobs.append({
                "search_role": role,
                "search_city": city,
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "description": job.get("description"),
                "created": job.get("created")
            })

df = pd.DataFrame(jobs)
df.to_csv("data/raw/jobs_raw.csv", index=False)
print("---")
print(f"Saved {len(df)} unique job listings to data/raw/jobs_raw.csv")
print("---")
