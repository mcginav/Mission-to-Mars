from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

@app.route("/scrape")

def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return  "Scraping Successful!"

if __name__ == "__main__":
   app.run()

# def featured_image(browser):
#     # Visit URL
#     try:
#         PREFIX = "https://web.archive.org/web/20181114023740"
#         url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#         browser.visit(url)
#         article = browser.find_by_tag('article').first['style']
#         article_background = article.split("_/")[1].replace('");',"")
#         return f'{PREFIX}_if/{article_background}'
#     except:
#         return 'https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia22486-main.jpg'
# def featured_image(browser):
#     # Visit URL
#     url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
#     browser.visit(url)

#     # Find and click the full image button
#     full_image_elem = browser.find_by_tag('button')[1]
#     full_image_elem.click()

#     # Parse the resulting html with soup
#     html = browser.html
#     img_soup = soup(html, 'html.parser')

#     # Add try/except for error handling
#     try:
#         # Find the relative image url
#         img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

#     except AttributeError:
#         return None

#     # Use the base url to create an absolute url
#     img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

#     return img_url

# def mars_facts():
#     # Add try/except for error handling
#     try:
#         # Use 'read_html' to scrape the facts table into a dataframe
#         df = pd.read_html('http://space-facts.com/mars/')[0]

#     except BaseException:
#         return None

#     # Assign columns and set index of dataframe
#     df.columns=['Description', 'Mars']
#     df.set_index('Description', inplace=True)

#     # Convert dataframe into HTML format, add bootstrap
#     return df.to_html()