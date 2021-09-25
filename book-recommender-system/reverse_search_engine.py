"""
The reverse search engine module: Find book title from cover art of books
"""
import json
import os

import nltk
import requests
from bs4 import BeautifulSoup
from flask import current_app
from nltk.corpus import stopwords
from transliterate import translit
from werkzeug.utils import secure_filename
from .db import get_db

# download the stopwords
nltk.download('stopwords')
# cache all the english stopwords
cachedStopWords = stopwords.words("english")


def get_url(image_file) -> str:
    """Creates a POST request with the user image input and then returns the URL link to be processed by the next module


    :param image_file: the image file uploaded by the user
    :return: URL in string format which can be accessed by a GET request
    :raises requests.exceptions.ConnectionError: raised when reverse image search API limit is reached
    """
    # get the storage file path
    file_path = os.path.join(current_app.instance_path, 'htmlfi', secure_filename(image_file.filename))

    # save the uploaded image file to the storage path
    image_file.save(file_path)

    # prepare the POST request
    files = {'upfile': ('blob', open(file_path, 'rb'), 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json',
              'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}

    # execute the POST request, raises requests.exceptions.ConnectionError when API limit is reached
    response = requests.post(current_app.config['SEARCH_URL'], params=params, files=files)

    # get the query string and create the URL
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    img_search_url = current_app.config['SEARCH_URL'] + '?' + query_string

    # return the URL
    return img_search_url


def remove_stopwords(keywords: set) -> list:
    """Utility function to remove the stopwords from set of keywords

    :param keywords: the keywords found from the reverse search result
    :return: all keywords with the stopwords (he, him, they ..) removed
    """
    return [w for w in keywords if w not in cachedStopWords]


def get_keywords_from_img(url: str) -> list:
    """Finds out the keywords from the image URL

    :param url: URL in string format which can be accessed by a GET request
    :return: list of keywords potentially matching the book title
    """
    # keywords to be stored
    keywords = set()

    # connect to the url and get the HTML content (reverse search result) using BeautifulSoup
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # section area where the img-to-text results exist
    div = soup.find("section", class_="CbirItem CbirTags")
    for section in div:
        span = section.find_all("span", class_="Button2-Text")
        for text_area in span:
            # translate the results to english
            translated = translit(text_area.text, 'ru', reversed=True).split()
            # add the translated words to keywords
            [keywords.add(word) for word in translated]

    # remove all the stopwords ('he', 'him', 'they' ...,  etc.)
    keywords = remove_stopwords(keywords)

    # return the keywords
    return keywords


def get_book_title_from_keywords(keywords: list) -> set:
    """

    :param keywords: list of keywords potentially matching the book title
    :return: collection of books (book_id, authors, title, image_url) that match the keywords
    """
    book_details = set()
    # connect to the database
    db = get_db()
    cur = db.cursor()
    # match the keywords with the book titles in the database
    for key in keywords:
        query_word = '%' + key + '%'
        # setting the LIMIT to 5, to ensure we get a max of 5 books per keyword
        sql_query = "SELECT book_id, authors, title, image_url FROM books WHERE title LIKE ? LIMIT 5"
        res_ = cur.execute(sql_query, (query_word,)).fetchall()
        for res in res_:
            # add the book titles
            book_details.add(res)

    # return the book details
    return book_details
