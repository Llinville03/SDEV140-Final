'''
Logan Linville
typinggame_final.py
Date: 4-23-2025

The program provides the user with a typing game that will give different
difficulty phrases for the user to enter and recieve a score and wpm for
the challenge.
'''

import tkinter as tk
from tkinter import messagebox
import time

# Starts the game after validating the name input
def start_game():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Missing Name", "Name field cannot be empty.")
    elif not name.isalpha():
        messagebox.showerror("Invalid Name", "Please enter a valid name (letters only).")
    else:
        open_game_window()

# Opens the leaderboard window
def view_leaderboard():
    open_leaderboard()

# Exits the application with confirmation
def exit_game():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        window.destroy()

# Opens a new window to display the leaderboard
def open_leaderboard():
    leaderboard_window = tk.Toplevel()
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("400x300")
    leaderboard_window.resizable(False, False)

    title_label = tk.Label(leaderboard_window, text="Top Scores", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    header = tk.Label(leaderboard_window, text="Name\tAccuracy (%)\tWPM", font=("Arial", 12, "underline"))
    header.pack()

    try:
        with open("leaderboard.txt", "r") as file:
            lines = file.readlines()

        scores = []
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 3:
                name, accuracy, wpm = parts
                scores.append((name, float(accuracy), float(wpm)))

        scores.sort(key=lambda x: x[1], reverse=True)

        for name, accuracy, wpm in scores[:10]:
            entry = tk.Label(leaderboard_window, text=f"{name}\t{accuracy:.2f}\t\t{wpm:.2f}", font=("Arial", 12))
            entry.pack()

    except FileNotFoundError:
        no_data_label = tk.Label(leaderboard_window, text="No scores yet.", font=("Arial", 12))
        no_data_label.pack()

    close_btn = tk.Button(leaderboard_window, text="Close", command=leaderboard_window.destroy)
    close_btn.pack(pady=20)

# Sets up the main application window
window = tk.Tk()
window.title("Typing Speed Challenge")
window.geometry("500x400")
window.resizable(False, False)

# Sets the main timer start point
start_time = [0]

# Opens the typing game window
def open_game_window():
    game_window = tk.Toplevel()
    game_window.title("Typing Speed Challenge - LETS PLAY")
    game_window.geometry("600x400")
    game_window.resizable(False, False)

    target_sentence = "The quick brown fox jumps over the lazy dog."

    sentence_label = tk.Label(game_window, text=target_sentence, font=("Arial", 14), wraplength=500)
    sentence_label.pack(pady=20)

    entry_label = tk.Label(game_window, text="Your Input:")
    entry_label.pack()

    input_entry = tk.Entry(game_window, width=60)
    input_entry.pack(pady=10)
    input_entry.bind("<Return>", lambda event: submit_typing(input_entry, game_window))

    timer_label = tk.Label(game_window, text="Time: 00:00")
    timer_label.pack(pady=5)

    accuracy_label = tk.Label(game_window, text="Accuracy: 0%")
    accuracy_label.pack(pady=5)

    move_label = tk.Label(game_window, text="Moves: 0")
    move_label.pack(pady=5)

    # Starts the timer when typing begins
    def start_timer(event):
        if start_time[0] == 0:
            start_time[0] = time.time()

    input_entry.bind("<Key>", start_timer)

# Submits the user's typing, calculates stats, and shows results
def submit_typing(input_entry, game_window):
    end_time = time.time()
    typed = input_entry.get().strip()
    target = "The quick brown fox jumps over the lazy dog."

    correct_chars = 0
    for i in range(min(len(typed), len(target))):
        if typed[i] == target[i]:
            correct_chars += 1

    total_chars = len(typed)
    accuracy = (correct_chars / len(target)) * 100 if target else 0

    elapsed_time = (end_time - start_time[0]) / 60
    word_count = len(typed.split())
    wpm = word_count / elapsed_time if elapsed_time > 0 else 0

    try:
        player_name = name_entry.get().strip()
        if player_name:
            with open("leaderboard.txt", "a") as file:
                file.write(f"{player_name},{accuracy:.2f},{wpm:.2f}\n")
    except Exception as e:
        print(f"Error saving score: {e}")

    messagebox.showinfo("Results", f"You typed:\n{typed}\n\nAccuracy: {accuracy:.2f}%\nWPM: {wpm:.2f}\nCharacters Typed: {total_chars}")

# Sets the app title and welcome interface
title_label = tk.Label(window, text="Typing Speed Challenge", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

# Placeholder for game logo
image_label = tk.Label(window, text="[Typing Game Logo]", font=("Times New Roman", 12, "italic"))
image_label.pack()

# Name entry field
name_label = tk.Label(window, text="Enter Your Name:")
name_label.pack(pady=5)

name_entry = tk.Entry(window, width=30)
name_entry.pack(pady=5)

# Start button
start_button = tk.Button(window, text="Start Game", command=start_game, width=20)
start_button.pack(pady=10)

# Leaderboard button
leaderboard_button = tk.Button(window, text="Leaderboard", command=view_leaderboard, width=20)
leaderboard_button.pack(pady=5)

# Exit button
exit_button = tk.Button(window, text="Exit", command=exit_game, width=20)
exit_button.pack(pady=20)

# Starts the main event loop
window.mainloop()
