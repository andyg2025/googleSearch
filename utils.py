import requests
import os
from dotenv import load_dotenv
import re
import json
from models import Job

def extract_time(item) -> str:
    time_pattern = re.compile(r"\b(\d+\s*(?:hours|days|weeks|months|years) ago)\b", re.IGNORECASE)
    match = time_pattern.search(item.get("htmlSnippet", ""))
    return match.group(1) if match else ""

def get_jobs():
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    CX_ID = os.getenv("CX_ID")

    jobs = []
    
    keywords = 'site:linkedin.com/jobs/view ("Software Engineer" | "Backend Developer") "Ireland"'
    
    params = {
        "q": keywords,
        "key": API_KEY,
        "cx": CX_ID,
        "dateRestrict": "d1",
    }

    items = []
    start_index = 1
    while True:
        params["start"] = start_index
        response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
        data = response.json()
        if not data.get("items", []):
            break
        else:
            start_index += 10
            items += data.get("items", [])

    for item in items:
        job = Job()
        job.name = item.get("title", "")
        job.url = item.get("link", "")
        job.keywords = keywords
        job.time = extract_time(item)
        job.status = "new"
        jobs.append(job)
    
    return jobs

# def get_jobs():
#     return [
#         Job(
#             name="Software Engineer",
#             url="https://www.linkedin.com/jobs/view/123456",
#             keywords="site:linkedin.com/jobs/view ('Software Engineer' | 'Backend Developer') 'Ireland'",
#             time="2 days ago",
#             status="new"
#         ),
#         Job(
#             name="Backend Developer",
#             url="https://www.linkedin.com/jobs/view/789012",
#             keywords="site:linkedin.com/jobs/view ('Software Engineer' | 'Backend Developer') 'Ireland'",
#             time="5 hours ago",
#             status="new"
#         )
#     ]

def update_jobs(db):

    jobs = get_jobs() 

    for job in jobs:
        db.add(job)

    db.commit()
    return {"message": "{} jobs updated".format(len(jobs))}
        