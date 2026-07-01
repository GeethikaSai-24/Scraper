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
            
           # company name sits between title and location in the h2 text
            # structure: "New\nTitle\n\t\t    Company\n"
            parts = [p.strip() for p in card.text.split("\n") if p.strip()]
            # parts[0] = "New" (badge) or title
            # parts[1] = title (if New exists) or company
            # parts[-1] = company name
            # Filter out "New" badge and get second-to-last clean part
            clean_parts = [p for p in parts if p.lower() != "new" and p.strip()]
            company = clean_parts[1] if len(clean_parts) > 1 else "Unknown"
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
        print(f"    Location  : {job['location']}")
        print(f"    Posted  : {job['posted']}")
        print()

def filter_ai_jobs(jobs):
    """
    Filters jobs to show only AI/ML/Data related roles.
    """
    ai_keywords = [
        "ai", "ml", "machine learning", "data", "nlp",
        "deep learning", "neural", "llm", "python", "scientist"
    ]
    
    filtered = []
    for job in jobs:
        title_lower = job["title"].lower()
        if any(keyword in title_lower for keyword in ai_keywords):
            filtered.append(job)
    
    return filtered


def save_report(jobs, keyword):
    """
    Saves a human-readable text report of jobs found.
    """
    filename = f"report_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    
    with open(filename, "w") as f:
        f.write(f"Job Search Report — {keyword}\n")
        f.write(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}\n")
        f.write(f"Total jobs found: {len(jobs)}\n")
        f.write("=" * 60 + "\n\n")
        
        for i, job in enumerate(jobs, 1):
            f.write(f"[{i}] {job['title']}\n")
            f.write(f"    Company  : {job['company']}\n")
            f.write(f"    Location : {job['location']}\n")
            f.write(f"    Posted   : {job['posted']}\n")
            f.write("\n")
    
    print(f"✓ Report saved to {filename}")
    return filename

# ── Main flow ──
keyword = "Python"
print(f"Searching jobs for: {keyword}\n")

html = get_jobs(keyword)
all_jobs = parse_jobs(html)

print(f"\nTotal jobs scraped: {len(all_jobs)}")

ai_jobs = filter_ai_jobs(all_jobs)
print(f"AI/ML related jobs: {len(ai_jobs)}\n")

if ai_jobs:
    display_jobs(ai_jobs)
    save_jobs(ai_jobs, keyword)
    save_report(ai_jobs, keyword)
else:
    print("No AI/ML jobs found in current listings.")
    if all_jobs:
        print("Showing all jobs instead:\n")
        display_jobs(all_jobs)
        save_jobs(all_jobs, keyword)
        save_report(all_jobs, keyword)