import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

load_dotenv()

BASE_PAGE_URL = os.getenv("E_BASE_PAGE_URL")
CAR_SELECTOR = os.getenv("E_CAR_SELECTOR")


def fetch_cars():

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(BASE_PAGE_URL)
        time.sleep(5)

        cards = driver.find_elements(By.CSS_SELECTOR, CAR_SELECTOR)

        cars = []

        for card in cards[:10]:
            title = card.text
            link = card.get_attribute("href")
            cars.append({"title": title, "link": link})

        return cars

    finally:
        driver.quit()


if __name__ == "__main__":
    cars = fetch_cars()

    for car in cars:
        print(car)
