# Forked from [codepen-scraper](https://github.com/eduardoboucas/codepen-scraper.git)

## Introduction

Python version of web scraper previously made using Node and [cheerio](https://cheerio.js.org/). I used [Selenium](https://www.selenium.dev/) for exctracting elements from a CodePen user such as :

- Pens title
- Pens comments
- Pens number of love
- Pens date of last update
- Pens number of views
- An amount of wanted pages

A list of each pen informations is returned.

## How to run

- You need a username, you can take randomly one username (you have to look for it in CodePen) or one of your friends username. 

- You can specify the amount of page to fetch (by default: 1) or choose to fetch them all.

- You can save the result in a file with these extensions : `.json`, `.csv`, `.tsv` or `.txt`

## Example

Try for yourself !

```bash
# On Windows
python -u codepen.py --user=username --page_count=2 --output=file_output.json
```

```bash
# On Linux
python3 -u codepen.py --user=username --page_count=2 --output=file_output.json
```

**Note** : If you choose to store data in txt files you can gather them into a directory by using `-g` or `--gather` option.

This is just an example, it might not work and serve as example and model.

Don't forget to use `-h` or `--help` to have an explanation for each argument !