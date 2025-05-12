'''
Logan Linville
typinggame_final.py
Date: 5-11-2025

The program provides the user with a typing game that will give different
difficulty phrases for the user to enter and recieve a score and wpm for
the challenge.
'''

import tkinter as tk
import time
import random
from tkinter import messagebox

start_time = [0]

# Function to start the timer when the user starts typing
def start_timer(event):
    if start_time[0] == 0:
        start_time[0] = time.time()  # Record the start time when typing begins

# Update the timer continuously
    update_timer()

# Function to start the game
def start_game():
    name = name_entry.get().strip()  # Get the name from the input field and strip any extra spaces
    if not name:
        messagebox.showerror("Missing Name", "Name field cannot be empty.")  # Show error if name is empty
    elif not name.isalpha():
        messagebox.showerror("Invalid Name", "Please enter a valid name (letters only).")  # Validate name for alphabetic input
    else:
        open_game_window()  # If name is valid, open the game window

# Function to submit the user's typing result
def submit_typing():
    end_time = time.time()  # Record the end time
    typed = input_entry.get().strip()  # Get the typed text from the entry widget
    target = target_sentence  # The target sentence to compare with

    # Accuracy calculation: compare typed text with target sentence
    correct_chars = 0
    for i in range(min(len(typed), len(target))):
        if typed[i] == target[i]:
            correct_chars += 1  # Count correct characters

    total_chars = len(typed)  # Total characters typed
    accuracy = (correct_chars / len(target)) * 100 if target else 0  # Calculate accuracy percentage

    # Time and WPM calculation: Calculate words per minute (WPM)
    elapsed_time = (end_time - start_time[0]) / 60  # Time in minutes
    word_count = len(typed.split())  # Split the typed text by spaces and count words
    wpm = word_count / elapsed_time if elapsed_time > 0 else 0  # Calculate WPM

    # Update the UI labels with calculated values
    accuracy_label.config(text=f"Accuracy: {accuracy:.2f}%")
    move_label.config(text=f"Moves: {total_chars}")
    timer_label.config(text=f"Time: {int(end_time - start_time[0])} sec")

    # Save the score to the leaderboard file
    try:
        player_name = name_entry.get().strip()
        if player_name:
            with open("leaderboard.txt", "a") as file:
                file.write(f"{player_name},{accuracy:.2f},{wpm:.2f}\n")  # Append score to leaderboard file
    except:
        pass  # If saving fails, do nothing

    # Show the results to the user in a message box
    messagebox.showinfo("Results", f"You typed:\n{typed}\n\nAccuracy: {accuracy:.2f}%\nWPM: {wpm:.2f}\nCharacters Typed: {total_chars}")



# Function to continuously update the timer label
def update_timer():
    elapsed_time = int(time.time() - start_time[0])  # Calculate elapsed time in seconds
    timer_label.config(text=f"Time: {elapsed_time} sec")  # Update the timer label
    window.after(1000, update_timer)  # Call this function again after 1000ms (1 second)

# Function to open the game window
def open_game_window():
    global input_entry, accuracy_label, move_label, timer_label, start_time, target_sentence

    try:
        # Read sentences from the file "sentences.txt"
        with open("sentences.txt", "r") as f:
            sentence_list = [line.strip() for line in f if line.strip()]  # Remove empty lines

        if not sentence_list:  # If the list is empty, show an error
            raise ValueError("Sentences file is empty.")

        target_sentence = random.choice(sentence_list)  # Randomly choose a sentence from the list
    except (FileNotFoundError, ValueError) as e:
        # If an error occurs, fall back to the default sentence
        print(f"Error loading sentences: {e}")
        target_sentence = "The quick brown fox jumps over the lazy dog."

    # Create the game window
    game_window = tk.Toplevel()
    game_window.title("Typing Challenge")
    game_window.geometry("600x500")
    game_window.resizable(False, False)

    # Display the target sentence in the game window
    tk.Label(game_window, text=target_sentence, font=("Arial", 14), wraplength=500).pack(pady=20)

    # Display the input field for the user to type
    tk.Label(game_window, text="Your Input:").pack()
    input_entry = tk.Entry(game_window, width=60)  # Create an entry field for user input
    input_entry.pack(pady=10)

    input_entry.bind("<Key>", start_timer)  # Start timer on first key press
    input_entry.bind("<Return>", lambda event: submit_typing())  # Submit on Enter

    # Initialize and display the timer label
    timer_label = tk.Label(game_window, text="Time: 0 sec")
    timer_label.pack()

    # Labels for accuracy and number of moves
    accuracy_label = tk.Label(game_window, text="Accuracy: 0%")
    accuracy_label.pack(pady=5)

    move_label = tk.Label(game_window, text="Moves: 0")
    move_label.pack(pady=5)

    # Button to submit typing
    tk.Button(game_window, text="Submit", command=submit_typing).pack(pady=10)
    # Button to return to the main menu
    tk.Button(game_window, text="Back to Menu", command=game_window.destroy).pack()

    # Display a small image at the bottom of the game window
    try:
        game_image = tk.PhotoImage(file="timer.ppm")  # Load PPM image
        image_label = tk.Label(game_window, image=game_image)
        image_label.image = game_image  # Keep a reference to avoid garbage collection
        image_label.pack(pady=10)
    except tk.TclError:
        print("Image not found or invalid format. Skipping image.")
        
# Function to view the leaderboard
def view_leaderboard():
    open_leaderboard()

# Function to exit the game
def exit_game():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        window.destroy()

# Function to open the leaderboard window
def open_leaderboard():
    leaderboard_window = tk.Toplevel()
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("400x400")
    leaderboard_window.resizable(False, False)

    # Title for the leaderboard window
    title_label = tk.Label(leaderboard_window, text="Top Scores", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Header for the leaderboard
    header = tk.Label(leaderboard_window, text="Name\tAccuracy (%)\tWPM", font=("Arial", 12, "underline"))
    header.pack()

    try:
        # Read the leaderboard file
        with open("leaderboard.txt", "r") as file:
            lines = file.readlines()

        scores = []
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 3:  # Ensure correct data format
                name, accuracy, wpm = parts
                scores.append((name, float(accuracy), float(wpm)))  # Store each score as a tuple

        # Sort scores by accuracy 
        scores.sort(key=lambda x: x[1], reverse=True)

        # Display the top 10 scores
        for name, accuracy, wpm in scores[:10]:
            entry = tk.Label(leaderboard_window, text=f"{name}\t{accuracy:.2f}\t\t{wpm:.2f}", font=("Arial", 12))
            entry.pack()

    except FileNotFoundError:
        no_data_label = tk.Label(leaderboard_window, text="No scores yet.", font=("Arial", 12))
        no_data_label.pack()

    # Close button for leaderboard window
    close_btn = tk.Button(leaderboard_window, text="Close", command=leaderboard_window.destroy)
    close_btn.pack(pady=20)

# Main window (where user enters their name and starts the game)
window = tk.Tk()
window.title("Typing Speed Challenge")
window.geometry("500x550")
window.resizable(False, False)

# Title label for the main window
title_label = tk.Label(window, text="Typing Speed Challenge", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

#Logo for main window
ppm_image = tk.PhotoImage(file="keyboard.ppm") 
image_label = tk.Label(window, image=ppm_image)
image_label.pack()

# Input field for user's name
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

# Start the Tkinter main loop
window.mainloop()
