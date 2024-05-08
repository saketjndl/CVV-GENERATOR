import random
import time
import tkinter as tk
from threading import Thread
from tkinter import font as tkFont

# Global variable to track cooldown and captcha
cooldown_active = False
captcha_solved = False

# Function to generate a random CVV
def generate_cvv():
    return '{:03d}'.format(random.randint(0, 999))

# Function to update the e-ink display (simulated here with a label update)
def update_display(cvv):
    cvv_label.config(text=cvv)
    # Here you would include the code to update the e-ink display

# Function to handle the cooldown logic using Tkinter's after method
def handle_cooldown(cooldown_label):
    global cooldown_active
    cooldown_active = True
    for i in range(10, 0, -1):
        cooldown_label.after(1000, lambda i=i: cooldown_label.config(text=f"Cooldown: {i}s"))
        root.update_idletasks()
        time.sleep(1)
    cooldown_label.config(text="")
    cooldown_active = False

# Function to generate a simple CAPTCHA
def generate_captcha(captcha_label):
    global captcha_solved
    captcha_solved = False
    captcha = '{:04d}'.format(random.randint(0, 9999))
    captcha_label.config(text=f"Captcha: {captcha}")
    return captcha

# Function to check the CAPTCHA input
def check_captcha(user_input, captcha_label):
    global captcha_solved
    captcha = captcha_label.cget("text").split(": ")[1]
    if user_input == captcha:
        captcha_solved = True
        captcha_label.config(text="Captcha correct. You may generate a CVV.")
    else:
        # Generate a new CAPTCHA for the user to try again
        new_captcha = generate_captcha(captcha_label)
        captcha_label.config(text=f"Captcha incorrect. New CAPTCHA: {new_captcha}")

# Function to manually generate a new CVV
def manual_generate(captcha_entry, captcha_label, cooldown_label):
    global captcha_solved
    if not cooldown_active:
        if captcha_solved:
            new_cvv = generate_cvv()
            update_display(new_cvv)
            # Start the cooldown in a separate thread
            cooldown_thread = Thread(target=handle_cooldown, args=(cooldown_label,))
            cooldown_thread.start()
            captcha_solved = False  # Reset the CAPTCHA solved status
        else:
            check_captcha(captcha_entry.get(), captcha_label)  # Check the CAPTCHA again
        captcha_entry.delete(0, 'end')  # Clear the CAPTCHA entry field
        generate_captcha(captcha_label)  # Generate a new CAPTCHA
    else:
        cooldown_label.config(text="Please wait for the cooldown.")

# Function to automatically update CVV every hour
def auto_update_cvv():
    while True:
        new_cvv = generate_cvv()
        update_display(new_cvv)
        time.sleep(3600)  # 1-hour interval

# Setting up the GUI
root = tk.Tk()
root.title("CVV Generator")
root.geometry("400x300")  # Window size
root.resizable(False, False)  # Disable resizing

# Custom fonts
cvv_font = tkFont.Font(family="Helvetica", size=24, weight="bold")
button_font = tkFont.Font(family="Helvetica", size=12)
cooldown_font = tkFont.Font(family="Helvetica", size=10, slant="italic")
captcha_font = tkFont.Font(family="Helvetica", size=14, weight="bold")

# Styling
root.configure(bg="#333333")
cvv_label = tk.Label(root, text="---", font=cvv_font, bg="#333333", fg="#4CAF50")
cvv_label.pack(pady=20)

captcha_label = tk.Label(root, text="", font=captcha_font, bg="#333333", fg="#FFFFFF")
captcha_label.pack()

captcha_entry = tk.Entry(root, font=captcha_font)
captcha_entry.pack(pady=5)

check_captcha_button = tk.Button(root, text="Check Captcha", command=lambda: check_captcha(captcha_entry.get(), captcha_label), font=button_font, bg="#555555", fg="#FFFFFF")
check_captcha_button.pack(pady=5)

cooldown_label = tk.Label(root, text="", font=cooldown_font, bg="#333333", fg="#FF0000")
cooldown_label.pack()

generate_button = tk.Button(root, text="Generate New CVV", command=lambda: manual_generate(captcha_entry, captcha_label, cooldown_label), font=button_font, bg="#555555", fg="#FFFFFF")
generate_button.pack(pady=10)

# Generate initial captcha
generate_captcha(captcha_label)

# Start the automatic CVV update in a separate thread
auto_update_thread = Thread(target=auto_update_cvv)
auto_update_thread.daemon = True
auto_update_thread.start()

# Run the GUI
root.mainloop()