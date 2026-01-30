import tkinter as tk
from tkinter import simpledialog
import random

# --- Root window ---
root = tk.Tk()
root.title("Jump for Math")
WIDTH, HEIGHT = 600, 700
root.geometry(f"{WIDTH}x{HEIGHT}")

# --- Canvas ---
canvas = tk.Canvas(root, width=WIDTH, height=600, bg="black")
canvas.pack()

# --- Settings bar ---
settings_frame = tk.Frame(root, bg="gray20", height=40)
settings_frame.pack(fill="x")

colors = ["Blue", "Red", "Green", "Pink"]
selected_color = tk.StringVar(value=colors[0])

tk.Label(settings_frame, text="Ball Color:", fg="white", bg="gray20").pack(side="left", padx=5)
tk.OptionMenu(settings_frame, selected_color, *colors).pack(side="left", padx=5)
tk.Button(settings_frame, text="Reset", command=lambda: reset_game()).pack(side="left", padx=5)

# --- Game state ---
GRAVITY = 2
JUMP_FORCE = -22
MOVE_SPEED = 6
SCROLL_LINE = 250

player = None
platforms = []
base_floor = None
y_velocity = 0
game_running = True
paused_for_math = False
move_left = False
move_right = False
platform_counter = 0
counted_platforms = set()
loop_id = None

# --- Score ---
score = 0
score_text = None

math_levels = ["+", "-", "*", "/"]
next_math_trigger = 5

# --- Player & platform functions ---
def create_base_floor():
    global base_floor
    base_floor = canvas.create_rectangle(0, 580, WIDTH, 600, fill="darkgreen")

def remove_base_floor():
    global base_floor
    if base_floor:
        canvas.delete(base_floor)
        base_floor = None

def create_player():
    global player
    player = canvas.create_oval(280, 540, 320, 580, fill=selected_color.get())

def create_platform(x, y):
    return canvas.create_rectangle(x, y, x + 100, y + 10, fill="brown")

def create_start_platforms():
    platforms.clear()
    counted_platforms.clear()
    y = 500
    for _ in range(6):
        x = random.randint(0, WIDTH - 100)
        platforms.append(create_platform(x, y))
        y -= 70

def create_score_display():
    global score_text
    score_text = canvas.create_text(
        10, 10,
        anchor="nw",
        text="Score: 0",
        fill="white",
        font=("Arial", 16)
    )

def update_player_color():
    if player:
        canvas.itemconfig(player, fill=selected_color.get())

selected_color.trace("w", lambda *args: update_player_color())

# --- Key controls ---
def key_press(event):
    global move_left, move_right, y_velocity
    if paused_for_math:
        return
    if event.keysym == "Left":
        move_left = True
    if event.keysym == "Right":
        move_right = True
    if event.keysym == "Up" and y_velocity >= 0:
        y_velocity = JUMP_FORCE

def key_release(event):
    global move_left, move_right
    if event.keysym == "Left":
        move_left = False
    if event.keysym == "Right":
        move_right = False

root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

# --- Platform collision ---
def check_platform_collision(prev_y, curr_y):
    for plat in platforms:
        x0, y0, x1, y1 = canvas.coords(plat)
        px0, _, px1, _ = canvas.coords(player)
        if px1 > x0 and px0 < x1 and prev_y <= y0 <= curr_y:
            canvas.move(player, 0, y0 - curr_y)
            return plat
    return None

# --- Reset game ---
def reset_game():
    global y_velocity, game_running, platform_counter, loop_id, next_math_trigger
    global player, platforms, counted_platforms, move_left, move_right
    global base_floor, paused_for_math, score

    if loop_id:
        root.after_cancel(loop_id)

    canvas.delete("all")

    # Reset state
    y_velocity = 0
    platform_counter = 0
    next_math_trigger = 5
    game_running = True
    paused_for_math = False
    move_left = move_right = False
    counted_platforms = set()
    platforms = []
    base_floor = None
    player = None
    score = 0
    loop_id = None

    # Recreate elements
    create_base_floor()
    create_player()
    create_start_platforms()
    create_score_display()

    # Start loop
    game_loop()

# --- Math problem ---
def show_math_problem():
    global paused_for_math
    paused_for_math = True

    level_index = min(platform_counter // 5, 3)
    op = math_levels[level_index]

    a, b = random.randint(1, 10), random.randint(1, 10)
    if op == "/":
        a = a * b

    if op == "+": answer = a + b
    if op == "-": answer = a - b
    if op == "*": answer = a * b
    if op == "/": answer = a // b

    user_input = simpledialog.askinteger(
        "Math Challenge",
        f"Solve: {a} {op} {b} = ?"
    )

    if user_input == answer:
        countdown(3)
    else:
        game_over()

# --- Countdown ---
def countdown(time_left):
    global paused_for_math, y_velocity, move_left, move_right
    canvas.delete("countdown")
    if time_left > 0:
        canvas.create_text(
            WIDTH // 2, HEIGHT // 2,
            text=str(time_left),
            font=("Arial", 48),
            fill="yellow",
            tags="countdown"
        )
        root.after(1000, lambda: countdown(time_left - 1))
    else:
        canvas.delete("countdown")
        paused_for_math = False
        y_velocity = 0
        move_left = move_right = False
        game_loop()

# --- Game loop ---
def game_loop():
    global y_velocity, platform_counter, loop_id, next_math_trigger, paused_for_math, score

    if not game_running or paused_for_math:
        return

    # Move left/right
    if move_left:
        canvas.move(player, -MOVE_SPEED, 0)
    if move_right:
        canvas.move(player, MOVE_SPEED, 0)

    # Wrap around horizontally
    px0, py0, px1, py1 = canvas.coords(player)
    if px1 < 0:
        canvas.move(player, WIDTH + (px1 - px0), 0)
    elif px0 > WIDTH:
        canvas.move(player, -(px1 - px0 + WIDTH), 0)

    # Gravity
    prev_py1 = py1
    y_velocity += GRAVITY
    canvas.move(player, 0, y_velocity)
    px0, py0, px1, py1 = canvas.coords(player)

    # Base floor collision
    if base_floor:
        bx0, by0, bx1, by1 = canvas.coords(base_floor)
        if py1 >= by0:
            canvas.move(player, 0, by0 - py1)
            y_velocity = JUMP_FORCE

    # Remove base floor
    if base_floor and py0 < SCROLL_LINE:
        remove_base_floor()

    # Platform collision
    plat = check_platform_collision(prev_py1, py1)
    if plat:
        y_velocity = JUMP_FORCE
        if plat not in counted_platforms:
            counted_platforms.add(plat)
            platform_counter += 1

            score += 10
            canvas.itemconfig(score_text, text=f"Score: {score}")

            if platform_counter >= next_math_trigger:
                next_math_trigger += 5
                show_math_problem()

    # Scroll platforms
    if py0 < SCROLL_LINE:
        diff = SCROLL_LINE - py0
        canvas.move(player, 0, diff)
        for plat in platforms:
            canvas.move(plat, 0, diff)

    # Recycle platforms
    for plat in platforms[:]:
        if canvas.coords(plat)[1] > 600:
            canvas.delete(plat)
            platforms.remove(plat)
            platforms.append(
                create_platform(
                    random.randint(0, WIDTH - 100),
                    random.randint(-60, -10)
                )
            )

    # Game over
    if py0 > 600:
        game_over()
        return

    loop_id = root.after(16, game_loop)

# --- Game over ---
def game_over():
    global game_running
    game_running = False
    canvas.create_text(
        WIDTH // 2, 300,
        text="GAME OVER\nPress Reset",
        fill="white",
        font=("Arial", 28),
        justify="center"
    )

# --- Start game ---
create_base_floor()
create_player()
create_start_platforms()
create_score_display()
game_loop()

root.mainloop()
