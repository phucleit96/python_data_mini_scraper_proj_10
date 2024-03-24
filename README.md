# Web Scraper for Tour Information

This project is a Python script that scrapes a webpage for tour information, extracts the relevant data, checks if the data already exists in a SQLite database, and if not, stores the new data in the database and sends an email notification.

## How it works

The script works in the following steps:

1. It sends a GET request to the specified URL to scrape the webpage.
2. It extracts the tour information from the HTML content of the webpage using a YAML file that specifies the data to be extracted.
3. It checks if the extracted data already exists in the SQLite database.
4. If the data does not exist in the database, it stores the new data in the database and sends an email notification with the details of the new event.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have the following Python libraries installed:

- ssl
- time
- requests
- selectorlib
- os
- smtplib
- sqlite3

### Built With
* Python - The programming language used
* requests - Used to send HTTP requests
* selectorlib - Used to extract data from the HTML content
* sqlite3 - Used to interact with the SQLite database
* smtplib - Used to send emails

You can install these using pip:

```bash
pip install requests selectorlib sqlite3