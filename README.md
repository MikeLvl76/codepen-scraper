# Forked from [codepen-scraper](https://github.com/eduardoboucas/codepen-scraper.git)

## About

Python version of web scraper previously made using Node and [cheerio](https://cheerio.js.org/). I used [Selenium](https://www.selenium.dev/) for exctracting elements from a CodePen user such as :

- Pens title
- Pens comments
- Pens number of love
- Pens date of last update
- Pens number of views
- An amount of wanted pages

A list of each pen informations is returned.

## Get started

Here is all command line arguments :

- `-usr` or `--user` : provide an username (mandatory)
- `-pc` or `--page_count` : fetch a number of page or all if 'all' is typed, by default it fetches one page
- `-o` or `--output` : give a filename with these extensions : `.json`, `.csv`, `.tsv` or `.txt` (mandatory)
- `-g` or `--gather` : if `txt` is chosen you can put them into a directory

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

This is just an example, it might not work and serves as example and model.

Don't forget to use `-h` or `--help` to have an explanation for each argument !

## Output file example

In case of saving output in file the username is automatically appended to the filename and you will have different results for each file here is below an example of each file content :

- JSON

    **There are 2 main keys : one for user name and another one for pens. The `pens` key stores list of each pen, which contains itself 2 other keys such as `url` for url used and `Page` + `index` for indexing visited pages. The value of `Page 1` is a list that contains pens of the page.**

    ```json
    {
        "user": "username",
        "pens": [
            {
                "url": "https://codepen.io/userexample/pens/public?grid_type=list",
                "Page 1": [
                    {
                        "title": "Example title",
                        "updated at": "January 10, 2023",
                        "loves": 0,
                        "comments": 0,
                        "views": 0
                    },
                    ...
                ]
            },
            ...
        ]
    }
    ```

- CSV

    **The head row shows informations about pens, unlike JSON file url and page index are not stored. Each row displays pen's information independantly of the page. Each value for column is separated by a comma.**

    ```csv
    ,Title,Date of update,Loves,Comments,Views
    0,Example Title,"January 10, 2023",0,0,0
    ...
    ```

- TSV

    **The head row shows informations about pens, unlike JSON file url and page index are not stored. Each row displays pen's information independantly of the page. Each value for column is separated by a tabulation.**

    ```tsv
        Title   Date of update  Loves   Comments    Views
    0   Example Title   "January 10, 2023"  0   0   0
    ...
    ```

- TXT

    **For each page visited a txt file is created and each file displays only pens in the page. Each pen has an index in purpose of more readability. Note when many files are created each one indicates page number in its name.**

    ```txt
    ==================== Pens of username (Page 1) ====================

    ==================== Pen n°1 ====================
    Title : Example Title
        Updated at : January 10, 2023
        Number of loves approbation : 0
        Number of comments : 0
        Number of views : 0

    ==================== End of page ====================
    ```
