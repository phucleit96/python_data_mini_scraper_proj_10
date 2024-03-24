# Import necessary libraries
import ssl
import time
import requests
import selectorlib
import os
import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# URL to scrape
URL = "https://programmer100.pythonanywhere.com/tours/"

# Establish a connection to the SQLite database
connections = sqlite3.connect('data.db')

# Function to scrape the webpage
def scrape(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Get the HTML content of the page
    source = response.text
    return source

# Function to extract data from the scraped webpage
def extract(source):
    # Create an Extractor from the YAML file
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    # Extract the data
    value = extractor.extract(source)['tours']
    return value

# Function to send an email
def send_email(subject, message_body):
    host = 'smtp.gmail.com'
    port = 465

    username = 'badboy27796@gmail.com'
    password = os.getenv('PASSWORD')

    receiver = 'phuc.le.it96@gmail.com'
    context = ssl.create_default_context()

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = receiver
    msg['Subject'] = subject

    # Attach the message body to the email
    msg.attach(MIMEText(message_body, 'plain'))

    with smtplib.SMTP_SSL(host, port) as server:
        server.login(username, password)
        server.sendmail(username, receiver, msg.as_string())

# Function to store the extracted data into the database
def store(extracted):
    # Split the extracted data into individual items
    row = extracted.split(",")
    # Remove leading and trailing whitespaces from each item
    row = [item.strip() for item in row]
    # Get a cursor object
    cursor = connections.cursor()
    # Execute the SQL query to insert the data into the database
    cursor.execute("INSERT INTO events VALUES (?, ?, ?)", row)
    # Commit the changes
    connections.commit()

# Function to read the data from the database
def read(extracted):
    # Split the extracted data into individual items
    row = extracted.split(",")
    # Remove leading and trailing whitespaces from each item
    row = [item.strip() for item in row]
    # Unpack the row into individual variables
    band, city, date = row
    # Get a cursor object
    cursor = connections.cursor()
    # Execute the SQL query to select the data from the database
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    # Fetch all the rows
    rows = cursor.fetchall()
    # Print the rows
    print(rows)
    return rows

# Main function
if __name__ == "__main__":
    # Infinite loop
    while True:
        # Scrape the webpage
        scraped = scrape(URL)
        # Extract the data
        extracted = extract(scraped)

        # If there are upcoming tours
        if extracted != "No upcoming tours":
            # Read the data from the database
            row = read(extracted)
            # If the row does not exist in the database
            if not row:
                store(extracted)
                send_email("New Event Found", f"Hey, a new event was found: {extracted}")
        # Wait for 3 seconds before the next iteration
        time.sleep(2)