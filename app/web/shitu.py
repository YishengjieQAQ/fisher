import json

from flask import jsonify, request, render_template, flash
from flask_login import current_user

from app.forms.book import search_forms
from app.function_class import yushu_book
from app.function_class.search import isbn_or_key
from app.function_class.yushu_book import YuShuBook
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.book import Bookviewmodel, Bookcollection
from app.view_models.trade import Tradeinfo

from app.web import web
@web.route('/test')
def test():
    list1 = ['jiejie','lailai']
    dict1 = {
        'jiejieaideshi':'lailai',
        'lailaiaideshi':'jiejie'
    }
    flash('lailaizhuzhu')
    flash('zhuzhulailai')
    return render_template('test.html', data=list1,data2=dict1)



@web.route('/book/search')
def search():

    form = search_forms(request.args) #这里的里面 要传入一个request.args参数 即为客户端获取的参数q和page具体的取值
    books = Bookcollection()
    if form.validate():
        q = form.q.data.strip() #这里调用form里的q时要在后面加上data
        page = form.page.data #同上
        isbn_and_key = isbn_or_key(q)
        yushu_book1 = yushu_book.YuShuBook()

        if isbn_and_key == 'isbn':
            yushu_book1.search_by_isbn(q)
        else:
            yushu_book1.search_by_key(q, page)

        books.fill(yushu_book1, q)
    else:
        flash('没有找到任何书籍信息')

    return render_template('search_result.html', books = books)


@web.route('/book/<isbn>/ditail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False
    # isbn_or_key = is_isbn_or_key(isbn)
    # if isbn_or_key == 'isbn':
    # 获取图书信息
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)

    if current_user.is_authenticated:
        # 如果未登录，current_user将是一个匿名用户对象
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    book = Bookviewmodel(yushu_book.first)
    # if has_in_gifts:
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes_model = Tradeinfo(trade_wishes)
    trade_gifts_model = Tradeinfo(trade_gifts)
    return render_template('book_detail.html', book=book, has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model)