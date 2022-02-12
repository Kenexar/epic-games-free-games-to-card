import json
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class Game:
    def __init__(self, href=""):
        self.href = href

        self.__get_store_link()

    def __get_store_link(self):
        base_url = "https://www.epicgames.com"
        self.store_url = base_url + self.href


free_games = []

def get_free_games():
    response = requests.get(
        "https://www.epicgames.com/store/de/browse?sortBy=releaseDate&sortDir=DESC&priceTier=tierFree&category=Game"
        "&count=90&start=0")

    s1 = BeautifulSoup(response.text, "html.parser").find(class_="css-cnqlhg")

    for s in s1.find_all(class_="css-1jx3eyg"):
        free_games.append(Game(href=s["href"]))


def game_add_shopping_cart():
    s = Service("lib/chromedriver.exe")

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--auto-open-devtools-for-tabs")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--headless")

    def load_cookie(driver, path):
        with open(path, 'r') as cookiesfile:
            cookies = json.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

    with webdriver.Chrome(options=options, service=s) as browser:
        start = time.time()
        for game in free_games:
            browser.get(game.store_url)
            load_cookie(browser, "cookie.json")
            browser.get(game.store_url)

            if not browser.find_element(By.CLASS_NAME, "css-8en90x"):
                content = browser.find_element(By.CLASS_NAME, "css-1xs0iza")
                print(len(content))
                ActionChains(browser).click(content).perform()
                print(f"{game.href} added to card!")
            else:
                print("Already in biblo")

        end = time.time()
        print(f" [{end - start:.2f}]")
        browser.quit()


def main():
    get_free_games()
    game_add_shopping_cart()


if __name__ == '__main__':
    main()
