.PHONY: all lexer

all: lexer

lexer:
	@mkdir -p ./bin
	@clang++ \
		-O3 \
		-Wall \
		-shared \
		-std=c++11 \
		-undefined dynamic_lookup \
		$(shell python3-config --includes) \
		-I../extern/pybind11/include \
		-o ./bin/lexer$(shell python3-config --extension-suffix) \
		./lexer/lexer_pybind.cpp
