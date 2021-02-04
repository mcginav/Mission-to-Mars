#!/usr/bin/env python
# coding: utf-8

# In[1]:



#Import Splinter, Beautiful Soup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt




def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': 'C:\\Users\\mcgin\\Class\\Mission-to-Mars\\chromedriver'}
    browser = Browser('chrome', executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_image_urls(browser)
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    try:
        PREFIX = "https://web.archive.org/web/20181114023740"
        url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        article = browser.find_by_tag('article').first['style']
        article_background = article.split("_/")[1].replace('");',"")
        return f'{PREFIX}_if/{article_background}'
    except:
        return 'https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia22486-main.jpg'
 

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")



# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres



def hemispheres_image_urls(browser):
    #1. Use browser to visit the URL    
    try:
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        html = browser.html
        html = soup(html, 'html.parser')
    
        #2. Create a list to hold the images and titles.
        hemispheres_image_urls = []
        img_elem = browser.find_by_tag("h3")
    
        links=browser.find_by_css("a.product-item h3")
        for i in range(len(img_elem)):
            hemispheres={}
            browser.find_by_tag("h3")[i].click()
            img_link=browser.links.find_by_text('Sample')[0]
            hemispheres['img_url']=img_link['href']
            hemispheres['title']=browser.find_by_css("h2.title").text
            hemispheres_image_urls.append(hemispheres)
            browser.back()
        # 4. Print the list that holds the dictionary of each image url and title.
        return hemispheres_image_urls
    
    except BaseException:
        return None
            
       
    

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())






