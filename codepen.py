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

def fetch_user_pens(driver, user: str):
    driver.get(f'https://codepen.io/{user}/pens/public?grid_type=list')
    print(driver.title)
    #driver.minimize_window()
    sleep(3)
    page = driver.find_element(By.ID, 'react-page')
    wrapper = page.find_element(By.CLASS_NAME, 'width-wrapper')
    
    titles = [elt.text for elt in wrapper.find_elements(By.CLASS_NAME, 'title')]
    updates = [elt.text for elt in wrapper.find_elements(By.CSS_SELECTOR, "td[class='date updated']")]
    loves, coms, views = [], [], []

    stats = wrapper.find_elements(By.CLASS_NAME, 'list-stats')
    for stat in stats:
        divs = stat.find_elements(By.TAG_NAME, 'div')
        loves.append(int(divs[0].text.encode('ascii', 'ignore').decode('ascii')))
        coms.append(int(divs[1].text.encode('ascii', 'ignore').decode('ascii')))
        views.append(int(divs[2].text.encode('ascii', 'ignore').decode('ascii')))

    pens = [{
        "title": title,
        "updated on": update,
        "loves": love,
        "comments": com,
        "views": view,
    } for title, update, love, com, view in zip(titles, updates, loves, coms, views)]

    res = {
        "user": user,
        "url": driver.current_url,
        "pens": pens,
    }

    driver.quit()

    return json.dumps(res, indent=4)

if __name__ == '__main__':
    check_args()
    driver = init()
    print(fetch_user_pens(driver, sys.argv[1]))