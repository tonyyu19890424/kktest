import argparse
import os
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

HOST = "https://play.kkbox.com/"
class KKBOXTest(object):
    def __init__(self):
        self._driver = webdriver.Chrome()

    def login(self):
        CSS_NAV_ICON = "svg[class='icon-48']"
        self._driver.get(HOST)
        WebDriverWait(self._driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, CSS_NAV_ICON))
        )

    def quit(self):
        self._driver.quit()

    def test(self, test_type, query=""):
        print("you need to login!")
        self.login()

        if test_type == "collection":
            self.navgate_bar_control()
            self.song_list_play()

        elif test_type == "search":
            if query != "":
                self.search(query)
                self.song_play()
            else:
                print("You need to enter the query for searching!")

    def search(self, query):
        SEARCHINPUT = "search_hint"
        searchElement = self._driver.find_element_by_class_name(SEARCHINPUT)
        searchElement.send_keys(query)
        searchElement.send_keys(Keys.ENTER)

    def song_play(self):
#         you can using this function to play a song after searching

        CSS_ALBUM_PLAY = "div[context-menu='right-main-albumMode']"
        WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, CSS_ALBUM_PLAY))
        )
        element = self._driver.find_element_by_css_selector(CSS_ALBUM_PLAY)
        element.click()
        try:
            alert = self._driver.switch_to_alert()
            alert.accept()
        except:
            pass

    def song_list_play(self):
        CSS_SONG_LIST = "div[class='cover']"
        CSS_SONG_PLAY = "i[class='icon icon-playthis icon-28-b-play']"
        CSS_SONG_PLAY2 = "i[class='icon icon-40 icon-40-headerplay']"

        WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SONG_LIST))
        )
        elements = self._driver.find_elements_by_css_selector(CSS_SONG_LIST)
        while len(elements) <10:
            elements = self._driver.find_elements_by_css_selector(CSS_SONG_LIST)
        index = random.randint(0,len(elements))
        elements[index].click()

        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SONG_PLAY))
            )
            element = self._driver.find_element_by_css_selector(CSS_SONG_PLAY)
            element.click()
            pass
        except:
            pass

        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SONG_PLAY2))
            )
            element = self._driver.find_element_by_css_selector(CSS_SONG_PLAY2)
            element.click()
            pass
        except:
            pass

        try:
            alert = self._driver.switch_to_alert()
            alert.accept()
        except:
            pass

    def navgate_bar_control(self, index=1):
#         index    Go
#         0        My Play List
#         1        Special Collection
#         2        Radio
#         3        Listen Together
#         default index is 1
        CSS_ICON_SVG = "svg[class='icon-48']"
        WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, CSS_ICON_SVG))
        )
        elements = self._driver.find_elements_by_css_selector(CSS_ICON_SVG)
        elements[index].click()


def main():
    parser = argparse.ArgumentParser(description='KKBOX Test')
    parser.add_argument('-t', '--test_type', type=str, default='collection',
                        help="Options: 'collection' | 'search' ")
    parser.add_argument('-q', '--query', type=str, default='',
                        help="Query for searching")
    args = parser.parse_args()
    k_test = KKBOXTest()
    k_test.test(test_type=args.test_type, query=args.query)
    pause = input("Press Enter key to quit progress")
if __name__ == '__main__':
    main()
