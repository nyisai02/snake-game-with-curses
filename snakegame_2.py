import curses
import random
import time

WINDOW_WIDTH = 70
WINDOW_HEIGHT = 20
FOOD_DURATION = 5  # Food disappears after 5 seconds

curses.initscr()
win = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

snake = [(4, 4), (4, 3), (4, 2)]
foods = [(6, 6), (10, 10)]  # Initialize with two food items
food_timers = [time.time() + FOOD_DURATION for _ in range(len(foods))]
key = curses.KEY_RIGHT
ESC = 27
score = 0

def generate_food():
    while True:
        food = (random.randint(1, WINDOW_HEIGHT - 2), random.randint(1, WINDOW_WIDTH - 2))
        if food not in snake and food not in foods:
            return food

# Initial food placement
for food in foods:
    win.addch(food[0], food[1], '#')

while key != ESC:
    win.addstr(0, 2, f'Score {score}')
    win.timeout(150 - len(snake) // 5 + len(snake) // 10 % 120)
    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key

    check_list = [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]
    if key not in check_list:
        key = prev_key

    y, x = snake[0]
    if key == curses.KEY_RIGHT:
        x += 1
    elif key == curses.KEY_LEFT:
        x -= 1
    elif key == curses.KEY_DOWN:
        y += 1
    elif key == curses.KEY_UP:
        y -= 1

    snake.insert(0, (y, x))

    if y == 0 or y == WINDOW_HEIGHT - 1:
        break
    if x == 0 or x == WINDOW_WIDTH - 1:
        break

    if snake[0] in snake[1:]:
        break

    for i, food in enumerate(foods):
        if snake[0] == food:
            score += 1
            foods.remove(food)
            food_timers.pop(i)
            food = generate_food()
            foods.append(food)
            food_timers.append(time.time() + FOOD_DURATION)
            win.addch(food[0], food[1], '#')
            break
    else:
        last = snake.pop()
        win.addch(last[0], last[1], ' ')

    win.addch(snake[0][0], snake[0][1], "*")

    for s in snake[1:]:
        win.addch(s[0], s[1], "*")

    # Check if any food has expired
    current_time = time.time()
    for i, timer in enumerate(food_timers):
        if current_time >= timer:
            food_timers.pop(i)
            foods.pop(i)
            food = generate_food()
            foods.append(food)
            food_timers.append(time.time() + FOOD_DURATION)
            win.addch(food[0], food[1], '#')

curses.endwin()
print(f'Your final score is {score}')
