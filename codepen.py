from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from argparse import ArgumentParser, Namespace, ArgumentError, ArgumentTypeError
from json import dumps
from time import sleep, time
from os import path, getcwd, mkdir, sep
from re import match
import pandas as pd
import random
import string

def parse_args() -> Namespace:
    '''
        Parse command prompt arguments
    '''
    parser = ArgumentParser(description="Arguments and their features",
                                         usage='%(prog)s [-h] [-usr USER] [-pn PAGE_NUMBER] [-all ALL_PAGES]',
                                         epilog="Use -h or --help to see more about arguments")
    parser.add_argument(
        '-usr', '--user', help='Enter CodePen username', type=str, required=True)

    parser.add_argument(
        '-pc', '--page_count', help='Enter the count of desired pages', type=str, default='1', required=False)

    parser.add_argument(
        '-o', '--output', help='Save result in file (json, csv/tsv or txt)', type=str, required=False)

    parser.add_argument(
        '-g', '--gather', help='Put output files into directory, only applied with txt files', action='store_true', required=False)

    return parser.parse_args()


def check_args(args: Namespace) -> None:
    '''
        Check if args are correct when used
    '''
    if args.user == '':
        raise ArgumentError(message='you must provide username !')

    if not args.page_count.isnumeric() and args.page_count != 'all':
        raise ArgumentTypeError('positive integer expected or "all" expected !')

    if args.page_count != 'all' and int(args.page_count) < 1:
        raise ArgumentTypeError('positive integer expected !')

    if match(r'^[\w,\s-]+\.[A-Za-z]{2,4}$', args.output) is None:
        raise ArgumentError(message='wrong filename or file extension !')

def init() -> Chrome:
    options = ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument('--log-level=1')
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    return Chrome(service=service, options=options)

def fetch_user_page(driver: Chrome, user: str) -> WebElement:
    '''
        Fetch user page main div
    '''
    driver.get(f'https://codepen.io/{user}/pens/public?grid_type=list')
    sleep(2)
    h1 = driver.find_element(By.TAG_NAME, 'h1').text
    if h1 == '404':
        raise NoSuchElementException('invalid user')
    return driver.find_element(By.ID, 'react-page')

def fetch_user_pens(page: WebElement) -> list[dict]:
    '''
        Get all user pens on a page
    '''
    titles = [elt.text for elt in page.find_elements(By.CSS_SELECTOR, 'th[class="title"]')]
    updates = [elt.text for elt in page.find_elements(By.CSS_SELECTOR, "td[class='date updated']")]
    loves, coms, views = [], [], []

    stats = page.find_elements(By.CLASS_NAME, 'list-stats')
    for stat in stats:
        divs = stat.find_elements(By.TAG_NAME, 'div')
        loves.append(int(divs[0].text.encode('ascii', 'ignore').decode('ascii')))
        coms.append(int(divs[1].text.encode('ascii', 'ignore').decode('ascii')))
        views.append(int(divs[2].text.encode('ascii', 'ignore').decode('ascii')))

    return [{
        "title": title,
        "updated at": update,
        "loves": love,
        "comments": com,
        "views": view,
    } for title, update, love, com, view in zip(titles, updates, loves, coms, views)]

def fetch_pens_on_many_pages(driver: Chrome, page: WebElement, page_count: str = '1') -> list[dict]:
    '''
        Go to the next pages for retrieving pens
    '''
    pens_page = []
    if page_count != 'all':
        for i in range(int(page_count)):
            try:
                sleep(2)
                pens_page.append((fetch_user_pens(page), i + 1, driver.current_url))
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable(page.find_element(By.CSS_SELECTOR, 'button[data-direction="next"]'))).click()
                sleep(2)
            except NoSuchElementException:
                break
        
        return [{'url': pen[2], f'Page {pen[1]}': pen[0]} for pen in pens_page]

    if page_count == 'all':
        index = 0
        while True:
            try:
                sleep(2)
                index += 1
                pens_page.append((fetch_user_pens(page), index, driver.current_url))
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable(page.find_element(By.CSS_SELECTOR, 'button[data-direction="next"]'))).click()
                sleep(2)
            except NoSuchElementException:
                break

        return [{'url': pen[2], f'Page {pen[1]}': pen[0]} for pen in pens_page]

    return [{}]

def save_results(output: str, gather: bool, user: str, pens: list[dict]) -> None:
    '''
        Save the result in a file or just print it.
        Allowed extensions : .json, .csv, .tsv and .txt
        Gathering txt files into a dir is possible.
    '''
    dir_path = f'{getcwd()}{sep}results'

    if not path.exists(dir_path):
        mkdir(dir_path)

    extension = output.split('.')[-1]

    if extension == 'json':
        res = {
            "user": user,
            "pens": pens,
        }
        with open(f'{dir_path}{sep}{user}_{output}', 'w', encoding='utf-8') as writer:
            writer.write(dumps(res, indent=4))

        return None

    if extension in ['csv', 'tsv']:

        items = [pen[list(pen.keys())[-1]] for pen in pens]
        flatten = [elt for item in items for elt in item]
        titles, dates, loves, comments, views = [], [], [], [], []

        for value in flatten:
            titles.append(value['title'])
            dates.append(value['updated at'])
            loves.append(value['loves'])
            comments.append(value['comments'])
            views.append(value['comments'])

        res = {
            'Title': titles,
            'Date of update': dates,
            'Loves': loves,
            'Comments': comments,
            'Views': views,
        }

        df = pd.DataFrame(res)
        separator = ','
        if extension == 'tsv':
            separator = '\t'

        df.to_csv(f'{dir_path}{sep}{user}_{output}', sep=separator)
        return None

    if extension == 'txt':

        randomly_named_dir = f'{dir_path}{sep}txt_output_dir'

        if gather:
            # checking if dir already exists
            if path.exists(randomly_named_dir):
                # prevent duplicated name
                random_name = ''
                while path.exists(randomly_named_dir + random_name):
                    random_name = "".join(random.choices(string.ascii_letters + string.digits, k=5))

                randomly_named_dir += f'_{random_name}'

            # create the new dir
            mkdir(randomly_named_dir)
        
        for pen in pens:

            page = list(pen.keys())[-1].lower().replace(' ', '_')
            items = pen[list(pen.keys())[-1]]
            filepath = f'{dir_path}{sep}{user}_{page}_{output}'

            if gather:
                filepath = f'{randomly_named_dir}{sep}{user}_{page}_{output}'

            file = open(filepath, 'w', encoding='utf-8')
            file.write(f'{"=" * 20} Pens of {user} (Page {page.split("_")[1]}) {"=" * 20}\n\n')

            for item in items:
                title = item['title']
                date = item['updated at']
                love = item['loves']
                comment = item['comments']
                view = item['views']

                file.write(f'{"=" * 20} Pen n°{items.index(item) + 1} {"=" * 20}\nTitle : {title}\n\tUpdated at : {date}\n\tNumber of loves approbation : {love}\n\tNumber of comments : {comment}\n\tNumber of views : {view}\n\n')
            
            file.write(f'{"=" * 20} End of page {"=" * 20}')
            file.close()

        return None

    res = {
        "user": user,
        "pens": pens,
    }

    print(dumps(res, indent=4))

if __name__ == '__main__':

    print('Reading and checking args...')
    args = parse_args()
    check_args(args)
    print('Args are ok !')

    print('Launching driver...')
    driver = init()
    print('Driver ready !')

    print('Fetching data...')
    t1 = time()
    page = fetch_user_page(driver, args.user) # get main div of user page
    pens = fetch_pens_on_many_pages(driver, page, args.page_count) # get pens on many pages
    save_results(output=args.output, gather=args.gather, user=args.user, pens=pens)
    t2 = time()
    print('Data saved !')

    print('Closing driver...')
    driver.close()
    print('Driver closed.')

    print(f'Execution time : {round(t2 - t1, 4)}s')