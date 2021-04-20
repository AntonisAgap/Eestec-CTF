from flask import *
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_name = ""
        user_email = ""
        data = request.form.get('name', user_name)
        user_email = request.form.get('mail', user_email)
        child = """
        {% extends "index.html" %}
        {% block content %}
        <label> Thanks! We will be sure to send our news to : """+str(user_email)+""" </label>
        {% endblock %}
        """
        return render_template_string(child)
        
    elif request.method == 'GET':
        return render_template("index.html")
    

if __name__ == '__main__':
	app.run(debug=False,host='0.0.0.0',port=1337)