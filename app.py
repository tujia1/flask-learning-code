import uuid
from flask import Flask, redirect, make_response, url_for, request, session, abort, render_template, flash, send_from_directory
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum, escape
from flask import Markup
from flask_ckeditor import CKEditor, upload_success, upload_fail
from form import LoginForm, UploadForm, MultiUploadForm, RichTextForm, NewPostForm, SignLoginForm, RegisterForm
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
import os

# -*- coding: utf-8 -*-

app = Flask(__name__)
app.secret_key = '7ScKjnuBvhH9'
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']
app.config['CKEDITOR_SERVE_LOCAL'] = True
# app.config['CKEDITOR_FILE_UPLOADER'] = 'upload_for_ckeditor'

'''
result.scheme : 网络协议
result.netloc: 服务器位置（也有可能是用户信息）
result.path: 网页文件在服务器中的位置
result.params: 可选参数
result.query: &连接键值对
'''
ckeditor = CKEditor(app)


@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for ('hello'))


@app.route ('/hello', methods=['GET', 'POST'])
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name')
        response = '<h1> hello %s</h1>' % escape (name)
    if 'logged_in' in session:
        response += '[SUESSE]'
    else:
        response += '[no authenticated]'
    return response


@app.route ('/admin')
def admin():
    if 'logged_in' not in session:
        abort (403)
    return 'welcome to admin page'


@app.route ('/greet', defaults={'name': 'admin'})
@app.route ('/greet/<name>')
def greet(name):
    return '<h1> hello, %s!</h1>' % escape (name)


@app.route ('/huangwang')
def huangwang():
    return redirect ('greet')


@app.route('/foo')
def foo():
    return '<h1> foo page </h1><a href="%s">do something and redirect</a>' % url_for ('do_something',next=request.full_path)

@app.route('/bar')
def bar():
    return '<h1> bar page </h1><a href="%s">do something and redirect</a>' % url_for('do_something',next=request.full_path)


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin (request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/do-something')
def do_something():
    return redirect_back ()


@app.route ('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
    <h1>A very long post</h1>
    <div class="body">%s</div>
    <button id="load">Load More</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
        $(function(){
            $('#load').click(function() {
                $.ajax({
                 url: '/more',
                 
                 type: 'get',
                 success: function(data){
                     $('.body').append(data);
                 }
             })
         })
    })
    </script>''' % post_body


@app.route('/more')
def load_more():
    return generate_lorem_ipsum(n=1)


@app.route ('/set/<name>')
def set_cookie(name):
    response = make_response (redirect (url_for ('hello')))
    response.set_cookie ('name', name)
    return response


user = {'username': '李晓明', 'bio': 'a boy who loves movies and music.'}
movies = [{'name': 'aaa', 'year': '1991'}, {'name': 'bbb', 'year': '1992'}, {'name': 'ccc', 'year': '1993'},
          {'name': 'ddd', 'year': '1994'}]


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/watch')
def watch():
    return render_template ('watch.html', user=user, movies=movies)


'''
使用app.jinja_env.globals向模板添加全局函数bar和foo
使用app.jinja_env.filters向模板添加自定义过滤器
使用app.jinja_env.test向模板添加自定义测试器
'''


def bar():
    return 'i am bar'


foo = 'i am foo.'
app.jinja_env.globals['bar'] = bar
app.jinja_env.globals['foo'] = foo


def smiling(s):
    return s + ':)'


app.jinja_env.filters['smiling'] = smiling


def baz(n):
    if n == 'baz':
        return True
    return False


app.jinja_env.tests['baz'] = baz
'''
自定义过滤器 使用app.template_filter()装饰器可以注册自定义过滤器
自定义测试器 使用app.template_test()装饰器可以注册自定义测试器
'''


@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')


@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False

@app.route('/flash')
def just_flash():
    flash(u'哈喽， 你好。欢迎来到精神病院！')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
       username = form.username.data
       flash('welcome %s home' % username)
       return redirect(url_for('index'))
    return render_template('basic.html', form=form)

@app.route('/uploads/<path:filename>')
def get_filename(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')


def random_filename(filename):
    ext = os.path.split(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload success')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)

@app.route('/mulit-upload', methods=['GET', 'POST'])
def mulit_upload():
    form = MultiUploadForm()
    if request.method == 'POST':
        filenames = []
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CRSF token error.')
            return redirect(url_for('mulit_upload'))
        if 'photo' not in request.files:
            flash('This field is required.')
            return redirect(url_for('mulit_upload'))
        for f in request.files.getlist('photo'):
            if f and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                filenames.append(filename)
            else:
                flash('invalid file type')
                return redirect(url_for('mulit_upload'))
        flash('Hi bro upload success,do like something?')
        session['filenames']=filenames
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)




@app.route('/ckeditor', methods=['GET', 'POST'])
def ckeditor():
    form = RichTextForm()
    if form.validate_on_submit:
        title = form.title.data
        body = form.body.data
        flash('Your post is published!')
        return render_template('post.html', title=title, body=body)
    return render_template('ckeditor.html', form=form)

@app.route('/two-submits', methods=['GET', 'POST'])
def two_submits():
    form = NewPostForm()
    if form.validate_on_submit():
        if form.save.data:
            # save it...
            flash('You click the "Save" button.')
        elif form.publish.data:
            # publish it...
            flash('You click the "Publish" button.')
        return redirect(url_for('index'))
    return render_template('2submit.html', form=form)

@app.route('/mulit-form', methods=['GET', 'POST'])
def mulit_form():
    sign_form = SignLoginForm()
    register_form = RegisterForm()

    if sign_form.submit.data and sign_form.validate():
        username = sign_form.username.data
        flash('%s, you just submit the sigin form.' % username)
        return redirect(url_for('index'))
    if register_form.submit2.data and register_form.validate():
        username = register_form.username.data
        flash('%s, you just submit the Register Form.' % username)
        return redirect(url_for('index'))

    return render_template('2form.html', sign_form=sign_form, register_form=register_form)



if __name__ == '__main__':
    app.run(debug=True)
