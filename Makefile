MAIN = Interpreter/__main__.py

VPATH = tests: Interpreter

.PHONY: test add substract multipy divide if loop sum_up combine
test: add substract multipy divide if loop sum_up combine

add: $(MAIN) simple_add.py
	python $(MAIN) tests/simple_add.py

substract: $(MAIN) simple_substract.py
	python $(MAIN) tests/simple_substract.py

multipy: $(MAIN) simple_multipy.py
	python $(MAIN) tests/simple_multipy.py

divide: $(MAIN) simple_divide.py
	python $(MAIN) tests/simple_divide.py

if: $(MAIN) if_statement.py
	python $(MAIN) tests/if_statement.py

loop: $(MAIN) fibonacci_loop.py
	python $(MAIN) tests/fibonacci_loop.py

sum_up: $(MAIN) sum_up.py
	python $(MAIN) tests/sum_up.py

combine: $(MAIN) combine_strings.py
	python $(MAIN) tests/combine_strings.py
