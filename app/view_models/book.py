class Bookviewmodel:
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = '、'.join(book['author'])
        self.image = book['image']
        self.price = book['price']
        self.summary = book['summary']
        self.pages = book['pages']
        self.isbn = book['isbn']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,[self.publisher, self.author, self.price])
        return '/'.join(intros)


class Bookcollection:

    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [Bookviewmodel(book) for book in yushu_book.books]





class Bookviewmodel_:
    @classmethod
    def package_single(cls,data,keyword):
        returned = {
            'books' : [],
            'total' : 0,
            'keyword' : keyword
        }
        if data:
            returned['books'] = [cls.__cut_book_data(data)]
            returned['total'] = 1
        return returned
    @classmethod
    def package_collection(cls,data,keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['books'] = [cls.__cut_book_data(book)for book in data['books']]
            returned['total'] = data['total']
        return returned


    @classmethod
    def __cut_book_data(cls,data):
        book = {
            'author':'、'.join(data['author']),
            'image' : data['image'],
            'publisher' : data['publisher'],
            'pages' : data['pages'] or '',
            'price' : data['price'],
            'summary' : data['summary'] or ''



        }
        return book
