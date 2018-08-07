import wtforms
from wtforms import StringField, Form, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


class search_forms(Form):

    q = StringField(validators=[Length(min=1, max=30)])

    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)


class DriftForm(Form):
    recipient_name = StringField(validators=[DataRequired(),
                                             Length(min=2, max=30,
                                                    message='收件人姓名必须在2-30个字符之间')])
    mobile = StringField(validators=[DataRequired(),
                                     Regexp('^1[0-9]{10}$', 0, '请输入正确的手机号')])
                                        #^是值开头严格匹配，$是值从末尾开始严格匹配

    message = StringField()

    address = StringField(validators=[DataRequired(),
                                      Length(min=10, max=80,
                                             message='地址必须填写详细在10-80个字符之间')])
