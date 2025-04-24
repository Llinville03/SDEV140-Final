import tkinter as tk
from tkinter import messagebox


def start_game():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Missing Name", "Name field cannot be empty.")
    elif not name.isalpha():
        messagebox.showerror("Invalid Name", "Please enter a valid name (letters only).")
    else:
        open_game_window()

def view_leaderboard():
    messagebox.showinfo("Leaderboard", "Leaderboard feature coming soon!")

def exit_game():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        window.destroy()

'''
Logan Linville
typinggame_final.py
Date: 4-23-2025

The program provides the user with a typing game that will give different
difficulty phrases for the user to enter and recieve a score and wpm for
the challenge.
'''

# Main window
window = tk.Tk()
window.title("Typing Speed Challenge")
window.geometry("500x400")
window.resizable(False, False)

# Title 
title_label = tk.Label(window, text="Typing Speed Challenge", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

# Game Logo (main)
image_label = tk.Label(window, text="[Typing Game Logo]", font=("Times New Roman", 12, "italic"))
image_label.pack()

# Name entry (main)
name_label = tk.Label(window, text="Enter Your Name:")
name_label.pack(pady=5)
name_entry = tk.Entry(window, width=30)
name_entry.pack(pady=5)



# Main menu buttons
start_button = tk.Button(window, text="Start Game", command=start_game, width=20)
start_button.pack(pady=10)

leaderboard_button = tk.Button(window, text="Leaderboard", command=view_leaderboard, width=20)
leaderboard_button.pack(pady=5)

exit_button = tk.Button(window, text="Exit", command=exit_game, width=20)
exit_button.pack(pady=20)



def open_game_window():
    window = tk.Toplevel()
    window.title("Typing Challenge - Level: Easy")
    window.geometry("600x400")
    window.resizable(False, False)

    target_sentence = "The quick brown fox jumps over the lazy dog."

    sentence_label = tk.Label(window, text=target_sentence, font=("Arial", 14), wraplength=500)
    sentence_label.pack(pady=20)

    entry_label = tk.Label(window, text="Your Input:")
    entry_label.pack()
    input_entry = tk.Entry(window, width=60)
    input_entry.pack(pady=10)

    timer_label = tk.Label(window, text="Time: 00:00")
    timer_label.pack(pady=5)

    accuracy_label = tk.Label(window, text="Accuracy: 0%")
    accuracy_label.pack(pady=5)

    move_label = tk.Label(window, text="Moves: 0")
    move_label.pack(pady=5)

    def submit_typing():
        typed = input_entry.get().strip()
        target = target_sentence

        correct_chars = 0
        for i in range(min(len(typed), len(target))):
            if typed[i] == target[i]:
                correct_chars += 1

        total_chars = len(typed)
        accuracy = (correct_chars / len(target)) * 100 if target else 0

        # Update labels
        accuracy_label.config(text=f"Accuracy: {accuracy:.2f}%")
        move_label.config(text=f"Moves: {total_chars}")

        messagebox.showinfo("Results", f"You typed:\n{typed}\n\nAccuracy: {accuracy:.2f}%\nCharacters Typed: {total_chars}")

    submit_button = tk.Button(window, text="Submit", command=submit_typing)
    submit_button.pack(pady=10)

    def back_to_menu():
        window.destroy()

    main_menu_button = tk.Button(window, text="Main Menu", command=back_to_menu)
    main_menu_button.pack()

 
window.mainloop()
