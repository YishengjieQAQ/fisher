from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不合规范')])

    password = PasswordField(validators=[DataRequired(message='密码必须在6-24位'), Length(6, 64)])

    nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称至少需要2个字符且最多10个')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱输入不合规范')])


class LoginForm(EmailForm):
    password = PasswordField(validators=[DataRequired(message='密码必须在6-24位之间'),
                                         Length(6, 64)])


class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[DataRequired(),
                                          Length(6, 32, message='密码长度不在6-32位之间'),
                                          EqualTo('password2', message='两次密码输入不一致')])
    password2 = PasswordField(validators=[DataRequired(),
                                          Length(6, 32, message='密码长度不在6-32位之间')])


