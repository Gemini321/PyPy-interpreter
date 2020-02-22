# A Python-based Python Interpreter

## Introduction

Here are many Python interpreters being used(CPython, PyPy, Jython, IronPython...). Here I select 
PyPy to achieve. The final goal of this project is providing a simple Python interpreter. The features of this interpreter will be introduced in the following part.

## Features

1. It can execute simple arithmetical and logical operations
2. It can run conditional statements and loops
3. Only print(..., (end=...)), range(), input() functions are supported(only one or two strings or variables can be printed for one time)

## Experiments

The experiments consist of eight parts.  

1. simple add, simple substract, simple multipy, simple divide: the default value are '123' and '456',
and testers can enter two value that you want to calculate.
2. if_statement: calculate the absolute value of the difference value of two value.
3. fibonacci_loop: print the 'n'th fibonacci value.
4. sum_up: sum up from '1' to 'n' that you enter.
5. combine_strings: print the combination of two strings with a space between strings.

Just type "make test" to begin the test. If you want to test your program, please type "python \_\_main\_\_.py xxx.py".

## Progress

|  Date  |                Progress                 |
| :----: | :-------------------------------------: |
| Feb 6  |      Begin building the structure       |
| Feb 7  |    Begin writing bytecode operations    |
| Feb 10 |       Begin writing the VM class        |
| Feb 13 | Begin writing the block and frame class |
| Feb 15 |             Begin debugging             |
| Feb 18 |        Preparing the experiments        |

## Acknowledgement

The design of this interpreter partly refers to Byterun by Allison Kaptur and Ned Batchelder. From Byterun, I adopted the basic
structure and principles of designing a Python interpreter.
