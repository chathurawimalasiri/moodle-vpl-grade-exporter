import requests
from bs4 import BeautifulSoup
import csv
import os
import re
from collections import defaultdict

# Credentials (use environment variables for security)
FEELS_USERNAME = os.getenv("FEELS_USERNAME", "")
FEELS_PASSWORD = os.getenv("FEELS_PASSWORD", "")

# List of VPL links
VPL_URLS = [
    "",
    "",
    "",
    "",
]

# Login URL
LOGIN_URL = "https://feels.pdn.ac.lk/login/index.php"

# Output CSV file
OUTPUT_CSV = "filtered_ids.csv"

# Session to maintain cookies
session = requests.Session()

def login_to_moodle():
    login_page = session.get(LOGIN_URL)
    soup = BeautifulSoup(login_page.text, "html.parser")
    login_token_tag = soup.find("input", {"name": "logintoken"})
    if not login_token_tag:
        raise Exception("Login token not found. Check login page structure.")
    login_token = login_token_tag["value"]

    payload = {
        "username": FEELS_USERNAME,
        "password": FEELS_PASSWORD,
        "logintoken": login_token,
    }
    
    response = session.post(LOGIN_URL, data=payload)
    if "Dashboard" in response.text:
        print("Login successful!")
    else:
        raise Exception("Login failed. Check your credentials.")

def scrape_grades(vpl_url):
    response = session.get(vpl_url)
    if response.status_code != 200:
        raise Exception(f"Failed to access {vpl_url}")

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "generaltable"})
    if not table:
        raise Exception(f"No grades table found on {vpl_url}")

    headers = [th.text.strip().replace("\u00a0", " ") for th in table.find("thead").find_all("th")]
    
    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cells = [td.text.strip() for td in tr.find_all("td")]
        if cells:
            rows.append(cells)

    return headers, rows

def extract_id(full_name):
    """ Extracts the ID part (e.g., E/20/030) from the full name. """
    match = re.match(r'^E/\d+/\d+', full_name)
    return match.group() if match else None  # Return None if no match is found

def consolidate_marks():
    student_marks = defaultdict(lambda: [0] * len(VPL_URLS))  
    all_students = set()  

    for i, vpl_url in enumerate(VPL_URLS):
        headers, rows = scrape_grades(vpl_url)
        
        name_index = 2  # Assuming "First name" is at index 2
        grade_index = 5  # Assuming "Grade" is at index 5
        
        for row in rows:
            if len(row) <= max(name_index, grade_index):
                continue

            full_name = row[name_index]  
            student_id = extract_id(full_name)  # Extract ID from the full name
            
            if student_id:
                try:
                    grade = float(row[grade_index].split("/")[0].strip())  
                except ValueError:
                    grade = 0  

                student_marks[student_id][i] = grade  
                all_students.add(student_id)  

    return sorted(all_students), student_marks

def save_to_csv(student_list, student_marks):
    """ Saves filtered student IDs with grades into a CSV file. """
    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        header = ["Student ID"] + [f"Task {i+1}" for i in range(len(VPL_URLS))] + ["Total"]
        writer.writerow(header)
        
        for student in sorted(student_list):
            scores = student_marks[student]
            total = sum(scores)
            writer.writerow([student] + scores + [total])
    
    print(f"Filtered IDs saved to {OUTPUT_CSV}")

def main():
    try:
        login_to_moodle()
        student_list, student_marks = consolidate_marks()
        save_to_csv(student_list, student_marks)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
