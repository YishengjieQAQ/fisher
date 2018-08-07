from flask import current_app
from sqlalchemy import Integer, Column, Boolean, String, desc, func
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from app.function_class.yushu_book import YuShuBook
from app.models.base import Base, db


class Gift(Base):
    id = Column(Integer, primary_key=True)
    launched = Column(Boolean, default=False)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)

    def is_your_self_gift(self, uid):
        return True if self.id == uid else False



    @property
    def current_book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False
                                     ).order_by(desc(Gift.create_time
                                                     )).all(
        )
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @classmethod
    def recent(cls):
        recent_gift = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift