all: mkcells.py

mkcells.py: mkcells.c mkcells.h
	gcc -std=c99 -Werror -g -fPIC -c mkcells.c -Wall
	gcc -shared  -o libmkcells.so mkcells.o -lc
	./ctypesgen-read-only/ctypesgen.py -l libmkcells.so mkcells.h > mkcells.py

clean:
	rm mkcells.py
