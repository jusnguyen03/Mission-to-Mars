# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver.exe'}
#browser = Browser('chrome', **executable_path, headless=False)

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": featured_image(browser),
    "facts": mars_facts(),
    "cerberus": cerberus(browser),
    "schiaparelli": schiaparelli(browser),
    "syrtis": syrtis(browser),
    "valles": valles(browser),
    "last_modified": dt.datetime.now()
    }
    return data

# Visit the NASA mars news site
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first 'a' tag and save it as 'new_title'
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    return news_title, news_p

def featured_image(browser):
    # Featured Images

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None
    
    return "https://www.jpl.nasa.gov/"+ img_url_rel

def mars_facts():
    #Add try/exept for error handling
    try:
        #Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars']
    df.set_index('description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return(df.to_html())

# Challenge
# Fuction for Cerberus Hemisphere
def cerberus(browser):
    try:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        cerb_image = browser.find_by_text('Cerberus Hemisphere Enhanced', wait_time=1)
        cerb_image.click()
        html = browser.html
        imagesoup = BeautifulSoup(html, 'html.parser')
        cerbsoup = BeautifulSoup(html, 'html.parser')
        # Find the title
        cerberus_title = cerbsoup.find("h2", class_='title').get_text()
        cerberusSam = browser.links.find_by_partial_text('Sample')
        cerberusSam.click()
        # Find the relative image url
        cerb_url_rel = imagesoup.select_one('img.wide-image').get('src')
        # Use the base URL to create an absolute URL
        cerb_img_url = f'https://astrogeology.usgs.gov{cerb_url_rel}'
        return(cerb_img_url, cerberus_title)
    except AttributeError:
        return None, None
# Fuction for Schiaparelli Hemisphere
def schiaparelli(browser):
    try:
        # Visit schiaparelli URL
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        schiap_image = browser.find_by_text('Schiaparelli Hemisphere Enhanced')
        schiap_image.click()
        # Parse the resulting html with soup
        html = browser.html
        imagesoup = BeautifulSoup(html, 'html.parser')
        schiapsoup = BeautifulSoup(html, 'html.parser')
        # Find the title
        schiap_title = schiapsoup.find("h2", class_='title').get_text()
        schiaparelli = browser.links.find_by_partial_text('Sample')
        schiaparelli.click()
        # Find the relative image url
        schiap_url_rel = imagesoup.select_one('img.wide-image').get('src')
        schiap_img_url = f'https://astrogeology.usgs.gov{schiap_url_rel}'
        return(schiap_img_url, schiap_title)
    except AttributeError:
        return None, None
# Fuction for Syrtis Major Hemisphere
def syrtis(browser):
    try:
        # Visit Syrtis major URL
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        # Find and click the Schiaparelli image button
        syrtis_image = browser.find_by_text('Syrtis Major Hemisphere Enhanced')
        syrtis_image.click()
        # Parse the resulting html with soup
        html = browser.html
        image_soup = BeautifulSoup(html, 'html.parser')
        syrtissoup = BeautifulSoup(html, 'html.parser')
        # Find the title
        syrtis_title = syrtissoup.find("h2", class_='title').get_text()
        syrtis = browser.links.find_by_partial_text('Sample')
        syrtis.click()
        # Find the relative image url
        syrtis_url_rel = image_soup.select_one('img.wide-image').get('src')
        syrtis_img_url = f'https://astrogeology.usgs.gov{syrtis_url_rel}'
        return(syrtis_img_url, syrtis_title)
    except AttributeError:
        return None, None
def valles(browser):
    try:
        # Visit Valles Marineris URL
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        # Find and click the Schiaparelli image button
        valles_image = browser.find_by_text('Valles Marineris Hemisphere Enhanced')
        valles_image.click()
        # Parse the resulting html with soup
        html = browser.html
        image_soup = BeautifulSoup(html, 'html.parser')
        vallessoup = BeautifulSoup(html, 'html.parser')
        # Find title
        valles_title = vallessoup.find("h2", class_='title').get_text()
        valles = browser.links.find_by_partial_text('Sample')
        valles.click()
        # Find the relative image url
        valles_url_rel = image_soup.select_one('img.wide-image').get('src')
        valles_img_url = f'https://astrogeology.usgs.gov{valles_url_rel}'
        return(valles_img_url, valles_title)
    except AttributeError:
        return None, None

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
