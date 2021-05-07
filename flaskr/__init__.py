from flask import Flask, request, render_template
import os

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    press = []
    @app.route('/', methods=['GET', 'POST'])
    def index():
        #print(request.method)
	question = ['Sample Question' 'Answer 1' 'Answer 2' 'Answer 3' 'Answer4'] 
        if request.method == 'POST':
            if request.form.get('1') == '1':
                print('Pressed button1')
		press.append('button1')
		print(press)
            elif request.form.get('2') == '2':
                print('Pressed 2')
		press.append('button2')
	    elif request.form.get('3') == '3':
                print('Pressed 3')
		press.append('button3')
            elif request.form.get('4') == '4':
                print('Pressed 4')
		press.append('button4')
            else:
                return render_template("hello.html", press=press,question=question)
        elif request.method == 'GET':
            return render_template("hello.html",press=press,question=question)
        return render_template("hello.html", press=press,question=question)

    return app