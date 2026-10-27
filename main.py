import tkinter as tk 
from tkinter import ttk 
import tkinter.font as tkfont
import random 
import math 
from datetime import datetime
import os
import csv
import json
import time
from decimal import Decimal
from predictor import predict_questions
import customtkinter as ctk
from PIL import Image
import sys 

root = tk.Tk()
root.title("Multi/Div/Sqrts Trainer")
root.geometry("1000x800")

BUTTON_WIDTH = 15
BUTTON_HEIGHT = 7
FONT_SIZE = 70

"""
Gear icon: https://icons8.com/icons/set/settings-page--yellow
Stop icon: https://www.iconsdb.com/red-icons/square-rounded-icon.html
Start icon: https://www.iconsdb.com/green-icons/play-icon.html
History icon: https://icones.pro/en/history-history-icon-png-symbol-blue/
Progress icon: https://icons8.com/icon/nqb0Et2diOFc/tasks

Unfinished extensions: 
MAKE ANOTHER, SMALLER VERSION WITHOUT ML TO DECREASE THE EXE FILE SIZE
 - (Small but time consuming) Guides on techniques for division, how to do square roots, cube roots, squares, and difference of squares
 - (Small) How to use the app (especially keybinds)
TODO (Small) Proper error checking
TODO Save settings while using the app and when close 
TODO Continually delete past history + clear history button
TODO (Big) User Login (username / password) 
 - (Small) Delete older questions 
 - (Big) Leaderboard based on time and accuracy (Must be random questions and at least 20+ questions completed) 
    - For time, make sure to get rid of any outlies
    - Create an elo score based on time, accuracy, and number of questions completed
 - Categories: 
    - Multi: 2x1, 3x1, 2x2, 3x2, 4x2, 3x3, 4x3, 5x3, 4x4
    - Division: 3/1, 4/1, 4/2, 5/2, 5/3, 6/3, 6/4, 
    - Square Roots: 3/4, 5/6, 7/8, 9/10
    - Cube Roots: 4/5/6, 7/8/9, 10/11/12
    - Difference of Squares: 2-2
    - Squares: 2, 3
    = ["2x1", "3x1", "2x2", "3x2", "4x2", "3x3", "4x3", "5x3", "4x4", 
    "3\u00F71", "4\u00F71", "4\u00F72", "5\u00F72", "5\u00F73", "6\u00F73", "6\u00F74",
    "2\u00B2", "3\u00B2",
    "\u221A3/4", "\u221A5/6", "\u221A7/8", "\u221A9/10",
    "2\u00B2-2\u00B2",
    "\u221B4/5/6", "\u221B7/8/9", "\u221B10/11/12"]
TODO Create competition style Listening / Flash with leaderboard
TODO (Big) VS Mode
"""
APP_DIR = os.path.join(
    os.environ["LOCALAPPDATA"],
    "Advanced Flash App"
)

os.makedirs(APP_DIR, exist_ok=True)

CSV_FILE = os.path.join(APP_DIR, "attempts.csv")
STATS_FILE = os.path.join(APP_DIR, "statistics.json")
USERS_FILE = os.path.join(APP_DIR, "users.json")


STAT_CATEGORIES = [
    "1x1 Multiplication",
    "2x1 Multiplication",
    "2x3 Multiplication",
    "3x1 Multiplication",
    "2x2 Multiplication",
    "3x2 Multiplication",
    "4x2 Multiplication",
    "3x3 Multiplication",
    "3x4 Multiplication",
    "4x3 Multiplication",
    "5x3 Multiplication",
    "4x4 Multiplication",

    "3/1 Division",
    "4/1 Division",
    "4/2 Division",
    "5/2 Division",
    "5/3 Division",
    "6/3 Division",
    "6/4 Division",

    "2 Squares",
    "3 Squares",

    "3/4 Square Roots",
    "5/6 Square Roots",
    "7/8 Square Roots",
    "9/10 Square Roots",

    "2-2 Difference of Squares",

    "4/5/6 Cube Roots",
    "7/8/9 Cube Roots",
    "10/11/12 Cube Roots"
]
if not os.path.exists(STATS_FILE):
    with open(STATS_FILE, "w") as f:
        json.dump({}, f, indent=4)
        
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "user", "a", "b", "operation", "correct",
            "response_time", "correct_answer",
            "user_answer", "timestamp"
        ])

class Settings: 
    def __init__(self, root, question_font):
        self.root = root

        self.modes = ["Multiplication", "Division", "Squares", "Square Roots", "Difference of Squares", "Cube Roots"]
        self.settings_window = None
        self.options_frame = None
        self.entries = {}
        self.variables = {}
        self.question_font = question_font
        self.mode_var = tk.StringVar(value = "Multiplication")        
        
        self.question_settings = {
            "Font Size": 20, 
            "Multiplication": {
                "first_length": 3, 
                "second_length": 3, 
                "first_decimals": 0, 
                "second_decimals": 0
            }, 
            "Division": {
                "dividend_length": 4, 
                "divisor_length": 2, 
                "dividend_decimals": 0, 
                "divisor_decimals": 0, 
                "decimal_quotients": False
            }, 
            "Squares": {
                "square_length": 2, 
                "decimal_length": 0
            }, 
            "Square Roots": {
                "radicand_length": "5, 6", 
                "decimal_length": 0, 
                "imperfect_root": False
            }, 
            "Difference of Squares": {
                "first_length": 2, 
                "second_length": 2, 
                "first_decimals": 0, 
                "second_decimals": 0,
                "negative_difference": False
            }, 
            "Cube Roots": {
                "decimal_length": 0, 
                "radicand_length": "4, 5, 6", 
                "imperfect_root": False
            }
        }

    # def fill_entry(self, entry, value): 

    def update_options(self, event = None): 
        self.entries = {}
        self.variables = {}
        self.mode = self.mode_var.get()
        for widget in self.options_frame.winfo_children(): 
            widget.destroy()
        self.row = tk.Frame(self.options_frame)
        self.row.pack(pady = 10)
        self.row2 = tk.Frame(self.options_frame)
        self.row2.pack(pady = 10)
        self.row3 = tk.Frame(self.options_frame)
        self.row3.pack(pady = 10) 
        self.row4 = tk.Frame(self.options_frame)
        self.row4.pack(pady = 10)
        self.row5 = tk.Frame(self.options_frame)
        self.row5.pack(pady = 10)
        self.row6 = tk.Frame(self.options_frame)
        self.row6.pack(pady = 10)
        self.button_row = tk.Frame(self.options_frame)
        self.button_row.pack(pady = 20)
        self.entry_1 = tk.Entry(self.row)
        self.entry_2 = tk.Entry(self.row2)
        self.entry_3 = tk.Entry(self.row3)
        self.entry_4 = tk.Entry(self.row4)
        
        if self.mode == "Multiplication":
            self.create_entry(self.row, "First Number Digit Length: ", "first_length")
            self.create_entry(self.row2, "Second Number Digit Length: ", "second_length")
            self.create_entry(self.row3, "Number of Decimals in First Factor: ", "first_decimals")
            self.create_entry(self.row4, "Number of Decimals in the Second Factor:" , "second_decimals") 
        elif self.mode == "Division": 
            self.create_entry(self.row, "Dividend Length: ", "dividend_length")
            self.create_entry(self.row2, "Divisor Length: ", "divisor_length")
            self.create_entry(self.row3, "Decimals in Dividend: ", "dividend_decimals")
            self.create_entry(self.row4, "Decimals in Divisor: ", "divisor_decimals")
            self.create_checkbox(self.row5, "Decimal Quotients: ", "decimal_quotients") 
        elif self.mode == "Squares": 
            self.create_entry(self.row, "Square Length: ", "square_length")
            self.create_entry(self.row2, "Decimals in Square: ", "decimal_length")
        elif self.mode == "Square Roots": 
            self.create_combo(self.row, "Radicand Length: ", "radicand_length", ["1, 2", "3, 4", "5, 6", "7, 8", "9, 10", "11, 12"])
            self.create_entry(self.row2, "Decimals in Radicand: ", "decimal_length") 
            self.create_checkbox(self.row3, "Imperfect Roots: ", "imperfect_root")
        elif self.mode == "Difference of Squares": 
            self.create_entry(self.row, "First Square Length: ", "first_length")
            self.create_entry(self.row2, "Second Square Length: ", "second_length")
            self.create_entry(self.row3, "Decimals in First Square: ", "first_decimals")
            self.create_entry(self.row4, "Decimals in Second Square: ", "second_decimals")
            self.create_checkbox(self.row5, "Negative Difference: ", "negative_difference")
        elif self.mode == "Cube Roots": 
            self.create_combo(self.row, "Radicand Length: ", "radicand_length", ["1, 2, 3", "4, 5, 6", "7, 8, 9", "10, 11, 12"])
            self.create_entry(self.row2, "Decimals in Radicand: ", "decimal_length")
            self.create_checkbox(self.row3, "Imperfect Cube Root: ", "imperfect_root")
        self.load_settings()
        # Save Button 
        tk.Button(self.button_row, text = "Save", command=self.save, width = 9, height = 2).pack(side="left", padx = 20)
        # Cancel Button
        tk.Button(self.button_row, text = "Cancel", command=self.settings_window.withdraw, width = 9, height = 2).pack(side = "right", padx = 20)
    
    def load_settings(self): 
        saved = self.question_settings[self.mode] 
        for key, entry in self.entries.items():
            if key in saved: 
                entry.insert(0, str(saved[key]))
        for key, variable in self.variables.items(): 
            if key in saved: 
                variable.set(saved[key])

    def create_entry(self, frame, text, key): 
        tk.Label(frame, text = text).pack(side = "left")
        entry = tk.Entry(frame, width = 13)
        entry.pack(side = "right")
        self.entries[key] = entry

    def create_combo(self, frame, text, key, values): 
        var = tk.StringVar() 
        combobox = ttk.Combobox(frame, values=values, textvariable = var, state="readonly", width = 13)
        combobox.pack(side = "right")
        tk.Label(frame, text = text).pack(side = "left") 
        self.variables[key] = var

    def create_checkbox(self, frame, text, key): 
        tk.Label(frame, text = text).pack(side = "left")
        variable = tk.BooleanVar()
        tk.Checkbutton(frame, variable = variable).pack(side = "right")
        self.variables[key] = variable

    def open_settings(self): 
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("400x450")

        title = tk.Label(self.settings_window, text = "Settings Menu", font = ("Roboto", 20))
        title.pack(pady = 10)
        mode_dropdown = ttk.Combobox(self.settings_window, justify = "center", values=self.modes, textvariable = self.mode_var, state="readonly")
        mode_dropdown.pack(pady = 5)

        self.font_frame = tk.Frame(self.settings_window)
        self.font_frame.pack(pady = 5)

        tk.Label(self.font_frame, text = "Font Size: ").pack(side = "left")

        self.font_entry = tk.Entry(self.font_frame, width = 3)
        self.font_entry.pack(side = "left", padx = 5)

        self.font_entry.delete(0, tk.END)
        self.font_entry.insert(0, str(self.question_font.cget("size")))

        self.options_frame = tk.Frame(self.settings_window)
        self.options_frame.pack(pady = 10)
        
        mode_dropdown.bind("<<ComboboxSelected>>", self.update_options)

        if self.mode_var.get() == "": 
            self.mode_var.set("Multiplication")
        self.update_options()
        
    def save(self):
        mode = self.mode_var.get()
        settings = {}
        try: 
            font_size = int(self.font_entry.get())
            if font_size <= 0: 
                raise ValueError
            self.question_settings["Font Size"] = font_size
            self.question_font.config(size = font_size)
        except ValueError: 
            pass
        for key, entry in self.entries.items(): 
            value = entry.get()            
            if not value.isdigit(): 
                print("Please enter valid integers.")  # TODO later need to trigger a popup 
                return 
            settings[key] = int(value) 
        for key, var in self.variables.items(): 
            settings[key] = var.get()
        self.question_settings[mode] = settings
        self.settings_window.withdraw()
    
class Trainer(): 
    for i in range(30):
        root.grid_rowconfigure(i, weight = 1)

    for i in range(30): 
        root.grid_columnconfigure(i, weight = 1)
    
    def __init__(self, root):
        self.question_font = tkfont.Font(family = "Roboto", size = FONT_SIZE)
        self.settings = Settings(root, self.question_font)
        self.root = root
        self.after_id = None
        self.first_number = 0
        self.second_number = 0
        self.start_time = 0 
        self.probability = 0
        self.total = 0
        self.correct = 0
        self.num_correct = 0
        self.elapsed_time = 0.0
        self.stopwatch_running = False
        self.stopwatch_after_id = None
        self.time_sum = 0
        self.statistics = {}
        self.history = []
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        changed = False
        
        with open(STATS_FILE, "r") as f: 
            self.statistics = json.load(f)
        for category in STAT_CATEGORIES:
            if category not in self.statistics:
                self.statistics[category] = {
                    "questions": 0,
                    "correct": 0,
                    "total_time": 0
                }
                changed = True
        if changed:
            with open(STATS_FILE, "w") as f:
                json.dump(self.statistics, f, indent=4)
                
        # Change to dumping into a csv
        if os.path.getsize(CSV_FILE) != 0: 
            with open(CSV_FILE, "r", newline="") as file: 
                reader = csv.DictReader(file)
                for row in reader:
                    self.history.append(row)

        self.var = tk.StringVar(value = "Current Session")
        self.question_types = ["Current Session", "1x1","2x1", "2x3", "3x1", "2x2", "3x2", "4x2", "3x3", "3x4", "4x3", "5x3", "4x4", 
                                "3\u00F71", "4\u00F71", "4\u00F72", "5\u00F72", "5\u00F73", "6\u00F73", "6\u00F74",
                                "2\u00B2", "3\u00B2", 
                                "\u221A3/4", "\u221A5/6", "\u221A7/8", "\u221A9/10",
                                "2\u00B2-2\u00B2",
                                "\u221B4/5/6", "\u221B7/8/9", "\u221B10/11/12"]
        self.q_name_dict = {}
        for i in self.question_types: 
            if "x" in i: 
                self.q_name_dict[i] = self.statistics[f"{i} Multiplication"]["questions"]
            # Division
            elif "\u00F7" in i: 
                self.q_name_dict[i] = self.statistics[f"{str(i)[0]}/{str(i)[2]} Division"]["questions"]
            # Diff Squares 
            elif "\u00B2" in i and "-" in i: 
                self.q_name_dict[i] = self.statistics["2-2 Difference of Squares"]["questions"]
            # Squares 
            elif "\u00B2" in i: 
                self.q_name_dict[i] = self.statistics[f"{str(i)[0]} Squares"]["questions"]
            # Square Roots
            elif "\u221A" in i: 
                if "3" in i:
                    self.q_name_dict[i] = self.statistics["3/4 Square Roots"]["questions"]
                elif "5" in i: 
                    self.q_name_dict[i] = self.statistics["5/6 Square Roots"]["questions"]
                elif "7" in i: 
                    self.q_name_dict[i] = self.statistics["7/8 Square Roots"]["questions"]
                elif "9" in i: 
                    self.q_name_dict[i] = self.statistics["9/10 Square Roots"]["questions"]
            # Cube Root
            elif "\u221B" in i: 
                if "4" in i: 
                    self.q_name_dict[i] = self.statistics["4/5/6 Cube Roots"]["questions"]
                elif "7" in i: 
                    self.q_name_dict[i] = self.statistics["7/8/9 Cube Roots"]["questions"]
                elif "10" in i: 
                    self.q_name_dict[i] = self.statistics["10/11/12 Cube Roots"]["questions"]
        self.question_types = [key for key, value in sorted(self.q_name_dict.items(), key = lambda item: item[1], reverse = True)]
        self.question_types.insert(0, "Current Session")
        
        

        self.question_label = tk.Label(root, text = "", font=self.settings.question_font, width = 12)
        self.question_label.place(relx=0.55, rely=0.45, anchor = "center")
        self.answer_entry = tk.Entry(root, font=("Roboto", 30), width = 10, bd = 2)
        self.answer_entry.bind("<Return>", self.on_enter)

    def resource_path(self, filename): 
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, filename)
    
    def show_sidebar(self): 
        TOP_ROW = 3
        sidebar = tk.Frame(root, width = 180) 
        sidebar.grid(row = TOP_ROW , column = 1, rowspan = 30, sticky = "ns")
        sidebar.grid_propagate(False)

        self.start_image = ctk.CTkImage(light_image=Image.open(self.resource_path("play_icon.png")), size = (50, 50), dark_image=Image.open(self.resource_path("play_icon.png")))
        start_button = ctk.CTkButton(sidebar, image=self.start_image, text = "   Start   ", border_width=5, border_color="#6CE975", text_color="black", command=self.show_sequence, font = ("Roboto", 20, "bold"), hover_color="#6CE975", fg_color = "#F3F1F1", corner_radius=15, height = 100)
        start_button.grid(row = TOP_ROW, column = 1, sticky = "nw")
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#F3F1F1")
        separator.grid(row = TOP_ROW+2, column = 1, stick = "ew", padx = 20, pady = 5)

        self.stop_image = ctk.CTkImage(light_image=Image.open(self.resource_path("stop_icon.png")), size = (50, 50), dark_image=Image.open(self.resource_path("stop_icon.png")))
        stop_button = ctk.CTkButton(sidebar, image=self.stop_image, border_width=5, border_color="#EC6569",text = "    Stop   ", text_color="black", hover_color="#EC6569", command=self.stop, corner_radius=15, font = ("Roboto", 20, "bold"), fg_color = "#F3F1F1", height=100)
        stop_button.grid(row = TOP_ROW+3, column = 1, sticky = "nw")
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#F3F1F1")
        separator.grid(row = TOP_ROW+5, column = 1, stick = "ew", padx = 20, pady = 5)

        self.gear_image = ctk.CTkImage(light_image=Image.open(self.resource_path("gear_image.png")), size = (50,50), dark_image=Image.open(self.resource_path("gear_image.png")))
        settings_button = ctk.CTkButton(sidebar, image=self.gear_image, border_width=5, border_color="#F5FD80", text = " Settings", text_color="black", hover_color="#F5FD80", fg_color="#F3F1F1", command=self.settings.open_settings, corner_radius=15, font = ("Roboto", 20, "bold"), height = 100)
        settings_button.grid(row = TOP_ROW+6, column = 1, sticky = "nw")
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#F3F1F1")
        separator.grid(row = TOP_ROW+8, column = 1, stick = "ew", padx = 20, pady = 5)

        self.history_image = ctk.CTkImage(light_image=Image.open(self.resource_path("history_icon.png")), dark_image=Image.open(self.resource_path("history_icon.png")), size=(50,50))
        history_button = ctk.CTkButton(sidebar, image=self.history_image, border_width=5, border_color="#97BBF0", text = " History  ", text_color="black", hover_color= "#97BBF0", fg_color="#F3F1F1", command=self.show_history, font = ("Roboto", 20, "bold"), height = 100, corner_radius=15)
        history_button.grid(row = TOP_ROW+9, column = 1, sticky = "nw")
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#F3F1F1")
        separator.grid(row = TOP_ROW+11, column = 1, stick = "ew", padx = 20, pady = 5)

        self.progress_image = ctk.CTkImage(light_image = Image.open(self.resource_path("progress_icon1.png")), dark_image=Image.open(self.resource_path("progress_icon1.png")), size = (50, 50))
        progress_button = ctk.CTkButton(sidebar, compound = "left", anchor="w", image = self.progress_image, border_width = 5, command = self.show_progress, text = "Progress", border_color="#D36AF3", hover_color = "#D36AF3", text_color = "black", fg_color = "#F3F1F1", font = ("Roboto", 20, "bold"), height = 100, corner_radius=15)
        progress_button.grid(row = TOP_ROW+12, column = 1, sticky = "nw")
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#F3F1F1")
        separator.grid(row = TOP_ROW+14, column = 1, stick = "ew", padx = 20, pady = 5)

        self.prob_enabled = ctk.BooleanVar(value = False) 
        self.prob_checkbox = ctk.CTkCheckBox(sidebar, command = self.toggle_probability, text = f"AI: {self.probability}", font = ("Roboto", 24, "bold"), variable=self.prob_enabled, text_color = "#F3F1F1", fg_color = "black")
        self.prob_checkbox.grid(row = TOP_ROW+15, column = 1, stick = "w")
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#F3F1F1")
        separator.grid(row = TOP_ROW+17, column = 1, stick = "ew", padx = 20, pady = 5)

        self.stopwatch_enabled = ctk.BooleanVar(value = True) 
        self.stopwatch_checkbox = ctk.CTkCheckBox(sidebar, command=self.toggle_stopwatch, text = "0.00s", variable= self.stopwatch_enabled, text_color="black", fg_color="black", font = ("Roboto", 24, "bold"))
        self.stopwatch_checkbox.grid(row = 23, column = 1, sticky = "w")
        
        self.root.bind_all("<Key>", self.handle_bind)

    def toggle_probability(self): 
        if self.prob_enabled.get(): 
            self.prob_checkbox.configure(text_color = "black") 
        else : 
            self.prob_checkbox.configure(text_color = "#F3F1F1")

    def toggle_stopwatch(self): 
        if self.stopwatch_enabled.get(): 
            self.stopwatch_checkbox.configure(text_color = "black")
        else:
            self.stopwatch_checkbox.configure(text_color = "#F3F1F1")
    # -------------------- Logic -------------------- 
    def show_result(self, event = None): 
        mode = self.settings.mode_var.get()
        if self.first_number == 0 and self.second_number == 0: 
            return 0
        elif mode == "Multiplication": 
            answer = Decimal(str(self.first_number)) * Decimal(str(self.second_number))
        elif mode == "Division": 
            if self.settings.question_settings["Division"]["decimal_quotients"]: 
                answer = (round((self.first_number / self.second_number), 2))
            else: 
                answer = (int(self.first_number / self.second_number))
        elif mode == "Squares": 
            answer = (round(self.first_number ** 2, 2)) 
        elif mode == "Square Roots": 
            s_decimal_length = self.settings.question_settings["Square Roots"]["decimal_length"]
            if math.sqrt(self.first_number * 10 ** s_decimal_length).is_integer(): 
                if math.sqrt(self.first_number).is_integer(): 
                    answer = (int(math.sqrt(self.first_number)))
                else: 
                    answer = (round(math.sqrt(self.first_number), s_decimal_length))
            else: 
                answer = (round((math.sqrt(self.first_number)), 2))
        elif mode == "Cube Roots":
            c_decimal_length = self.settings.question_settings["Cube Roots"]["decimal_length"] 
            if math.cbrt(self.first_number * 10 ** c_decimal_length).is_integer(): 
                if math.cbrt(self.first_number).is_integer(): 
                    answer = (int(math.cbrt(self.first_number)))
                else: 
                    answer = (round(math.cbrt(self.first_number), c_decimal_length))
            else: 
                answer = (round((math.cbrt(self.first_number)), 2))
        elif mode == "Difference of Squares": 
            neg_diff = self.settings.question_settings["Difference of Squares"]["negative_difference"]
            if (neg_diff == False and self.first_number > self.second_number) or (neg_diff and self.second_number > self.first_number): 
                answer = (round(self.first_number ** 2 - self.second_number ** 2, 2))
            else: 
                answer = (round(self.second_number ** 2 - self.first_number ** 2, 2))
        return answer
 
    def generate_number(self, digits, decimals): 
        if digits == 1: 
            whole = random.randint(1, 9)
        elif digits == 0: 
            whole = 0 
        else: 
            whole = random.randint(10**(digits-1), 10**digits - 1)
        
        if decimals == 0: 
            return whole
        decimal = "".join(str(random.randint(0, 9)) for num in range(decimals))
        return float(f"{whole}.{decimal}")
    
    def special_division(self, d1, d2): 
        while True: 
            temp = self.generate_number(d1 - d2, 0)
            divisor = self.generate_number(d2, 0) 
            if temp * divisor >=  10 ** (d1-1):
                break
        return [temp*divisor, divisor]

    def choose_next_q(self, target_prob = 0.6, candidates = 30): 
        mode = self.settings.mode_var.get()
        best = ""
        a = 0
        b = 0
        # positive infinity
        best_difference = float("inf")
        temp_out = ""
        for _ in range(candidates): 
            temp_out = self.generate_question() 
            self.probability = predict_questions(self.first_number, self.second_number, mode, self.show_result()) 
            difference = abs(self.probability - target_prob) 
            if difference < best_difference: 
                a = self.first_number
                b = self.second_number
                best_difference = difference
                best = temp_out
        self.first_number = a 
        self.second_number = b
        return best 
    
    def generate_question(self): 
        mode = self.settings.mode_var.get() 
        if mode == "Multiplication": 
            multi_settings = self.settings.question_settings["Multiplication"]
            self.first_number = self.generate_number(multi_settings["first_length"], multi_settings["first_decimals"])
            self.second_number = self.generate_number(multi_settings["second_length"], multi_settings["second_decimals"])
            question = f"{self.first_number} x {self.second_number}"
        elif mode == "Division": 
            division_settings = self.settings.question_settings["Division"] 
            if division_settings["decimal_quotients"]: 
                self.first_number = self.generate_number(division_settings["dividend_length"], division_settings["dividend_decimals"])
                self.second_number = self.generate_number(division_settings["divisor_length"], division_settings["divisor_decimals"])
            else: 
                # divisor
                self.second_number = self.generate_number(division_settings["divisor_length"], division_settings["divisor_decimals"])
                multiplier = 1
                if division_settings["divisor_length"] > division_settings["dividend_length"]: 
                        multiplier = 10 ** division_settings["divisor_decimals"]
                else: 
                    multiplier = 10 ** division_settings["dividend_decimals"]
                while True: 
                    self.first_number = self.generate_number(division_settings["dividend_length"], division_settings["dividend_decimals"])
                    if ((self.first_number * multiplier) / (self.second_number * multiplier)).is_integer(): 
                        break
                if (division_settings["dividend_length"] == 4 and division_settings["divisor_length"] == 2) or (division_settings["dividend_length"] == 5 and division_settings["divisor_length"] == 2 or division_settings["divisor_length"] == 3) or (division_settings["dividend_length"] == 6 and division_settings["divisor_length"] == 2) or (division_settings["dividend_length"] == 6 and division_settings["divisor_length"] == 3) or (division_settings["dividend_length"] == 6 and division_settings["divisor_length"] == 4): 
                    tup = self.special_division(division_settings["dividend_length"], division_settings["divisor_length"])
                    self.first_number = tup[0]
                    self.second_number = tup[1]
            question = f"{self.first_number} \u00F7 {self.second_number}"
        
        elif mode == "Squares": 
            squares_settings = self.settings.question_settings["Squares"] 
            self.first_number = self.generate_number(squares_settings["square_length"], squares_settings["decimal_length"])
            question = f"{self.first_number}\u00B2" # superscript of 2
        elif mode == "Square Roots": 
            s_roots_settings = self.settings.question_settings["Square Roots"] 
            s_radicand_length = [int(num) for num in s_roots_settings["radicand_length"].split(", ")]
            s_decimal_length = s_roots_settings["decimal_length"]
            if s_roots_settings["imperfect_root"]: 
                self.first_number = self.generate_number(random.randint(s_radicand_length[0], s_radicand_length[1]), s_decimal_length)
            else: 
                self.first_number = round((self.generate_number(round(s_radicand_length[1]/2), int(s_decimal_length/2))) ** 2, s_decimal_length)
            question =  f"\u221A{self.first_number}" # square root symbol
        elif mode == "Difference of Squares": 
            diff_settings = self.settings.question_settings["Difference of Squares"] 
            self.first_number = self.generate_number(diff_settings["first_length"], diff_settings["first_decimals"])
            self.second_number = self.generate_number(diff_settings["second_length"], diff_settings["second_decimals"])
            if (diff_settings["negative_difference"] and self.first_number > self.second_number) or (diff_settings["negative_difference"] == False and self.second_number > self.first_number): 
                question =  f"{self.second_number}\u00B2 - {self.first_number}\u00B2"
            elif (diff_settings["negative_difference"] and self.second_number > self.first_number) or (diff_settings["negative_difference"] == False and self.first_number > self.second_number): 
                question =  f"{self.first_number}\u00B2 - {self.second_number}\u00B2"
        elif mode == "Cube Roots": 
            c_roots_settings = self.settings.question_settings["Cube Roots"]
            c_radicand_length = [int(num) for num in c_roots_settings["radicand_length"].split(", ")]
            c_decimal_length = c_roots_settings["decimal_length"]
            if c_roots_settings["imperfect_root"]: 
                self.first_number = self.generate_number(random.randint(c_radicand_length[0], c_radicand_length[2]), c_decimal_length)
            else: 
                self.first_number = round(self.generate_number(math.ceil(c_radicand_length[2]/3), int(c_decimal_length/3)) ** 3, c_decimal_length)
            question = f"\u221B{self.first_number}"
        answer = self.show_result()

        return question
    # -----------------------------------------------
    
    def save_attempt(self, user, a, b, operation, correct, response_time, correct_answer, user_answer, timestamp): 
        filename = CSV_FILE
        fieldnames = ["user", 
                            "a", 
                            "b", 
                            "operation", 
                            "correct", 
                            "response_time",
                            "correct_answer", 
                            "user_answer",
                            "timestamp", "prediction"]
        attempt = {
                "user" : user,
                "a" : a, 
                "b" : b, 
                "operation" : operation, 
                "correct" : correct, 
                "response_time" : response_time, 
                "correct_answer" : correct_answer, 
                "user_answer" : user_answer, 
                "timestamp" : timestamp, 
                "prediction" : round(self.probability, 2) 
            }
        self.history.append(attempt)
        # append
        with open(filename, "a", newline="") as file: 
            writer = csv.DictWriter(file, fieldnames=fieldnames) 
            
            if file.tell() == 0: 
                writer.writeheader()
            writer.writerow(attempt)

    def handle_bind(self, event): 
        if isinstance(event.widget, tk.Entry): 
            return
        commands = {
            "1" : self.show_sequence,
            "2" : self.stop, 
            "3" : self.settings.open_settings, 
            "4" : self.show_history, 
            "5" : self.show_progress,
            "Return" : self.show_sequence
        }
        command = commands.get(event.keysym)
        if command:
            command() 

    def stop(self, event = None): 
        if self.after_id is not None: 
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.question_label.config(text = "")
        self.answer_entry.delete(0, tk.END) 
        self.answer_entry.place_forget()
        self.question_count = 0
        self.stop_stopwatch()

    
    def show_sequence(self, step = 0, event = None): 
        mode = self.settings.question_settings[self.settings.mode_var.get()]
        self.question_label.config(fg="#000000")
        if step == 0: 
            self.question_label.config(text = "Ready?") 
            self.after_id = self.root.after(500, lambda: self.show_sequence(1)) 
        elif step == 1:
            self.start_stopwatch()
            self.answer_entry.place(relx = 0.55, rely = 0.55, anchor="center")
            self.answer_entry.focus_set()
            
            if self.prob_enabled.get(): 
                self.question = self.choose_next_q()
            else: 
                self.question = self.generate_question()
            self.probability = predict_questions(self.first_number, self.second_number, self.settings.mode_var.get(), self.show_result())
            print(f"AI guess: {self.probability:.2%}")
            self.prob_checkbox.configure(text = f"AI: {self.probability:.2%}")
            self.question_label.config(text = f"{self.question}")

    def start_stopwatch(self): 
        self.start_time = time.perf_counter()
        self.stopwatch_running = True
        self.update_stopwatch() 

    def update_stopwatch(self): 
        if not self.stopwatch_running: 
            return 
        elapsed = time.perf_counter() - self.start_time
        self.stopwatch_checkbox.configure(text = f"{elapsed:.2f}s")
        self.stopwatch_after_id = self.root.after(10, self.update_stopwatch)

    def stop_stopwatch(self): 
        self.stopwatch_running = False
        if self.stopwatch_after_id is not None: 
            self.root.after_cancel(self.stopwatch_after_id)
        final_time = time.perf_counter() - self.start_time
        self.stopwatch_checkbox.configure(text=f"{final_time:.2f}s")
        return final_time
    
    def on_enter(self, event = None): 
        self.mode = self.settings.mode_var.get()
        self.stop_stopwatch()
        response_time = round(time.perf_counter() - self.start_time, 3)
        self.time_sum += response_time
        user_answer = self.answer_entry.get()
        self.total += 1
        correct = (user_answer == str(self.show_result()))
        self.question_label.config(text = f"{self.question} =\n{self.show_result()}")
        self.save_attempt(user="Kevin", a = self.first_number, b=self.second_number, correct_answer=self.show_result(), response_time=response_time, user_answer=user_answer, timestamp=datetime.now().strftime("%m/%d/%y %H:%M"), operation=self.settings.mode_var.get(), correct=correct)
        key = ""
        if not isinstance(self.first_number, float) and not isinstance(self.second_number, float):
            if ("Multiplication" == self.mode): 
                key = f"{len(str(self.first_number))}x{len(str(self.second_number))} Multiplication"
            elif "Division" == self.mode: 
                key = f"{len(str(self.first_number))}/{len(str(self.second_number))} Division"
            elif "Squares" == self.mode: 
                key = f"{len(str(self.first_number))} Squares"
            elif "Square Roots" == self.mode: 
                if self.first_number == 3 or self.first_number == 4: 
                    key = "3/4 Square Roots"
                elif self.first_number == 5 or self.first_number == 6: 
                    key = "5/6 Square Roots"
                elif self.first_number == 7 or self.first_number == 8: 
                    key = "7/8 Square Roots"
                elif self.first_number == 9 or self.first_number == 10: 
                    key = "9/10 Square Roots"
            elif "Cube Roots" == self.mode: 
                if self.first_number == 4 or self.first_number == 5 or self.first_number == 6: 
                    key = "4/5/6 Cube Roots"
                elif self.first_number == 7 or self.first_number == 8 or self.first_number == 9: 
                    key = "7/8/9 Cube Roots"
                elif self.first_number == 10 or self.first_number == 11  or self.first_number == 12: 
                    key = "10/11/12 Cube Roots"
            elif "Difference of Squares" == self.mode: 
                key = f"{len(str(self.first_number))}-{len(str(self.second_number))} Difference of Squares"
        
        if key in self.statistics:
            self.statistics[key]["questions"] += 1
            if correct:
                self.statistics[key]["correct"] += 1
            self.statistics[key]["total_time"] += response_time
            with open(STATS_FILE, "w") as f:
                json.dump(self.statistics, f, indent=4)
            print(f"Updated {key}: {self.statistics[key]}")
        if correct: 
            self.num_correct += 1
            if (self.probability >= 0.5): 
                self.correct += 1
            self.question_label.config(fg = "#2E7D32")
        else: 
            if (self.probability < 0.5): 
                self.correct += 1
            self.question_label.config(fg= "#FF474C")
        print(f"Correct {self.correct * 100 / self.total}%")
        if self.after_id: 
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.root.focus_set()
        self.answer_entry.delete(0, tk.END) 
        self.answer_entry.place_forget() 

    def on_close(self): 
        with open(STATS_FILE, "w") as f: 
            json.dump(self.statistics, f, indent=4)
        self.root.destroy() 
    
    def show_stats(self, mode): 
        pass

    def show_progress(self, event = None): 
        self.progress_window = tk.Toplevel(self.root) 
        self.progress_window.title("Progress") 
        self.progress_window.geometry("350x200")

        title = tk.Label(self.progress_window, text="Progress", font = ("Roboto", 20)) 
        title.pack(pady = 10)
        """
        Questions Answered
        Accuracy
        Average Time per Question

        Categories: (Sorted from easiest to most difficult)
         - Questions Completed
         - Accuracy
         - Average Time
         - sorted from most questions count 
        Create a category
        """
        mode_dropdown = ttk.Combobox(self.progress_window, values=self.question_types, textvariable = self.var, state="readonly", justify="center")
        mode_dropdown.pack(pady = 5)

        self.progress_frame = tk.Frame(self.progress_window)
        self.progress_frame.pack(anchor = "w", padx = 20, pady = 10)
        
        mode_dropdown.bind("<<ComboboxSelected>>", self.update_progress)
        self.update_progress()

    def update_progress(self, event = None): 
        tk.Label(self.progress_frame, text = "Questions Completed: ", anchor="e", width = 25).grid(row = 0, column = 0, sticky = "w") 
        tk.Label(self.progress_frame, text = "Accuracy: ", anchor="e", width = 25).grid(row = 1, column = 0, sticky = "w")
        tk.Label(self.progress_frame, text = "Average Time per Question: ", anchor="e", width = 25).grid(row = 2, column = 0, sticky = "w")

        if self.var.get() == "Current Session": 
            tk.Label(self.progress_frame, text = f"{self.total}", anchor="w", width = 10).grid(row = 0, column = 1, sticky = "w") 
            if self.total != 0: 
                tk.Label(self.progress_frame, text = f"{(self.num_correct * 100 / self.total):.2f}%", anchor="w", width = 10).grid(row = 1, column = 1, sticky = "w") 
            if self.total != 0: 
                tk.Label(self.progress_frame, text = f"{(self.time_sum / self.total):.2f}s", anchor="w", width = 10).grid(row = 2, column = 1, sticky = "w") 
        else: 
            correct = 0
            total_q = 0
            total_time = 0
            # Multiplication
            if "x" in self.var.get(): 
                key = f"{self.var.get()} Multiplication"
            # Division
            elif "\u00F7" in self.var.get(): 
                key = f"{str(self.var.get())[0]}/{str(self.var.get())[2]} Division"
            # Diff Squares 
            elif "\u00B2" in self.var.get() and "-" in self.var.get(): 
                key = "2-2 Difference of Squares"
            # Squares 
            elif "\u00B2" in self.var.get(): 
                key = f"{str(self.var.get())[0]} Squares"
            # Square Roots
            elif "\u221A" in self.var.get(): 
                if "3" in self.var.get():
                    key = "3/4 Square Roots"
                elif "5" in self.var.get(): 
                    key = "5/6 Square Roots"
                elif "7" in self.var.get(): 
                    key = "7/8 Square Roots"
                elif "9" in self.var.get(): 
                    key = "9/10 Square Roots"
            # Cube Root
            elif "\u221B" in self.var.get(): 
                if "4" in self.var.get(): 
                    key = "4/5/6 Cube Roots"
                elif "7" in self.var.get(): 
                    key = "7/8/9 Cube Roots"
                elif "10" in self.var.get(): 
                    key = "10/11/12 Cube Roots"
            correct = self.statistics[key]["correct"] 
            total_q = self.statistics[key]["questions"] 
            total_time = self.statistics[key]["total_time"]              
            if total_q != 0: 
                accuracy = round(correct * 100 / total_q, 2)
                average_time = round(total_time / total_q, 2)
            else: 
                accuracy = 0
                average_time = 0
            tk.Label(self.progress_frame, text = f"{total_q}", anchor="w", width = 10).grid(row = 0, column = 1, sticky = "w") 
            tk.Label(self.progress_frame, text = f"{accuracy}%", anchor="w", width = 10).grid(row = 1, column = 1, sticky = "w") 
            tk.Label(self.progress_frame, text = f"{average_time}s", anchor="w", width = 10).grid(row = 2, column = 1, sticky = "w") 
                        
    def show_history(self, event=None): 
        self.history_window = tk.Toplevel(self.root) 
        self.history_window.title("History") 
        self.history_window.geometry("450x500") 
        title = tk.Label(self.history_window, text="History", font=("Roboto", 20)) 
        title.pack(pady=10) 
        frame = tk.Frame(self.history_window) 
        frame.pack(fill="both", expand=True, padx=15, pady=10) 
        scrollbar = tk.Scrollbar(frame) 
        scrollbar.pack(side="right", fill="y") 
        history = tk.Text(frame, yscrollcommand=scrollbar.set) 
        history.pack(side="left", fill="both", expand=True) 
        scrollbar.config(command=history.yview) 
        # Configure colors once 
        history.tag_config("correct", foreground="#2E7D32") 
        history.tag_config("incorrect", foreground="#FF474C") 
        for item in reversed(self.history): 
            question = ( f"{self.format_question(item['a'], item['b'], item['operation'])} " f"= {item['correct_answer']} ({item['user_answer']})" ) 
            space = " " * max(0, math.floor((37 - len(question)) / 2)) 
            line = f"{item['timestamp']}{space}{question}\n" 
            if str(item["correct_answer"]) == item["user_answer"]: 
                history.insert(tk.END, line, "correct")
            else: 
                history.insert(tk.END, line, "incorrect") 
        history.config(state="disabled") # Optional: make history read-only

    def format_question(self, a, b, operation): 
        if operation == "Multiplication": 
            return f"{a} x {b}"
        elif operation == "Division": 
            return f"{a} \u00F7 {b}"
        elif operation == "Squares": 
            return f"{a}\u00B2"
        elif operation == "Square Roots":
            return f"\u221A{a}" 
        elif operation == "Cube Roots": 
            return f"\u221B{a}"
        elif operation == "Difference of Squares": 
            return f"{a}\u00B2 - {b}\u00B2"

App = Trainer(root)
App.show_sidebar()
root.mainloop()