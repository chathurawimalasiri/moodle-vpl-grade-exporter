# Moodle VPL Grade Exporter & Student Grades Collector

This contains two Python scripts to **automate grade extraction from Moodle’s Virtual Programming Lab (VPL)** and **consolidate student grades** across multiple assignments.

## Features (moodle-vpl-grade-exporter.py)

- Logs into Moodle using provided credentials.
- Scrapes the VPL submissions table for grades.
- Exports the grades and relevant details to a CSV file.

## Features (student_grades_collector.py)
- Connects to multiple Virtual Programming Lab (VPL) URLs.
- Extracts student names and grades from Moodle tables.
- Identifies students across different assignments.
- Maps grades to each student based on their name.
- Handles missing grades (defaults to 0 for empty values).
- Aggregates grades across assignments for a total score.
- Exports final grades to a CSV file.

## Prerequisites

- Python 3.7 or 3.7+.
- The following Python libraries:
  - `requests`
  - `beautifulsoup4`
