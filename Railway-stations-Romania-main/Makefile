CC = gcc
CFLAGS = -Wall -Wextra -std=gnu99 -g

build: exersare5

exersare5: main.c functii.h functii.c
	$(CC) $(CFLAGS) -o $@ $^

run:
	./exersare5

clean:
	rm -f exersare5
