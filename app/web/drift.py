from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from app.forms.book import DriftForm
from app.libs.email import send_email
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import Bookviewmodel
from app.view_models.drift import DriftCollection
from . import web




@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    form = DriftForm(request.form)
    if form.validate() and request.method == 'POST':
        save_drift(form, current_gift)

        send_email(current_gift.user.email, '有人想要一本书', 'email/get_gift.html',
                  wisher=current_user, gift=current_gift)
        return redirect(url_for('web.pending'))
    if current_gift.is_your_self_gift(current_user.id):
        flash('这本书是您自己的，您不可以对自己发起请求')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))
    can = current_user.can_send_drift()
    gifter = current_gift.user.summary

    if can:
        return render_template('drift.html', gifter=gifter, user_beans=current_user.beans, form=form)
    elif not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)





@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(or_(Drift.requester_id == current_user.id,
                                    Drift.gifter_id == current_user.id))\
                                    .order_by(desc(Drift.create_time)).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(Drift.id == did,
                                   Gift.uid == current_user.id) \
            .first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(Drift.id == did,
                                   Drift.requester_id == current_user.id)\
                        .first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(Drift.id == did,
                                   Drift.gifter_id == current_user.id)\
                        .first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += 1
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True
        wish = Wish.query.filter_by(uid=drift.requester_id, isbn=drift.isbn, launched=False).first_or_404()
        wish.launched = True
    return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)

        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gift_id = current_gift.id
        drift.gifter_id = current_gift.user.id
        drift.gifter_nickname = current_gift.user.nickname

        book = Bookviewmodel(current_gift.current_book)

        drift.isbn = book.isbn
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image

        current_user.beans = current_user.beans - 1

        db.session.add(drift)

