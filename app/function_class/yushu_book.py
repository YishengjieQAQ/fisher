from flask import current_app

from app.function_class import http


class YuShuBook:
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        real_isbn_url = self.isbn_url.format(isbn)
        result = http.HTTP.get_url(real_isbn_url)
        self.__fill_single(result)



    def search_by_key(self, key, page):
        real_key_url = self.keyword_url.format(key, current_app.config['PER_PAGE'], self.page_to_start(page))
        result = http.HTTP.get_url(real_key_url)
        self.__fill_collection(result)

    def __fill_single(self, data):
        self.total = 1
        self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    @classmethod
    def page_to_start(cls,page):
        return (page-1)*15

    @property
    def first(self):
        return self.books[0] if self.books[0] else None

