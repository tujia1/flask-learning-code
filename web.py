from flask import Flask, render_template

app = Flask (__name__)


@app.route ('/')
def hello():
    return render_template ('index.html')


@app.route ('/user/<name>')
def user(name):
    return render_template ('user.html', name=name)


@app.route ('/simple.html')
def test():
    return render_template ('simple.html', title="Title H", content='this is content' )


if __name__ == '__main__':
    app.run (debug=True)


