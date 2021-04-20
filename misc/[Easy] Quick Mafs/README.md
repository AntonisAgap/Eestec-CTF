# [__Quick Mafs 🎓__](#)

## Description: 

* It's basic addition and subtraction. The question is: Can you do it?

## Objective: 

* Create a web scraping solver to get the expression and send a post request with the answer.

## Flag: 🏁
* `INSSEC{w3ll_d0n3_y0u_kn0w_b4s1c_arithmetic!}`

### Difficulty:
* Easy 

## Writeup

We needed to create a web scraper app to solve the expressions and send them back to the flask web app.
```python
from re import S
import requests
from bs4 import BeautifulSoup
import operator

ops = {'+':operator.add,
        '-':operator.sub,
    }

url = 'http://127.0.0.1:5000/' #change
page = requests.get(url)

for i in range(100):
    soup = BeautifulSoup(page.content, 'html.parser')
    expression = soup.select('label')[2].string
    expression = expression.split()
    op = ops.get(str(expression[1]))
    num1 = int(expression[0])
    num2 = int(expression[2])
    answer = op(num1,num2)
    myobj = {"answer":str(answer)}

    page = requests.post(url, data = myobj)
    soup = BeautifulSoup(page.content, 'html.parser')
print(soup.select('label')[1].string)
```
The flag is: `INSSEC{w3ll_d0n3_y0u_kn0w_b4s1c_arithmetic!}`