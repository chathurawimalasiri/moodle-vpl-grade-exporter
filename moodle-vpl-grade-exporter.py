import requests
from bs4 import BeautifulSoup
import csv

# FEELS Usernama and Password
FEELS_USERNAME = "your_username"
FEELS_PASSWORD = "your_password"

# Go to VPL -> Submission List -> Copy and Paste Link
VPL_URL = "LINK"

# Login URL
LOGIN_URL = "https://feels.pdn.ac.lk/login/index.php"

# Output CSV file
OUTPUT_CSV = "grades.csv"

# Session to maintain cookies
session = requests.Session()

def login_to_moodle():

    login_page = session.get(LOGIN_URL)
    soup = BeautifulSoup(login_page.text, "html.parser")
    login_token = soup.find("input", {"name": "logintoken"})["value"]

    payload = {
        "username": FEELS_USERNAME,
        "password": FEELS_PASSWORD,
        "logintoken": login_token
    }

    response = session.post(LOGIN_URL, data=payload)
    if "Dashboard" in response.text:
        print("Login successful!")
    else:
        raise Exception("Login failed. Check your credentials.")

def scrape_grades():

    response = session.get(VPL_URL)
    if response.status_code != 200:
        raise Exception("Failed to access the VPL submissions page.")

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"class": "generaltable"})
    if not table:
        raise Exception("Unable to find the grades table on the page.")

    headers = [th.text.strip() for th in table.find("thead").find_all("th")]

    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cells = [td.text.strip() for td in tr.find_all("td")]
        rows.append(cells)

    return headers, rows

def save_to_csv(headers, rows):

    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Grades saved to {OUTPUT_CSV}")

def main():
    try:
        login_to_moodle()
        headers, rows = scrape_grades()
        save_to_csv(headers, rows)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
