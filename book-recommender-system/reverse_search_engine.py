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


def get_url(f) -> str:
    # get the storage file path
    file_path = os.path.join(current_app.instance_path, 'htmlfi', secure_filename(f.filename))

    # save the uploaded file to the storage path
    f.save(file_path)

    # prepare the POST request
    files = {'upfile': ('blob', open(file_path, 'rb'), 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json',
              'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}

    # execute the POST request
    response = requests.post(current_app.config['SEARCH_URL'], params=params, files=files)

    # get the query string and create the URL
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    img_search_url = current_app.config['SEARCH_URL'] + '?' + query_string

    # return the URL
    return img_search_url


def remove_stopwords(s: set) -> list:
    return [w for w in s if w not in cachedStopWords]


def get_keywords_from_img(url):
    keywords = set()

    # connect to the url and get the HTML content
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # section area where the img-to-text results exist
    div = soup.find("section", class_="CbirItem CbirTags")
    for section in div:
        span = section.find_all("span", class_="Button2-Text")
        for text_area in span:
            # translate the results to english
            translated = translit(text_area.text, 'ru', reversed=True).split()
            [keywords.add(word) for word in translated]

    # remove all the stopwords ('a', 'an', 'the) etc.
    keywords = remove_stopwords(keywords)
    print(keywords)
    # return the keywords
    return keywords


def get_book_title_from_keywords(keywords):
    book_details = set()
    # connect to the database and find title matching keywords
    db = get_db()
    cur = db.cursor()
    for key in keywords:
        query_word = '%' + key + '%'
        sql_query = "SELECT book_id, authors, title, image_url FROM books WHERE title LIKE ? LIMIT 3"
        res_ = cur.execute(sql_query, (query_word,)).fetchall()
        for res in res_:
            book_details.add(res)

    # return the book details
    return book_details
