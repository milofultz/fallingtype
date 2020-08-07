import random
import string
import time

from blessed import Terminal


TERM = Terminal()

WIDTH = TERM.width
HEIGHT = TERM.height

WORDS_FILE = '/usr/share/dict/web2'


def word_list_handler(filename=WORDS_FILE):
    word_lst = []

    with open(filename, 'r') as words:
        for word in words:
            word_lst.append(word.strip())

    return word_lst

def word_picker(lst, length):
    while True:
        word = random.choice(lst)
        if length-1 <= len(word) <= length+1:
            return word

def display(word, word_x, word_y, bottom):
    # print the word
    print(TERM.clear,
          TERM.move_xy(word_x, word_y),
          TERM.bold(word))
    # print the bottom layer
    print(TERM.move_xy(0, bottom),
          TERM.red("^ " * ((WIDTH-2)//2)))

def bang():
    # print(TERM.location(0,0))
    color_list = [TERM.on_bright_white,
                  TERM.on_white,
                  TERM.on_bright_black,
                  TERM.on_black]
    for i in color_list:
        print(i, TERM.clear)
        time.sleep(.04)

def game(word_lst):
    speed = 0.75
    length = 5
    bottom = TERM.height-1
    after, before = 0, 0
    word_x, word_y = 0, 0
    word = ''
    count = 0

    # Game loop
    while word_y < bottom:
        # If the amount of time for type to fall elapses
        if after - before > speed:
            # set before time stamp
            before = time.time()
            # lower word
            word_y += 1
        # if word has been completed or it's the first word,
        # start a new word and bring the bottom bar up
        if not word:
            word = word_picker(word_lst, length)
            margin = len(word) + 1
            word_x, word_y = random.randint(1, WIDTH-margin), 0
            if count < HEIGHT//2:
                bottom -= 1
                count += 1
            # if it's time to level up, reset the counter, add to the
            # complexity of the words, reset the bottom bar, and speed up
            else:
                count = 0
                length += 2
                bottom = TERM.height-2
                speed = speed*.66

        # display the word on screen
        display(word, word_x, word_y, bottom)

        # take input
        with TERM.hidden_cursor(), TERM.cbreak():
            inp = TERM.inkey(timeout=after-before)
            if inp:
                if word[0] == inp:
                    word = word[1:]
                else:
                    bang()
                    word = random.choice(string.ascii_letters) + word

        # set after timestamp
        after = time.time()

    # losing screen
    bang()
    with TERM.hidden_cursor():
        print(TERM.clear,
              TERM.move_xy(0, HEIGHT//2),
              TERM.center(TERM.bright_white("YOU LOSE")),
              TERM.move_xy(0, HEIGHT))
        time.sleep(1.25)

if __name__ == '__main__':
    word_lst = word_list_handler(WORDS_FILE)
    game(word_lst)