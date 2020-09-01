
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path':ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    #Mars News
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")

    news_title= soup.find_all('div',class_="content_title")[1].text
    
    news_p = soup.find_all('div',class_="rollover_description_inner")[1].string
    
    #mars_image
    url2= 'https://www.jpl.nasa.gov/'
    browser.visit(url2)
    time.sleep(5)
    mars_html=browser.html
    soup2=bs(mars_html,'html.parser')

    featured_image_url  = soup2.find_all('img')[3]["src"]
    print(featured_image_url)
    #mars facts
    url_facts = "https://space-facts.com/mars/"
    facts = pd.read_html(url_facts)
    new_table=facts[0]
    final_table=new_table.rename(columns={0: "Description", 1:"Mars"})
    html_table=final_table.to_html("table.html")

    #mars hemisphere
    url_hemi = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    browser.visit(url_hemi)
    time.sleep(5)
    html_astro=browser.html
    soup3=bs(html_astro,'html.parser')

    titles = []
    
    for title in titles:
      titles.append(title.h3.text)
    
    hemisphere_image_urls = []

    for title in titles:
        img_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
        browser.visit(img_url)
        time.sleep(5)
        browser.click_link_by_partial_text(title)
        html4=browser.html
        soup3=bs(html4,"html.parser")
        img_url_hemi=soup3.find_all("li")[0].a["href"]
        img_dict = {"title":title, "img_url":img_url_hemi}
        hemisphere_image_urls.append(img_dict)
    


  # Store data in a dictionary
    nasa_data = {
        "news_title": news_title,
        "news_p": news_p,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls,
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return nasa_data
