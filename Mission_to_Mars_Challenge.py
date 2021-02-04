#!/usr/bin/env python
# coding: utf-8

# In[7]:


#Import Splinter, Beautiful Soup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[8]:


executable_path = {'executable_path': 'C:\\Users\\mcgin\\Class\\Mission-to-Mars\\chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


#  ### Visit the NASA Mars News Site

# In[17]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[18]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[19]:


slide_elem.find("div", class_='content_title')


# In[20]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[21]:


# Use the parent element to find the teaser body
teaser_body = slide_elem.find("div", class_='article_teaser_body').get_text()
teaser_body


# ### JPL Space Images Featured Image

# In[23]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[24]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[25]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[26]:


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

# In[27]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[28]:


df.to_html()


# ### Mars Weather

# In[29]:


#Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[30]:


# Parse the data 
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[31]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[43]:


#1. Use browser to visit the URL
PREFIX = "https://web.archive.org/web/20181114023740"
url = f'{PREFIX}/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[35]:


#2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# In[36]:


#3. Write code to retrieve the image urls and titles for each hemisphere.
# Cerberus
browser.visit(url)
browser.links.find_by_partial_text('Cerberus').click()
html = browser.html
cerberus_soup = soup(html, 'html.parser')
cerberus_url = cerberus_soup.select_one('div.downloads a').get("href")
cerberus_title = cerberus_soup.select_one('div.content h2').text

# dictionary
cerberus_dict = {
    "img_url": cerberus_url,
    "title": cerberus_title
}

hemisphere_image_urls.append(cerberus_dict)


# In[37]:


# Schiaparelli
browser.visit(url)
browser.links.find_by_partial_text('Schiaparelli').click()
html = browser.html
schiaparelli_soup = soup(html, 'html.parser')
schiaparelli_url = schiaparelli_soup.select_one('div.downloads a').get("href")
schiaparelli_title = schiaparelli_soup.select_one('div.content h2').text

# dictionary
schiaparelli_dict = {
    "img_url": schiaparelli_url,
    "title": schiaparelli_title
}

hemisphere_image_urls.append(schiaparelli_dict)


# In[38]:


# Syrtis
browser.visit(url)
browser.links.find_by_partial_text('Syrtis').click()
html = browser.html
syrtis_soup = soup(html, 'html.parser')
syrtis_url = syrtis_soup.select_one('div.downloads a').get("href")
syrtis_title = syrtis_soup.select_one('div.content h2').text

# dictionary
syrtis_dict = {
    "img_url": syrtis_url,
    "title": syrtis_title
}

hemisphere_image_urls.append(syrtis_dict)


# In[39]:


# Valles
browser.visit(url)
browser.links.find_by_partial_text('Valles').click()
html = browser.html
valles_soup = soup(html, 'html.parser')
valles_url = valles_soup.select_one('div.downloads a').get("href")
valles_title = valles_soup.select_one('div.content h2').text

# dictionary
valles_dict = {
    "img_url": valles_url,
    "title": valles_title
}

hemisphere_image_urls.append(valles_dict)


# In[40]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[41]:


#5. Quit the browser
browser.quit()

