"""CS105: Python: Assignment 1

Get yourself started with a development environment and write some
code and look at the Python documentation.

For 85%:
* Fill in the fac function with an implementation of the factorial
  funcion.

For 100%:
* Convert fib to use a loop.
* Implement fac on one line using one standard library function and
  the product function below. You should look up functools.reduce in
  the documentation and be able to tell how what it does.

None of your code should print any output. You will lose points if it
does. If you want to have some debugging prints you do not have to
remove look up and use the logging package in the standard library.

See:
https://docs.python.org/3/library/functions.html
https://docs.python.org/3/tutorial/controlflow.html#for-statements

Feel free to use any code you find in the Python documention. However
you should cite the source of the code in a comment.

"""

import functools

# covered then case when l is empty list
def product(l):
    if len(l) == 0:
        return 1
    else:
        def times(x, y):
            return x * y
        return functools.reduce(times, l)

# Convert fib to use a loop, return None if input is negative
def fib(n):
    if n < 0:
        return None
    if n == 0 or n == 1:
        return n
    if n > 1:
        num1 = 0
        num2 = 1
        fibonacci = 0
        for _ in range(n-1):
            fibonacci = num1 + num2
            num1 = num2
            num2 = fibonacci
        return fibonacci

# def fib(n):
#     if n <= 1:
#         return n
#     else:
#         return fib(n-1) + fib(n-2)

# Implement fac on one line using one standard library function and
# the product function above.
def fac(n):
    return None if n < 0 else (product(list(i for i in range(1,n+1))))
