from flask import *
import random
import operator
import time
from datetime import date, datetime, timedelta
app = Flask(__name__)

start_time = datetime.now()
prev_answer = 0
ctr = 0


def make_expression():
    ops = {'+':operator.add,
           '-':operator.sub,
    }
    
    num1 = random.randint(0,10000)
    num2 = random.randint(1,10000)
    op = random.choice(list(ops.keys()))
    answer = ops.get(op)(num1,num2)
    expression = str(num1)+" "+op+" "+str(num2)
    return expression,answer

@app.route('/', methods=['GET', 'POST'])
def index():
    global ctr
    global prev_answer
    response = "Wrong!"
    user_answer = 0
    global start_time
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    start_time = datetime.now()
    expression, answer = make_expression()
    if request.method == 'POST':
        data = request.form.get('answer', user_answer)
        try:
            data = int(data)
            answer = int(answer)
            if data == prev_answer:
                response = "Correct!"
                ctr = ctr + 1
            else:
                response = "Wrong!"
                ctr = 0
        except:
            pass
        if duration > 5:
            response = "Too slow!"
            ctr = 0
        if ctr == 100:
            response = "INSSEC{w3ll_d0n3_y0u_kn0w_b4s1c_arithmetic!}"
            ctr = 0
        homepage  = render_template("index.html",expression = expression, response = response, cor_answers = str(ctr)+"/100")
        prev_answer = answer
        return homepage
    elif request.method == 'GET':
        ctr = 0
        homepage  = render_template("index.html",expression = expression, cor_answers = str(ctr)+"/100")
        prev_answer = answer
        return homepage

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
