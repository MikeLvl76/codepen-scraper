from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import sys, json
from time import sleep

def check_args() -> None:
    if len(sys.argv) == 1:
        raise ValueError('additional args must be provided !')

def init():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument('--log-level=1')
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def format_string_number(x: str):
    if not x.isnumeric:
        return 0
    return int(x)

def fetch_user_pens(driver, user: str):
    driver.get(f'https://codepen.io/{user}/pens/public?grid_type=list')
    print(driver.title)
    #driver.minimize_window()
    sleep(3)
    page = driver.find_element(By.ID, 'react-page')
    wrapper = page.find_element(By.CLASS_NAME, 'width-wrapper')
    
    titles = [elt for elt in map(lambda x: x.text, wrapper.find_elements(By.CLASS_NAME, 'title'))]
    updates = [elt for elt in map(lambda x: x.text, wrapper.find_elements(By.CSS_SELECTOR, "td[class='date updated']"))]
    loves, views = [], []

    stats = wrapper.find_elements(By.CLASS_NAME, 'list-stats')
    for stat in stats:
        divs = stat.find_elements(By.TAG_NAME, 'div')
        loves.append(format_string_number(divs[0].text))
        views.append(format_string_number(divs[2].text))

    pens = [{
        "title": title,
        "updated on": update,
        "loves": love,
        "views": view,
    } for title, update, love, view in zip(titles, updates, loves, views)]

    res = {
        "user": user,
        "pens": pens,
    }

    driver.quit()

    return json.dumps(res, indent=4)

if __name__ == '__main__':
    check_args()
    driver = init()
    print(fetch_user_pens(driver, sys.argv[1]))