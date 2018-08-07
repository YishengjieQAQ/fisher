from flask import current_app
from sqlalchemy import Integer, Column, Boolean, String, desc, func
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from app.function_class.yushu_book import YuShuBook
from app.models.base import Base, db


class Wish(Base):
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)

    @property
    def current_book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_wishes(cls, uid):
        gifts = Wish.query.filter_by(uid=uid, launched=False
                                     ).order_by(desc(Wish.create_time
                                                     )).all(
        )
        return gifts

    @classmethod
    def get_gift_counts(cls, isbn_list):
        from app.models.gift import Gift
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        print(count_list)
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        print(count_list)
        return count_list

    @classmethod
    def recent(cls):
        recent_wish = Wish.query.filter_by(launched=False).group_by(
            Wish.isbn).order_by(desc(Wish.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_wish