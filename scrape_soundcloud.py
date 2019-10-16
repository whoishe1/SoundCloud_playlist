import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

#returns playlist in dataframe format
def getplaylist(this_url):
    """param this_url: link of playlist url"""
    driver = webdriver.Chrome()
    try:
        driver.get(this_url)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(driver.page_source, "html.parser")

        TrackNames = soup.find_all("a", class_ = {'trackItem__trackTitle sc-link-dark sc-font-light'})
        ArtistNames = soup.find_all("a", class_ = {"trackItem__username sc-link-light"})

        tracknames_list = []
        for names in TrackNames:
            tracknames_list.append(str(names.text))

        artistnames_list = []
        for names in ArtistNames:
            artistnames_list.append(str(names.text))

        playlist = pd.DataFrame({'Tracks':pd.Series(tracknames_list), 'Artists':pd.Series\
                        (artistnames_list)})
        
    finally:
        driver.quit()
        return(playlist)


df = getplaylist(this_url = "your_playlist")

