# Moodle VPL Grade Exporter

This is a Python script to automate the process of downloading grades from a Moodle VPL submissions page and exporting them to a CSV file.

## Features

- Logs into Moodle using provided credentials.
- Scrapes the VPL submissions table for grades.
- Exports the grades and relevant details to a CSV file.

## Prerequisites

- Python 3.7 or 3.7+.
- The following Python libraries:
  - `requests`
  - `beautifulsoup4`

Install the required libraries using:
```bash
pip install -r requirements.txt
