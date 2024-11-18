import curses
import random

WINDOW_WIDTH = 70
WINDOW_HEIGHT = 20

curses.initscr()
win = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

snake = [(4, 4), (4, 3), (4, 2)]
food = (6, 6)
key = curses.KEY_RIGHT
suc = 30
score = 0

while key != suc : 
    win.addstr(0, 2, f'Score {score}')
    win.timeout(150 - len(snake) // 5 + len(snake) // 10 % 120)  # This is a formula
    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key

    check_list = [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]
    if key not in check_list:
        key = prev_key

    y, x = snake[0]
    if key == curses.KEY_RIGHT:
        x += 1
        snake[0] = (y, x, '>')
    elif key == curses.KEY_LEFT:
        x -= 1
        snake[0] = (y, x, '<')
    elif key == curses.KEY_DOWN:
        y += 1
        snake[0] = (y, x, 'v')
    elif key == curses.KEY_UP:
        y -= 1
        snake[0] = (y, x, '^')

    snake.insert(0, (y, x))

    if y == 0 or y == WINDOW_HEIGHT - 1:
        break
    if x == 0 or x == WINDOW_WIDTH - 1:
        break

    if snake[0] in snake[1:]:
        break

    if snake[0] == food:
        score += 1
        food = ()
        while food == ():
            food = (random.randint(1, WINDOW_HEIGHT - 2), random.randint(1, WINDOW_WIDTH - 2))
            if food in snake:
                food = ()
        win.addch(food[0], food[1], '#')
    else:
        last = snake.pop()
        win.addch(last[0], last[1], ' ')

    win.addch(snake[0][0], snake[0][1], "*")

    for s in snake[1:]:
        win.addch(s[0], s[1], "*")
    win.addch(food[0], food[1], '#')

curses.endwin()
print(f'Your final score is {score}')
