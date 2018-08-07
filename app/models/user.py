from flask import current_app
from flask_login import UserMixin, current_user
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.function_class.search import isbn_or_key
from app.function_class.yushu_book import YuShuBook
from app.libs.enums import PendingStatus
from app.models.base import Base, db
from app import login_manager
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    _password = Column('password', String(100))
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(24), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    receive_counter = Column(Integer, default=0)
    send_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @property
    def summary(self):
        return dict(nickname=self.nickname,
                    beans=self.beans,
                    email=self.email,
                    send_receive=str(self.send_counter)+ '/' + str(self.receive_counter))

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        if isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def can_send_drift(self):
        if self.beans < 1:
            return False
        send_gift_count = Gift.query.filter_by(id=self.id, launched=True).count()
        reciver_book_count = Drift.query.filter_by(requester_id=self.id,
                                                   pending=PendingStatus.Success).count()
        if reciver_book_count < ((send_gift_count + 1)*2)-1:
            return True
        else:
            return False

    def has_in_gifts_and_wishes(self, isbn):
        if current_user.is_authenticated:
            if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                    launched=False).first():
                has_in_gifts = True
                return has_in_gifts
            if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                    launched=False).first():
                has_in_wishes = False
                return has_in_wishes

    def generate_token(self, expiration=1200):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        token = s.dumps({'id': self.id}).decode('utf-8')
        return token

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))



