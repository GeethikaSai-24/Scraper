import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_jobs(keyword):
    """
    Scrapes Python job listings from Python.org job board.
    This site allows scraping and has no bot protection.
    """
    url = f"https://www.python.org/jobs/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"✓ Connected to python.org/jobs — status {response.status_code}")
        return response.text
    
    except requests.exceptions.ConnectionError:
        print("✗ No internet connection or site unreachable.")
        return None
    except requests.exceptions.Timeout:
        print("✗ Request timed out.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP error: {e}")
        return None

def parse_jobs(html):
    """
    Parses python.org/jobs listings.
    Jobs are inside <h2> tags within the job listing section.
    """
    if not html:
        return []
    
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    
    job_cards = soup.find_all("h2")
    
    for card in job_cards:
        try:
            # skip non-job h2s
            text = card.text.strip()
            if not text or "Get exploring" in text:
                continue
            
            # title and company are inside the h2
            link_tag = card.find("a")
            title = link_tag.text.strip() if link_tag else text
            
            # company is a <span> inside h2
            # get all text, split by newlines, clean each part
            parts = [p.strip() for p in card.text.split("\n") if p.strip()]
            # parts[0] = "New" or title, last part = company name
            company = parts[-1] if len(parts) > 1 else "Unknown"
            # location is a <span> sibling after h2
            location_tag = card.find_next("span", class_="listing-location")
            location = location_tag.text.strip() if location_tag else "Not listed"

            # posted date
            date_tag = card.find_next("time")
            posted = date_tag.text.strip() if date_tag else "Unknown"
            
            # skip if no real title found
            if title and company:
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "posted": posted
                })
        
        except AttributeError:
            continue
    
    return jobs[:10]

def save_jobs(jobs, keyword):
    """
    Saves job list to a JSON file with timestamp.
    """
    filename = f"jobs_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    
    with open(filename, "w") as f:
        json.dump(jobs, f, indent=4)
    
    print(f"✓ Saved {len(jobs)} jobs to {filename}")
    return filename

def display_jobs(jobs):
    """
    Prints a clean summary of jobs to terminal.
    """
    if not jobs:
        print("No jobs found.")
        return
    
    print(f"\n{'='*60}")
    print(f"  Found {len(jobs)} jobs")
    print(f"{'='*60}\n")
    
    for i, job in enumerate(jobs, 1):
        print(f"[{i}] {job['title']}")
        print(f"    Company : {job['company']}")
        print(f"    Skills  : {job['location']}")
        print(f"    Posted  : {job['posted']}")
        print()

# ── Main flow ──
keyword = "Python"
print(f"Searching jobs for: {keyword}\n")

html = get_jobs(keyword)
jobs = parse_jobs(html)
display_jobs(jobs)

if jobs:
    save_jobs(jobs, keyword)
else:
    print("Nothing to save.")