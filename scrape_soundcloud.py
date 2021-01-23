import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
import datetime
import time
import requests
import os

TODAYS_DATE = datetime.date.today().strftime("%Y-%m-%d")


class GetSoundCloud:
    """Scrapts playlists from a Soundcloud user and outputs them into excel format

    Attributes:
        url: url address of soundcloud user.  i.e. https://wwww.soundcloud.com/MyUserAccount/sets

    """

    def __init__(self, url):
        """ Initialize GetSoundCloud Object """
        self.url = url

    def which_playlists(self):
        """ Loads all playslist from url page and saves the playlist names (slug) into a list """

        this_url = self.url
        user = self.url.split("/")[3]
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

            playlist_extensions = soup.find_all(
                "a", class_={"soundTitle__title sc-link-dark"}
            )

            extensions_list = [str(ext.get("href")) for ext in playlist_extensions]

            corr_ext = []
            for i in extensions_list:
                splt = i.split("/")
                if splt[1] == user and splt[2] == "sets":
                    corr_ext.append(i)

            these_urls = [("https://soundcloud.com" + i) for i in corr_ext]
            self.playlist_urls = these_urls
        finally:
            driver.quit()
            return these_urls

    # Returns playlist in dataframe format
    def getplaylist(self, this_url):
        """
        Retrieve artist and song from specified playlist

        Args:
            this_url: specific playlist url from the which_playlists method

        Returns:
            DataFrame: pandas dataframe of Artists and Tracknames of playlist

        """
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

            track_names = soup.find_all(
                "a", class_={"trackItem__trackTitle sc-link-dark sc-font-light"}
            )
            artist_names = soup.find_all(
                "a", class_={"trackItem__username sc-link-light"}
            )

            tracknames_list = [str(names.text) for names in track_names]

            artistnames_list = [str(names.text) for names in artist_names]

            playlist = pd.DataFrame(
                {
                    "Tracks": pd.Series(tracknames_list),
                    "Artists": pd.Series(artistnames_list),
                }
            )

        finally:
            driver.quit()
            return playlist

    def __repr__(self):
        return f"The set url is {self.url}"


# Excel File
def main(URL):
    playlist_dfs = []
    sc = GetSoundCloud(URL)

    urls = sc.which_playlists()
    for i in urls:
        this_df = sc.getplaylist(i)
        playlist_dfs.append(this_df)

    playlist_order = playlist_dfs[::-1]
    total_playlist = pd.concat(playlist_order).reset_index(drop=True)

    try:
        # Desktop Path
        desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

        # write XLSX
        excel_name = "\\soundcloud_playlist_" + TODAYS_DATE + "." + "xlsx"
        writer = pd.ExcelWriter(desktop + str(excel_name), engine="xlsxwriter")
        total_playlist.to_excel(writer, sheet_name="total_playlist", index=False)
        for idx, val in enumerate(playlist_order):
            idx_ = idx + 1
            val.to_excel(writer, sheet_name=str(idx_), index=False)

    finally:
        writer.save()


if __name__ == "__main__":
    try:
        val = input("Enter your soundcloud playlist page: ")
        print("Getting URL and playlists....")
        main(val)
        time.sleep(1)
        print("Scraping done! The excel file is on your desktop!")
    except Exception as e:
        print("GG NO RE, error due to" + str(e))
