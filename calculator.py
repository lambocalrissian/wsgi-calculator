#!/usr/bin/env python3

"""
Usage:
python3 -u calculator.py
For your homework this week, you'll be creating a wsgi application of
your own.
You'll create an online calculator that can perform several operations.
You'll need to support:
  * Addition
  * Subtractions
  * Multiplication
  * Division
Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.
Consider the following URL/Response body pairs as tests:
```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```
To submit your homework:
  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!
"""

import traceback


def front_page(*args):
    return """
        <h2>Wsgi Calculator
        <h4>Instructions</h4>
        <p>Add, Subtract, Multiply, or Divide by putting your arguments
        into the URL as different elements separated by slashes.</p>
        <p><strong>Here are some examples:</strong>
        <br>
        <ul>
          <li>http://localhost:8080/multiply/3/5   => 15<br>
          <li>http://localhost:8080/add/23/42      => 65<br>
          <li>http://localhost:8080/subtract/23/42 => -19<br>
          <li>http://localhost:8080/divide/22/11   => 2</p><br></p>
          </ul>
    """


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    sum = 0

    for num in args:
        sum += int(num)
    return f"Sum of arguments is: {sum}"


def subtract(*args):
    """ Returns a STRING with the sum of the arguments """
    difference = 0
    difference = int(args[0]) - int(args[1])
    return f"Difference is: {difference}"


def multiply(*args):
    """ Returns a STRING with the sum of the arguments """
    product = 0
    product = int(args[0]) * int(args[1])
    return f"Product is: {product}"
# TODO: Add functions for handling more arithmetic operations.


def divide(*args):
    """ Returns a STRING with the sum of the arguments """
    num1, num2 = args
    try:
        dividend = int(num1) / int(num2)
    except ZeroDivisionError:
        return f"Division by Zero Error: {num1}/{num2}"

    return f"Dividend is: {dividend}"


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    # func = add
    # args = ['25', '32']
    funcs = {
        '': front_page,
        'add': add,
        'multiply': multiply,
        'subtract': subtract,
        'divide': divide,
    }

    # turns /book/id1 into ['book', 'id1']
    # turns / into ['']
    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    # print('entering application func')
    path = environ.get('PATH_INFO', None)
    print("path:", path)

    try:
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()