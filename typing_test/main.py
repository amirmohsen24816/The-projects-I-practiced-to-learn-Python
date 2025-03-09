import tkinter as tk
from tkinter import messagebox
import time
import random
import sqlite3
from datetime import datetime

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Initialize database
        self.init_database()

        # Sample texts
        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog. This pangram contains every letter of the English alphabet at least once.",
            "Programming is the art of telling another human what one wants the computer to do. It's about thinking clearly and solving problems.",
            "In the end, we will remember not the words of our enemies, but the silence of our friends. Life's most persistent question is: What are you doing for others?",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. Never give up on something that you can't go a day without thinking about.",
            "Technology is best when it brings people together. The advance of technology is based on making it fit in so that you don't really even notice it.",
            "Life is like riding a bicycle. To keep your balance, you must keep moving forward. The only way to do great work is to love what you do.",
            "Education is not preparation for life; education is life itself. The function of education is to teach one to think intensively and to think critically.",
            "The only limit to our realization of tomorrow will be our doubts of today. Let us move forward with strong and active faith.",
            "The future belongs to those who believe in the beauty of their dreams. Success is not the key to happiness. Happiness is the key to success.",
            "Innovation distinguishes between a leader and a follower. Stay hungry, stay foolish. Your time is limited, don't waste it living someone else's life."
        ]
        
        self.current_text = ""
        self.start_time = None
        self.test_started = False
        self.remaining_time = 60  # 60 seconds timer
        self.timer_id = None

        # Create GUI elements
        self.create_widgets()

    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect('typing_results.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                wpm INTEGER,
                accuracy INTEGER,
                time_taken REAL,
                text_length INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        # Timer label
        self.timer_label = tk.Label(
            self.root,
            text="Time: 60s",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        self.timer_label.pack(pady=5)

        # Instructions
        self.instructions = tk.Label(
            self.root,
            text="Type the text below as fast as you can!\nYou have 60 seconds.\nPress Start when ready.",
            font=("Arial", 12),
            bg="#f0f0f0",
            pady=10
        )
        self.instructions.pack()

        # Sample text display
        self.text_display = tk.Text(
            self.root,
            height=5,
            width=60,
            font=("Arial", 12),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#ffffff",
            pady=10,
            padx=10
        )
        self.text_display.pack(pady=20)

        # Input field
        self.input_field = tk.Text(
            self.root,
            height=5,
            width=60,
            font=("Arial", 12),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#ffffff",
            pady=10,
            padx=10
        )
        self.input_field.pack(pady=20)

        # Buttons frame
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=10)

        # Start button
        self.start_button = tk.Button(
            self.button_frame,
            text="Start",
            command=self.start_test,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            width=10
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Reset button
        self.reset_button = tk.Button(
            self.button_frame,
            text="Reset",
            command=self.reset_test,
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            width=10,
            state=tk.DISABLED
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # View History button
        self.history_button = tk.Button(
            self.button_frame,
            text="History",
            command=self.show_history,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            width=10
        )
        self.history_button.pack(side=tk.LEFT, padx=5)

        # Results label
        self.results_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            pady=10
        )
        self.results_label.pack()

    def update_timer(self):
        """Update the timer display"""
        if self.test_started and self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.config(text=f"Time: {self.remaining_time}s")
            self.timer_id = self.root.after(1000, self.update_timer)
            
            if self.remaining_time == 0:
                self.complete_test(timeout=True)

    def start_test(self):
        self.test_started = True
        self.start_time = time.time()
        self.remaining_time = 60
        self.current_text = random.choice(self.sample_texts)
        
        # Update display
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(1.0, self.current_text)
        self.text_display.config(state=tk.DISABLED)
        
        # Enable input field
        self.input_field.config(state=tk.NORMAL)
        self.input_field.delete(1.0, tk.END)
        self.input_field.focus()
        
        # Update buttons
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)
        self.history_button.config(state=tk.DISABLED)
        
        # Start timer
        self.update_timer()
        
        # Bind the key release event
        self.input_field.bind('<KeyRelease>', self.check_progress)

    def reset_test(self):
        self.test_started = False
        self.start_time = None
        self.current_text = ""
        self.remaining_time = 60
        
        # Cancel timer if running
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        # Reset timer display
        self.timer_label.config(text="Time: 60s")
        
        # Reset display
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.config(state=tk.DISABLED)
        
        # Reset input field
        self.input_field.config(state=tk.DISABLED)
        self.input_field.delete(1.0, tk.END)
        
        # Reset buttons
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.history_button.config(state=tk.NORMAL)
        
        # Reset results
        self.results_label.config(text="")

    def check_progress(self, event=None):
        if not self.test_started:
            return

        # Get current input
        current_input = self.input_field.get(1.0, tk.END).strip()
        
        # Check if the test is complete
        if current_input == self.current_text:
            self.complete_test()
        else:
            # Check for mistakes
            for i, (char1, char2) in enumerate(zip(current_input, self.current_text)):
                if char1 != char2:
                    self.input_field.tag_add("wrong", f"1.{i}", f"1.{i+1}")
                    self.input_field.tag_config("wrong", foreground="red")
                    break

    def complete_test(self, timeout=False):
        # Cancel timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        end_time = time.time()
        time_taken = end_time - self.start_time
        
        # Get typed text
        typed_text = self.input_field.get(1.0, tk.END).strip()
        
        # Calculate words per minute
        if timeout:
            words = len(typed_text.split())
        else:
            words = len(self.current_text.split())
            
        wpm = round((words / time_taken) * 60)
        
        # Calculate accuracy
        total_chars = len(self.current_text)
        correct_chars = sum(1 for i, j in zip(typed_text, self.current_text) if i == j)
        accuracy = round((correct_chars / total_chars) * 100)
        
        # Save results to database
        self.save_result(wpm, accuracy, time_taken, len(self.current_text))
        
        # Display results
        result_text = f"Speed: {wpm} WPM\nAccuracy: {accuracy}%"
        self.results_label.config(text=result_text)
        
        # Disable input field
        self.input_field.config(state=tk.DISABLED)
        
        # Enable history button
        self.history_button.config(state=tk.NORMAL)
        
        # Show completion message
        message = f"Test completed!\n\nYour typing speed: {wpm} WPM\nAccuracy: {accuracy}%\nTime taken: {round(time_taken, 1)} seconds\n"
        if wpm < 40:
            message += "\nKeep practicing to improve your speed!"
        elif wpm < 60:
            message += "\nGood job! You're at an average typing speed."
        else:
            message += "\nExcellent! You're above average!"
            
        messagebox.showinfo("Test Complete", message)

    def save_result(self, wpm, accuracy, time_taken, text_length):
        """Save test results to database"""
        conn = sqlite3.connect('typing_results.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO results (date, wpm, accuracy, time_taken, text_length)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            wpm,
            accuracy,
            time_taken,
            text_length
        ))
        conn.commit()
        conn.close()

    def show_history(self):
        """Show typing test history"""
        conn = sqlite3.connect('typing_results.db')
        c = conn.cursor()
        c.execute('SELECT date, wpm, accuracy, time_taken FROM results ORDER BY date DESC LIMIT 10')
        results = c.execute('SELECT date, wpm, accuracy, time_taken FROM results ORDER BY date DESC LIMIT 10').fetchall()
        conn.close()

        history_window = tk.Toplevel(self.root)
        history_window.title("Typing Test History")
        history_window.geometry("600x400")
        history_window.configure(bg="#f0f0f0")

        # Create header
        tk.Label(
            history_window,
            text="Recent Results (Last 10 Tests)",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            pady=10
        ).pack()

        # Create table
        table_frame = tk.Frame(history_window, bg="#ffffff")
        table_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Headers
        headers = ["Date", "WPM", "Accuracy", "Time (s)"]
        for col, header in enumerate(headers):
            tk.Label(
                table_frame,
                text=header,
                font=("Arial", 12, "bold"),
                bg="#ffffff",
                padx=10,
                pady=5
            ).grid(row=0, column=col, sticky="w")

        # Results
        for row, result in enumerate(results, start=1):
            date, wpm, accuracy, time_taken = result
            tk.Label(
                table_frame,
                text=date,
                font=("Arial", 10),
                bg="#ffffff",
                padx=10,
                pady=3
            ).grid(row=row, column=0, sticky="w")
            tk.Label(
                table_frame,
                text=str(wpm),
                font=("Arial", 10),
                bg="#ffffff",
                padx=10,
                pady=3
            ).grid(row=row, column=1, sticky="w")
            tk.Label(
                table_frame,
                text=f"{accuracy}%",
                font=("Arial", 10),
                bg="#ffffff",
                padx=10,
                pady=3
            ).grid(row=row, column=2, sticky="w")
            tk.Label(
                table_frame,
                text=f"{round(time_taken, 1)}",
                font=("Arial", 10),
                bg="#ffffff",
                padx=10,
                pady=3
            ).grid(row=row, column=3, sticky="w")

def main():
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()

if __name__ == "__main__":
    main()