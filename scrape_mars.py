#Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd

def init_browser():
# @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    #NASA Mars News Section
    url_Mars_News = 'https://mars.nasa.gov/news/'

    #Splinter Connection
    executable_path = {'executable_path':'chromedriver'}
    browser = Browser('chrome', **executable_path)
    browser.visit(url_Mars_News)

    html = browser.html
    soup = bs(html, 'html.parser')

    ###Nasa Mars News Site 
    #News Title from Site
    news_title = soup.find('div', class_='content_title').text

    #News Paragraph from Site
    news_paragraph = soup.find('div', class_='article_teaser_body').text

    #store as dictionary
    mars_news = {
            "news_title": news_title,
            "news_paragraph": news_paragraph
        }

    ###JPL Mars Space Images - Featured Image
    #URL for JPL Mars Space Image Site
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)
    time.sleep(10)
    html = browser.html
    soup = bs(html, "html.parser")

    image = soup.find("img", class_="thumb")["src"]
    image_url = "https://jpl.nasa.gov"+image

    ###Mars Weather
    url_mars_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_mars_weather)
    time.sleep(10)
    html = browser.html
    soup = bs(html,'html.parser')
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    #save
    weather_tweet = {
            " Weather Tweet": mars_weather
        }


    ###Mars Facts
    url_facts = "https://space-facts.com/mars/"
    browser.visit(url_facts)
    time.sleep(10)

    ##FACTS
    facts = pd.read_html(url_facts)[0]

    ###Mars Hemispheres
    ###################https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)
    time.sleep(10)
    hem_html = browser.html
    hemisphere_soup = bs(hem_html,'html.parser')

    #create results variable
    results = hemisphere_soup.find('h3')
    hemisphere_list = []
    #loop through results
    for x in results:

        #secure image title and links 
        title= results.text 
        browser.click_link_by_partial_text(title)
        hemisphere_htmls = browser.html
        hemisphere_soup = bs(hemisphere_htmls, "html.parser")
        url = hemisphere_soup.find('a', target='_blank').get("href")
        hemisphere_list.append({'Title': title, 'Hemisphere URL': url})
        browser.click_link_by_partial_text('Back')


    final_data ={}
    final_data["Mars_News"] = mars_news
    final_data["Mars_Image"] = url_image
    final_data["Mars_Weather"] = weather_tweet
    final_data["Mars_Facts"] = facts
    final_data["Mars_Hemispheres"] = hemisphere_list


    # Close the browser after scraping
    browser.quit()

    # Return results
    return final_data