#!/usr/bin/env python
# coding: utf-8

#Import Splinter, Beautiful Soup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


executable_path = {'executable_path': 'C:\\Users\\mcgin\\Class\\Mission-to-Mars\\chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


#  ### Visit the NASA Mars News Site


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


slide_elem.find("div", class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# Use the parent element to find the teaser body
teaser_body = slide_elem.find("div", class_='article_teaser_body').get_text()
teaser_body


# ### JPL Space Images Featured Image


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)



# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()



# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')



#Visit Archived JPL URL    
try:
    PREFIX = "https://web.archive.org/web/20181114023740"
    url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    article = browser.find_by_tag('article').first['style']
    article_background = article.split("_/")[1].replace('");',"")
    print (f'{PREFIX}_if/{article_background}')
except:
    print('https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia22486-main.jpg')


# ### Mars Facts


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df



df.to_html()


# ### Mars Weather


#Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)



# Parse the data 
html = browser.html
weather_soup = soup(html, 'html.parser')



# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres


#1. Use browser to visit the URL
url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)



#2. Create a list to hold the images and titles.
hemisphere_image_urls = []




links=browser.find_by_css("a.product-item h3")
for i in range(len(links)):
    hemisphere={}
    browser.find_by_css("a.product-item h3")[i].click()
    sample_elem=browser.links.find_by_text('Sample').first
    hemisphere['img_url']=sample_elem['href']
    hemisphere['title']=browser.find_by_css("h2.title").text
    hemisphere_image_urls.append(hemisphere)
    browser.back()
    



# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls



#5. Quit the browser
browser.quit()





