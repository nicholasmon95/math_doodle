import tkinter as tk
import tkinter.ttk as ttk

root = tk.Tk()
root.title("Jump for Math")

# User settings dictionary 
users_settings = {"color": None, "difficulty": None}

# --- List of colors ---
colors = ["Red", "Blue", "Green", "Pink"]

# --- Tkinter variable to store selected color ---
selected_color = tk.StringVar()
selected_color.set(colors[0])  # Default value
users_settings["color"] = selected_color.get()  # Save default

# --- Create Canvas ---
canvas = tk.Canvas(root, width=150, height=150, bg="black")
canvas.pack(pady=20)

# --- Draw character (ball) ---
ball = canvas.create_oval(60, 10, 90, 40, fill=selected_color.get(), outline="black")

# --- Function to change ball color ---
def change_ball_color(*args):
    color = selected_color.get()
    users_settings["color"] = color
    canvas.itemconfig(ball, fill=color)  # Change the fill of the oval
    print(f"Ball color changed to: {color}")

# --- Color dropdown ---
dropdown = tk.OptionMenu(root, selected_color, *colors)
dropdown.pack(pady=10)

# Link the function to the variable
selected_color.trace("w", change_ball_color)

# --- Difficulty dropdown ---
difficulty_options = ["Easy", "Hard"]
difficulty_combo = ttk.Combobox(root, values=difficulty_options, state="readonly")
difficulty_combo.current(0)  # Default selection
users_settings["difficulty"] = difficulty_combo.get()  # Save default

def difficulty_selected(event):
    users_settings["difficulty"] = difficulty_combo.get()
    print(f"Difficulty selected: {users_settings['difficulty']}")

difficulty_combo.bind("<<ComboboxSelected>>", difficulty_selected)
difficulty_combo.pack(pady=20)

# --- Start game button ---
def start_game():
    print("Game Started with settings:")
    print(users_settings)
    # Here you can pass users_settings to your game logic

start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack(pady=10)

# --- Exit game button ---
def exit_game():
    root.quit()

exit_button = tk.Button(root, text="Exit Game", command=exit_game)
exit_button.pack(pady=10)

# --- Set window size and center ---
window_width = 1000
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.mainloop()
