from flask import Flask ,render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, MultipleFileField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('remember me')
    submit = SubmitField('Log in')


class FortyTwoForm(FlaskForm):
    answer = IntegerField('the number')
    submit = SubmitField()

    def validate_answer(form, field):
       if field.data != 42:
          raise ValidationError('must be 42.')

class UploadForm(FlaskForm):
    photo = FileField('Upload image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('提交')

class MultiUploadForm(FlaskForm):
    photo = MultipleFileField('Upload image', validators=[DataRequired()])
    submit = SubmitField('提交上传')

class RichTextForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = CKEditorField('body', validators=[DataRequired()])
    submit = SubmitField('Publish')

class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = TextAreaField('Body', validators=[DataRequired()])
    save = SubmitField('Save')
    publish = SubmitField('Publish')

class SignLoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('password', validators=[DataRequired(), Length(8, 128)])
    submit = SubmitField('Log in')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(1, 10)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    password = PasswordField('password', validators=[DataRequired(), Length(8, 128)])
    submit2 = SubmitField('Register')