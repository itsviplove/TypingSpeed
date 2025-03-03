import tkinter as tk
import time


class TypingSpeedTestApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Speed Test")

        # Sample texts (you can add more)
        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Programming is the art of telling another human what one wants the computer to do.",
            "Practice makes perfect. Keep typing to improve your speed and accuracy.",
            "Python is an interpreted, high-level, general-purpose programming language.",
            "Success is not final, failure is not fatal: it is the courage to continue that counts."
        ]

        # Current sample text
        self.sample_text = self.sample_texts[0]

        # Test tracking variables
        self.test_started = False
        self.start_time = 0

        # Configure tags for styling
        self.configure_tags()

        # Create UI elements
        self.create_widgets()

    def configure_tags(self):
        # Configure tag colors for the sample text
        self.master.option_add("*TEntry*Font", "Arial 12")
        self.master.option_add("*TButton*Font", "Arial 10")

    def create_widgets(self):
        # Instructions label
        self.instructions_label = tk.Label(
            self.master,
            text="Type the following text as quickly and accurately as possible:",
            font=("Arial", 12),
            wraplength=600
        )
        self.instructions_label.pack(pady=10)

        # Sample text display (Text widget)
        self.sample_display = tk.Text(
            self.master,
            height=4,
            width=60,
            font=("Arial", 12),
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.sample_display.insert(tk.END, self.sample_text)
        self.sample_display.config(state=tk.DISABLED)
        self.sample_display.tag_configure("correct", background="lightgreen")
        self.sample_display.tag_configure("incorrect", background="salmon")
        self.sample_display.pack()

        # Input text widget
        self.input_text = tk.Text(
            self.master,
            height=6,
            width=60,
            font=("Arial", 12),
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.input_text.pack(pady=10)
        self.input_text.bind("<KeyRelease>", self.check_progress)
        self.input_text.bind("<Return>", lambda e: "break")  # Disable Enter key

        # Timer and results display
        self.stats_label = tk.Label(
            self.master,
            text="Time: 0.0s | WPM: 0 | Accuracy: 0%",
            font=("Arial", 12)
        )
        self.stats_label.pack(pady=5)

        # Reset button
        self.reset_button = tk.Button(
            self.master,
            text="Reset Test",
            command=self.reset_test,
            bg="#4CAF50",
            fg="white"
        )
        self.reset_button.pack(pady=10)

    def check_progress(self, event):
        input_text = self.input_text.get("1.0", tk.END).strip()

        # Start timer on first keystroke
        if not self.test_started and len(input_text) > 0:
            self.test_started = True
            self.start_time = time.time()
            self.update_timer()

        # Clear previous tags
        self.sample_display.config(state=tk.NORMAL)
        self.sample_display.tag_remove("correct", "1.0", tk.END)
        self.sample_display.tag_remove("incorrect", "1.0", tk.END)

        # Check each character
        for i, (input_char, sample_char) in enumerate(zip(input_text, self.sample_text)):
            start_idx = f"1.{i}"
            end_idx = f"1.{i + 1}"
            if input_char == sample_char:
                self.sample_display.tag_add("correct", start_idx, end_idx)
            else:
                self.sample_display.tag_add("incorrect", start_idx, end_idx)

        # Handle extra characters
        if len(input_text) > len(self.sample_text):
            for i in range(len(self.sample_text), len(input_text)):
                start_idx = f"1.{i}"
                end_idx = f"1.{i + 1}"
                self.sample_display.tag_add("incorrect", start_idx, end_idx)

        self.sample_display.config(state=tk.DISABLED)

        # Check if text matches completely
        if input_text == self.sample_text:
            self.show_results()

    def update_timer(self):
        if self.test_started:
            elapsed_time = time.time() - self.start_time
            self.stats_label.config(text=f"Time: {elapsed_time:.1f}s")
            self.master.after(100, self.update_timer)

    def show_results(self):
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        # Calculate WPM (words per minute)
        word_count = len(self.sample_text.split())
        minutes = elapsed_time / 60
        wpm = int(word_count / minutes) if minutes > 0 else 0

        # Calculate accuracy
        correct_chars = sum(1 for a, b in zip(self.input_text.get("1.0", tk.END).strip(), self.sample_text) if a == b)
        accuracy = (correct_chars / len(self.sample_text)) * 100

        self.stats_label.config(
            text=f"Time: {elapsed_time:.1f}s | WPM: {wpm} | Accuracy: {accuracy:.1f}%"
        )
        self.test_started = False

    def reset_test(self):
        # Reset test variables
        self.test_started = False
        self.start_time = 0

        # Clear input and update sample text
        self.input_text.delete("1.0", tk.END)
        self.sample_text = self.sample_texts[
            (self.sample_texts.index(self.sample_text) + 1) % len(self.sample_texts)]

        # Update sample display
        self.sample_display.config(state=tk.NORMAL)
        self.sample_display.delete("1.0", tk.END)
        self.sample_display.insert(tk.END, self.sample_text)
        self.sample_display.tag_remove("correct", "1.0", tk.END)
        self.sample_display.tag_remove("incorrect", "1.0", tk.END)
        self.sample_display.config(state=tk.DISABLED)

        # Reset stats label
        self.stats_label.config(text="Time: 0.0s | WPM: 0 | Accuracy: 0%")

if __name__ == "__main__":
    root = tk.Tk()
    app= TypingSpeedTestApp(root)
    root.mainloop()