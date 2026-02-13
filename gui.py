import tkinter as tk
from tkinter import ttk, messagebox
import sys
import subprocess # Restored
import json
import os
import random

# Suppress macOS Tk warning
os.environ['TK_SILENCE_DEPRECATION'] = '1'

def get_base_dir():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Use absolute path for data directory
BASE_DIR = get_base_dir()
DATA_DIR = os.path.join(BASE_DIR, "data")
PROGRESS_FILE = os.path.join(DATA_DIR, "user_progress.json")

class JapaneseLearningApp:
    def __init__(self, root):
        print("Initializing App...")
        self.root = root
        self.root.title("Japanese Learning App")
        self.root.geometry("600x500")
        
        # Apply theme for macOS compatibility
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except tk.TclError:
            pass
            
        try:
            self.full_vocab_data = [] 
            self.quiz_pool = []       
            self.current_word = None
            self.progress_data = self.load_progress()
            self.current_level = "n5" 
            
            self.create_widgets()
            print("Widgets created.")
            
            self.load_level_data(self.current_level)
            print(f"Level data loaded. Words: {len(self.full_vocab_data)}")
            
            # Force window to top (macOS fix)
            self.root.lift()
            self.root.attributes('-topmost', True)
            self.root.after_idle(self.root.attributes, '-topmost', False)
            
        except Exception as e:
            print(f"Error during initialization: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Initialization Error", f"An error occurred:\n{e}")

    def load_progress(self):
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_progress(self):
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.progress_data, f, ensure_ascii=False, indent=2)

    def load_level_data(self, level):
        file_path = os.path.join(DATA_DIR, f"vocab_{level}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.full_vocab_data = json.load(f)
                self.quiz_pool = self.full_vocab_data.copy() # Start with all words
                
            self.update_review_list()
            self.next_question()
        else:
            messagebox.showerror("Error", f"Data file for {level} not found!")
            self.full_vocab_data = []
            self.quiz_pool = []

    def create_widgets(self):
        # Top Bar: Level Selection
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")
        
        ttk.Label(top_frame, text="Level:").pack(side="left")
        self.level_var = tk.StringVar(value="n5")
        level_combo = ttk.Combobox(top_frame, textvariable=self.level_var, values=["n5"], state="readonly", width=5)
        level_combo.pack(side="left", padx=5)
        level_combo.bind("<<ComboboxSelected>>", self.on_level_change)
        
        # Main Tab Control
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tab 1: Learning (Quiz)
        self.learn_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.learn_frame, text="Learning")
        
        self.create_learning_tab()
        
        # Tab 2: Review (Notepad)
        self.review_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.review_frame, text="Review (Notepad)")
        
        self.create_review_tab()

    def create_learning_tab(self):
        # Question Section
        self.word_label = ttk.Label(self.learn_frame, text="", font=("Arial", 48, "bold"))
        self.word_label.pack(pady=(20, 10))
        
        # Audio Button
        self.audio_btn = ttk.Button(self.learn_frame, text="🔊 Listen", command=self.play_audio)
        self.audio_btn.pack(pady=(0, 10))
        
        self.reading_label = ttk.Label(self.learn_frame, text="", font=("Arial", 24))
        self.reading_label.pack(pady=(0, 30))
        
        # Input Section
        input_frame = ttk.Frame(self.learn_frame)
        input_frame.pack(fill="x", pady=10)
        
        ttk.Label(input_frame, text="Meaning (Korean):").pack(anchor="w")
        self.answer_entry = ttk.Entry(input_frame, font=("Arial", 14))
        self.answer_entry.pack(fill="x", pady=5)
        self.answer_entry.bind("<Return>", self.check_answer)
        
        self.submit_btn = ttk.Button(input_frame, text="Check Answer", command=self.check_answer)
        self.submit_btn.pack(fill="x", pady=5)

        # Feedback Section
        self.feedback_label = ttk.Label(self.learn_frame, text="", font=("Arial", 14, "bold"))
        self.feedback_label.pack(pady=20)
        
        self.next_btn = ttk.Button(self.learn_frame, text="Next Word", command=self.next_question, state="disabled")
        self.next_btn.pack(side="bottom", fill="x")

    def play_audio(self):
        if not self.current_word:
            return
            
        text = self.current_word["reading"] # Use reading for accurate pronunciation
        # Use macOS 'say' command (non-blocking)
        try:
            subprocess.Popen(["say", "-v", "Kyoko", text])
        except Exception as e:
            print(f"TTS Error: {e}")

    def create_review_tab(self):
        # Filter Controls
        filter_frame = ttk.Frame(self.review_frame)
        filter_frame.pack(fill="x", pady=5)
        
        self.filter_var = tk.StringVar(value="All")
        ttk.Radiobutton(filter_frame, text="All", variable=self.filter_var, value="All", command=self.update_review_list).pack(side="left", padx=5)
        ttk.Radiobutton(filter_frame, text="Correct (O)", variable=self.filter_var, value="correct", command=self.update_review_list).pack(side="left", padx=5)
        ttk.Radiobutton(filter_frame, text="Incorrect (X)", variable=self.filter_var, value="incorrect", command=self.update_review_list).pack(side="left", padx=5)
        
        ttk.Button(filter_frame, text="Retry Incorrect Words", command=self.retry_incorrect).pack(side="right", padx=5)
        
        # Treeview
        columns = ("word", "reading", "meaning", "status")
        self.tree = ttk.Treeview(self.review_frame, columns=columns, show="headings")
        
        self.tree.heading("word", text="Word")
        self.tree.heading("reading", text="Reading")
        self.tree.heading("meaning", text="Meaning")
        self.tree.heading("status", text="Status")
        
        self.tree.column("word", width=100)
        self.tree.column("reading", width=100)
        self.tree.column("meaning", width=200)
        self.tree.column("status", width=80)
        
        self.tree.pack(fill="both", expand=True)

    def on_level_change(self, event):
        level = self.level_var.get()
        if level != self.current_level:
            self.current_level = level
            self.load_level_data(level)

    def next_question(self):
        if not self.quiz_pool:
            messagebox.showinfo("Complete", "No more words in this session!")
            self.quiz_pool = self.full_vocab_data.copy() # Reset
            
        self.current_word = random.choice(self.quiz_pool)
        
        self.word_label.config(text=self.current_word["word"])
        self.reading_label.config(text=self.current_word["reading"])
        self.answer_entry.delete(0, "end")
        self.feedback_label.config(text="")
        
        # UI State
        self.answer_entry.config(state="normal")
        self.submit_btn.config(state="normal")
        self.next_btn.config(state="disabled")
        self.answer_entry.focus()

    def check_answer(self, event=None):
        user_input = self.answer_entry.get().strip()
        if not user_input:
            return

        correct_meaning = self.current_word["meaning"]
        
        # Simple containment check
        is_correct = user_input in correct_meaning or correct_meaning in user_input
        
        if is_correct:
            self.feedback_label.config(text="Correct! (정답)", foreground="green")
            self.update_word_status("correct")
        else:
            self.feedback_label.config(text=f"Incorrect. Answer: {correct_meaning}", foreground="red")
            self.update_word_status("incorrect")
            
        self.answer_entry.config(state="disabled")
        self.submit_btn.config(state="disabled")
        self.next_btn.config(state="normal")
        self.update_review_list()

    def update_word_status(self, status):
        if self.current_level not in self.progress_data:
            self.progress_data[self.current_level] = {}
            
        word_key = self.current_word["word"]
        self.progress_data[self.current_level][word_key] = status
        self.save_progress()

    def update_review_list(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        level_progress = self.progress_data.get(self.current_level, {})
        filter_mode = self.filter_var.get()
        
        for word_item in self.full_vocab_data:
            word = word_item["word"]
            status = level_progress.get(word, "Not Attempted")
            
            # Filter logic
            if filter_mode == "correct" and status != "correct":
                continue
            if filter_mode == "incorrect" and status != "incorrect":
                continue
                
            self.tree.insert("", "end", values=(word, word_item["reading"], word_item["meaning"], status))

    def retry_incorrect(self):
        level_progress = self.progress_data.get(self.current_level, {})
        incorrect_items = [
            item for item in self.full_vocab_data 
            if level_progress.get(item["word"]) == "incorrect"
        ]
        
        if not incorrect_items:
            messagebox.showinfo("Info", "오답인 단어가 없습니다! (No incorrect words found)")
            return
            
        self.quiz_pool = incorrect_items
        messagebox.showinfo("Retry Mode", f"오답 단어 {len(incorrect_items)}개로 학습을 시작합니다.")
        self.next_question()
        # Switch to learning tab
        self.notebook.select(self.learn_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = JapaneseLearningApp(root)
    root.mainloop()
