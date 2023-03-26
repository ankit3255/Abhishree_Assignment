import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import datetime

url = 'https://www.theverge.com/'

# Make a GET request to the URL and store the response
response = requests.get(url)
# print(response)

# Create a BeautifulSoup object from the response text
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the article elements on the page
articles = soup.find_all('article')
# print(articles)

# Define the current date in the format ddmmyyy
today = datetime.date.today().strftime('%d%m%Y')
# print(today)

# Define the name of the CSV file to write to
csv_filename = today + '_verge.csv'

# Define the name of the SQLite database to create
db_filename = today + '_verge.db'

# Open a connection to the database
conn = sqlite3.connect(db_filename)

# Create a cursor to execute SQL commands
c = conn.cursor()

# Create a table in the database to store the articles
c.execute('''CREATE TABLE articles
             (id INTEGER PRIMARY KEY,
              url TEXT,
              headline TEXT,
              author TEXT,
              date TEXT)''')

csvfile = open(csv_filename, 'w', newline='')

# Loop through each article and extract the information we want
for i, article in enumerate(articles):
    # Get the headline
    headline = article.find('h2').text.strip()
    
    # Get the link to the article
    link = article.find('a')['href']
    
    # Get the author
    author = article.find('span', {'class': 'c-byline__item'}).text.strip()
    
    # Get the date
    date = article.find('time')['datetime']
    
    # Write the article information to the CSV file
    writer = csv.writer(csvfile)
    writer.writerow([i, link, headline, author, date])
    csvfile.close()
    # Write the article information to the SQLite database
    c.execute("INSERT INTO articles VALUES (?, ?, ?, ?, ?)", (i, link, headline, author, date))

# Commit the changes to the database and close the connection
import os

print(os.path.abspath(csv_filename))
conn.commit()
conn.close()
