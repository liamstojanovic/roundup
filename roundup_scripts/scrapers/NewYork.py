# The purpose of this script is to scrape metadata from the most recent New York Fed working papers. This script uses
# the New York Fed "Staff Reports" landing page and also clicks on individual links to procure XX and YY. 
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 1 Aug 2023

import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Function to check if a URL exists by checking the HTTP status code
def url_exists(url):
    response = requests.get(url)
    return response.status_code == 200

# Function to create a url list based on date conditions. It takes before and after as arguments, which are strings
# that specify the URL structure before and after the year appears. For example, in 
# "https://www.newyorkfed.org/research/staff_reports/index.html#2023"
# the before_string is "https://www.newyorkfed.org/research/staff_reports/index.html#" and the after string is
# "" (empty).
# If the current date is in Jan or Feb, it contain's this year's and last year's url (after checking that this
# year's url does indeed exist - a non-trivial question if the code is being run on Jan 1 or 2, when people may
# still be on holiday and the webpage is not up yet. If the current date is in any month from March - December,
# then this function makes a list of one url for the current year.
def url_conditional(before, after):
    # Initialize an empty list for the URLs
    url = []

    # Get the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month

    # If the current month is January or February
    if current_month in [1, 2]:
        # Create a URL for the current year
        current_year_url = f"{before}{current_year}{after}"
        
        # If the URL exists, add it to the list
        if url_exists(current_year_url):
            url.append(current_year_url)
            
        # Create a URL for the previous year and add it to the list
        last_year_url = f"{before}{current_year - 1}{after}"
        url.append(last_year_url)

    # If the current month is not January or February
    else:
        # Add a URL for the current year to the list
        url.append(f"{before}{current_year}{after}")

    return(url)


url_list = url_conditional(before = "https://www.newyorkfed.org/research/staff_reports/index.html#", after = "")
from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()

# Your url_list logic goes here...
url_list = ["https://www.newyorkfed.org/research/staff_reports/index.html#2023"]

for url in url_list:
    print(url)

    # Send a GET request and render the JavaScript
    r = session.get(url)
    r.html.render(sleep=2, keep_page=True, scrolldown=1)

    # Then you can use BeautifulSoup as before to parse the page
    soup = BeautifulSoup(r.html.html, 'html.parser')
    elements = soup.select('tr > td > p')

    # Filter elements based on the presence of 'a' tag
    elements = [el for el in elements if el.select_one('a')]
    
    # Get titles, links, dates, and authors from the main website. Format them as a dictionary.
    data = {
        #'Title': [el.select('a').text.strip() for el in elements]
        #'Link': ["https://www.federalreserve.gov" + el.select_one('h5 > a')['href'] for el in elements],
        #'Number': [el.select_one('span.badge').text.strip().replace('FEDS ', '') for el in elements],
        #'Author': [el.select_one('div.authors').text.strip() for el in elements],
        #'Abstract': [el.select_one('div.collapse > p').text.strip().replace('Abstract: ', '') for el in elements],
        #'Date': [el.select_one('time')['datetime'] for el in elements]
    }
    Title = [el.select_one('a').text.strip() for el in elements]
    print(Title)
    Link = ["https://www.newyorkfed.org" + el.select_one('a')['href'] for el in elements]
    print(Link)
    Number = [el.select_one('a')['href'].split("/sr")[1].replace('.html', '') for el in elements]
    print(Number)
    Author = [list(el.stripped_strings)[1] for el in elements]
    print(Author)
    
    # Date is slightly more complicated, so I've moved it out of the list comprehension to show it more step-by-step.
    Date = []
    for el in elements:
        date_raw = el.select_one('span.paraNotes').get_text().split('\xa0')
        month = date_raw[1].strip()[4:]
        year = date_raw[2].strip()
        Date.append(month + " " + year)
    print(Date)
    
    # Abstracts need to visit a separate hyperlink to be scraped.
    Abstract = []
    for link in Link:
        response = requests.get(link)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Get the abstracts
        abstract = soup.select('div.ts-article-text')[1].text.strip().replace('\n', ' ')
        Abstract.append(abstract)
        
    print(Abstract)


