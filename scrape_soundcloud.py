import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
import time
import requests
import os

#Desktop Path
desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), 'Desktop')


#Get PlaylistNames
def which_playlists(URL):
    """@param URL: soundcloud playlist url page"""
    this_url = URL
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

        playlist_extensions = soup.find_all("a", class_ = {"soundTitle__title sc-link-dark"})
        playlist_extensions

        extensions_list = []
        for ext in playlist_extensions:
            extensions_list.append(str(ext.get("href")))
        these_urls = [('https://soundcloud.com' + i) for i in extensions_list]
    finally:
        driver.quit()
        return(these_urls)

#Returns playlist in dataframe format
def getplaylist(this_url):
    """param this_url: link of specific playlist url"""
    driver = webdriver.Chrome()
    try:
        driver.get(this_url)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
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

#Excel File
def get_excel(URL):
    playlist_dfs = []
    urls = which_playlists(URL)
    for i in urls:
        this_df = getplaylist(i)
        playlist_dfs.append(this_df)

    playlist_order = playlist_dfs[::-1]
    total_playlist = pd.concat(playlist_order).reset_index(drop = True)

    try:
        excel_name = '\\soundcloud_playlist'  + "." + "xlsx"
        writer = pd.ExcelWriter(desktop+str(excel_name), engine = 'xlsxwriter')
        total_playlist.to_excel(writer, sheet_name = 'total_playlist', index = False)
        for idx,val in enumerate(playlist_order):
            idx_ = idx + 1
            val.to_excel(writer, sheet_name = str(idx_), index =False)

    finally:
        writer.save()


get_excel("https://soundcloud.com/whoishe1/sets")
