# tracker_gui.py  ·  Class Stock Tracker, with a window
# SOYL Future Builders · Week 2 · Sunday
#
# This app has 3 parts:
#   PART 1  The data    a dictionary: item -> quantity
#   PART 2  The engine  the same functions as tracker.py
#   PART 3  The face    a window, built with tkinter (it comes with Python)
#
# Big idea: the window never changes the stock by itself.
# Every button just CALLS a function from the engine.
#
# To run: open this file in Thonny and press F5 (Run).
# Option 1 "Show" is the chart, always on screen. Option 5 "Quit" is the Quit button.

import tkinter as tk


# ============ PART 1: THE DATA ============

stock = {"chart paper": 20, "markers": 12, "glue sticks": 8, "scissors": 6}
LOW = 5    # fewer than this many = low stock (the bar turns orange)


# ============ PART 2: THE ENGINE ============
# These are the functions from tracker.py, with ONE change:
# they RETURN their message instead of printing it.
# Why? print only shows text in the Shell. The window needs
# the answer handed back to it, so it can show the answer itself.

def find_item(stock, name):
    if name in stock:
        return f"Found: {name} = {stock[name]}"
    return f"Sorry, '{name}' is not in the stock list."


def add_item(stock, name, qty):
    if name in stock:
        return f"'{name}' is already in stock. Use Update to change it."
    stock[name] = qty
    return f"Added {name}: {qty}"


def update_item(stock, name, qty):
    if name in stock:
        old = stock[name]
        stock[name] = qty
        return f"Updated {name}: {old} -> {qty}"
    return f"Sorry, '{name}' is not in the stock list. Use Add first."


# ============ PART 3: THE FACE ============

NAVY = "#0E1B2C"
PAPER = "#F6F3EC"
CARD = "#FFFDF8"
BLUE = "#2F5BEA"
LIGHT_BLUE = "#DCE5FF"
ORANGE = "#FF8A3D"
GREY = "#4A5568"
HIGHLIGHT = "#FFE3CF"

FONT = ("Helvetica", 13)
BOLD = ("Helvetica", 13, "bold")
CODE = ("Courier", 12)


# --- Helper functions for the window ---
# (Python only runs a function when it is called, so these can use
#  widgets like chart and log that are made further down the file.)

def draw_stock(highlight=""):
    # Draws one bar per item: Option 1 "Show", but always on screen.
    chart.delete("all")
    biggest = max(stock.values())
    if biggest == 0:
        biggest = 1
    y = 16
    for name in stock:
        qty = stock[name]
        if name == highlight:
            chart.create_rectangle(8, y - 6, 532, y + 34, fill=HIGHLIGHT, outline="")
        width = qty / biggest * 260 + 4
        if qty < LOW:
            colour = ORANGE
            label = f"{qty}  LOW"
        else:
            colour = BLUE
            label = str(qty)
        chart.create_text(20, y + 14, text=name, anchor="w", font=FONT, fill=NAVY)
        chart.create_rectangle(170, y, 170 + width, y + 28, fill=colour, outline="")
        chart.create_text(180 + width, y + 14, text=label, anchor="w", font=BOLD, fill=NAVY)
        y = y + 44
    chart.config(height=y + 4)


def log_call(text):
    # Adds one line to the "Function calls" box, so we can watch the chain.
    log.insert("end", text)
    log.see("end")


def show_message(message):
    if "Sorry" in message or "already" in message:
        result.config(text=message, fg="#B5480C")
    else:
        result.config(text=message, fg=BLUE)
    log_call(f'      returned: "{message}"')


def read_name():
    name = name_box.get().strip().lower()
    if name == "":
        result.config(text="Type an item name first.", fg="#B5480C")
    return name


def read_qty():
    # No while loop needed here: the window simply waits for the next click.
    text = qty_box.get().strip()
    if not text.isdigit():
        result.config(text="Please type a whole number, like 3.", fg="#B5480C")
        return None
    return int(text)


# --- What each button does ---

def on_find():
    name = read_name()
    if name == "":
        return
    log_call("Find clicked  ->  on_find()")
    log_call(f"   calls find_item(stock, '{name}')")
    message = find_item(stock, name)
    show_message(message)
    log_call("   calls draw_stock()")
    draw_stock(name)


def on_add():
    name = read_name()
    qty = read_qty()
    if name == "" or qty is None:
        return
    log_call("Add clicked  ->  on_add()")
    log_call(f"   calls add_item(stock, '{name}', {qty})")
    message = add_item(stock, name, qty)
    show_message(message)
    log_call("   calls draw_stock()")
    draw_stock(name)


def on_update():
    name = read_name()
    qty = read_qty()
    if name == "" or qty is None:
        return
    log_call("Update clicked  ->  on_update()")
    log_call(f"   calls update_item(stock, '{name}', {qty})")
    message = update_item(stock, name, qty)
    show_message(message)
    log_call("   calls draw_stock()")
    draw_stock(name)


# --- Build the window ---

root = tk.Tk()
root.title("Class Stock Tracker")
root.configure(bg=PAPER)

top = tk.Frame(root, bg=NAVY, padx=24, pady=16)
top.pack(fill="x")
tk.Label(top, text="Class Stock Tracker", font=("Helvetica", 22, "bold"),
         bg=NAVY, fg="#F3EFE6").pack(anchor="w")
tk.Label(top, text="Week 2 · every button calls a function from the engine",
         font=FONT, bg=NAVY, fg=ORANGE).pack(anchor="w")

body = tk.Frame(root, bg=PAPER, padx=20, pady=16)
body.pack(fill="both", expand=True)

# Left card: the stock chart
left = tk.Frame(body, bg=CARD, padx=12, pady=12)
left.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
tk.Label(left, text="STOCK", font=BOLD, bg=CARD, fg=GREY).pack(anchor="w")
chart = tk.Canvas(left, width=540, height=200, bg=CARD, highlightthickness=0)
chart.pack()

# Right card: inputs and buttons
right = tk.Frame(body, bg=CARD, padx=20, pady=16)
right.grid(row=0, column=1, sticky="nsew")
tk.Label(right, text="Item name", font=BOLD, bg=CARD, fg=NAVY).pack(anchor="w")
name_box = tk.Entry(right, font=FONT, width=22)
name_box.pack(anchor="w", pady=(4, 12))
tk.Label(right, text="Quantity", font=BOLD, bg=CARD, fg=NAVY).pack(anchor="w")
qty_box = tk.Entry(right, font=FONT, width=8)
qty_box.pack(anchor="w", pady=(4, 16))

buttons = tk.Frame(right, bg=CARD)
buttons.pack(anchor="w")
tk.Button(buttons, text="Find", command=on_find, font=BOLD, width=7,
          bg=LIGHT_BLUE, fg=NAVY).grid(row=0, column=0, padx=(0, 8))
tk.Button(buttons, text="Add", command=on_add, font=BOLD, width=7,
          bg=ORANGE, fg=NAVY).grid(row=0, column=1, padx=(0, 8))
tk.Button(buttons, text="Update", command=on_update, font=BOLD, width=7,
          bg=ORANGE, fg=NAVY).grid(row=0, column=2)

result = tk.Label(right, text="Type a name, then click a button.", font=BOLD,
                  bg=CARD, fg=GREY, wraplength=320, justify="left")
result.pack(anchor="w", pady=(18, 8))

tk.Button(right, text="Quit", command=root.destroy, font=FONT,
          fg=NAVY).pack(anchor="w", pady=(8, 0))

# Bottom: watch the functions call each other
bottom = tk.Frame(root, bg=PAPER, padx=20)
bottom.pack(fill="both", expand=True, pady=(0, 20))
tk.Label(bottom, text="FUNCTION CALLS  (newest at the bottom)", font=BOLD,
         bg=PAPER, fg=GREY).pack(anchor="w")
log_card = tk.Frame(bottom, bg="#16283F", padx=14, pady=10)
log_card.pack(fill="both", expand=True)
log = tk.Listbox(log_card, font=CODE, height=8, bg="#16283F", fg="#E6EDF7",
                 borderwidth=0, highlightthickness=0)
log.pack(fill="both", expand=True)

draw_stock()
root.mainloop()