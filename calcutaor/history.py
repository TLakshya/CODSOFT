
import os

HISTORY_FILE = "calculator_history.txt"

class HistoryManager:
    def __init__(self):
        self.history = []
        self.load_history()

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as file:
                self.history = [line.strip() for line in file.readlines()]

    def save_history(self):
        with open(HISTORY_FILE, "w") as file:
            for entry in self.history:
                file.write(entry + "\n")

    def add_entry(self, entry):
        self.history.append(entry)
        self.save_history()