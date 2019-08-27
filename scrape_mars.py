# Declare Dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests

# Choose the executable path to driver 
browser = Browser('chrome')


# Visit Nasa news url through splinter module
browser.visit('https://mars.nasa.gov/news/')

# HTML Object
html = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Retrieve the news title and news_paragraph
news_title = soup.find('div', class_='content_title').find('a').text
news_p = soup.find('div', class_='image_and_description_container').find('a').text


# Display scrapped data 
print(news_title)
print(news_p)

# Visit Mars Space Images through splinter module
image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(image_url_featured)

# HTML Object 
html_image = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html_image, 'html.parser')

# Retrieve background-image url from style tag 
featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

# Website Url 
main_url = 'https://www.jpl.nasa.gov'

# Concatenate website url with scrapped route
featured_image_url = main_url + featured_image_url

# Display full link to featured image
featured_image_url

# Visit Mars Weather Twitter through splinter module
weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weather_url)

# HTML Object 
html_weather = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html_weather, 'html.parser')

# Find all elements that contain tweets
latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

# Retrieve all elements that contain news title in the specified range
# Look for entries that display weather related words to exclude non weather related tweets 
for tweet in latest_tweets: 
    weather_tweet = tweet.find('p').text
    if 'Sol' and 'pressure' in weather_tweet:
        print(weather_tweet)
        break
    else: 
        pass

# Visit Mars facts url 
facts_url = 'http://space-facts.com/mars/'

# Use Panda's `read_html` to parse the url
mars_facts = pd.read_html(facts_url)

# Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
mars_df = mars_facts[1]

# Assign the columns `['Description', 'Value']`
mars_df.columns = ['Description','Mars_Profile']

# Set the index to the `Description` column without row indexing
mars_df.set_index('Description', inplace=True)

# Save html code to folder Assets
mars_df.to_html()

data = mars_df.to_dict(orient='records')  # Here's our added param..

# Display mars_df
mars_df

# Visit hemispheres website through splinter module 
hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemispheres_url)

# HTML Object
html_hemispheres = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html_hemispheres, 'html.parser')

# Retreive all items that contain mars hemispheres information
items = soup.find_all('div', class_='item')

# Create empty list for hemisphere urls 
hemisphere_image_urls = []

# Store the main_ul 
hemispheres_main_url = 'https://astrogeology.usgs.gov'

# Loop through the items previously stored
for i in items: 
    # Store title
    title = i.find('h3').text

    # Store link that leads to full image website
    partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
    browser.visit(hemispheres_main_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
    partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
    soup = BeautifulSoup( partial_img_html, 'html.parser')
    
    # Retrieve full image source 
    img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    

# Display hemisphere_image_urls
hemisphere_image_urls