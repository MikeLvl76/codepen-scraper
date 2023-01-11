# Forked from [codepen-scraper](https://github.com/eduardoboucas/codepen-scraper.git)

## Introduction

Python version of web scraper previously made using Node and [cheerio](https://cheerio.js.org/). I used [Selenium](https://www.selenium.dev/) for exctracting elements from a CodePen user such as :

- Pens title
- Pens number of love
- Pens date of last update
- Pens number of views

A list of each pen informations is returned.

## How to run

Command for running code :

- On Windows : 
    ```bash
    python -u codepen.py --user=<codepen_username> --page_count=<positive integer or "all">
    ```

- On Linux :
    ```bash
    python3 -u codepen.py --user=<codepen_username> --page_count=<positive integer or "all">
    ```

Try for yourself !