##############################################################################################
#                                           NEW GUI                                          #
##############################################################################################
# This is a (hopefully) better version of the gui
# Version name: cal_gui V.0.0.2

# The goals remain unchanged
##############################################################################################
#                                            to do                                           #
##############################################################################################
# 1. Must be able to run Doom
# 1. SOLVING FUNCTIONS
# 2. Differentiation and integration of functions
# 3. Graphing these functions and make them easily interactable
# 4. A compiler?? interpreter?? something to write code in
# 5. 3D BABYYYYYY

##############################################################################################
#                                        Finished goals                                      #
##############################################################################################
# 1. Basic calculations
# 2. Order of operations with parsing trees
# 3. A simple GUI

import PySimpleGUI as sg
import math
from tokenshunt import calout

numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8","9"]
operators = ["+", "-", "/", "*", "^", "(", ")"]

# Function that is called when creating the button grid layout of the calculator
def CBtn(button_text):
    return sg.Button(button_text, button_color= ("white", "blue"), size = (5, 1), font = ("Helvetica", 16))

def show_his(num, my_list1):
    return f"{my_list1[num][0]} = {my_list1[num][1]}"

def main():
    sg.theme("Dark Blue 3") # COLORS
    history = []
    # Creates the layout of the main calculator window
    main_layout = [
        [sg.TabGroup([
            [sg.Tab("Simple", layout = [
                [sg.Text("Input numbers"), sg.Input()],
                [CBtn(t) for t in ("MENU", "HIS", "BKSP", "^")],
                [CBtn(t) for t in ("1", "2", "3", "+")],
                [CBtn(t) for t in ("4", "5", "6", "-")],
                [CBtn(t) for t in ("7", "8", "9", "*")],
                [CBtn(t) for t in ("(","0",")", "/")],
                [sg.Button("Enter"), sg.Button("Cancel")]
            ])],
            [sg.Tab("Scientific", layout = [
                [sg.Text("Input numbers"), sg.Input()],
                [CBtn(t) for t in ("MENU", "HIS", "BKSP", "FUNC")],
                [CBtn(t) for t in ("SIN", "COS", "TAN", "DIFF")]
                ])
            ]
        ])]
    ]

    main = sg.Window("Calculator", main_layout)

    # This function creates the history window
    def open_history():
        history_layout = [  # Creates the layout for the history window
            [sg.Text("Equation and result history", size=(22,1), font=("Helvetica", 20), justification = "center")],
            [[sg.Text(show_his(row, history), size=(22,1), pad=(0,0), key = "-OUT-", font=("Helvetica", 20), justification = "center")] for row in range(len(history))],
            [sg.Button("Exit"), sg.Button("Clear")]
        ]

        his_win = sg.Window("History",history_layout)
        while True:
            event, values = his_win.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break

            elif event == "Clear" and len(history) != 0:
                history.clear()
                his_win.close()
                open_history()
        his_win.close(); del his_win
    
    deci = 0
    # This function creates the menu window
    def open_menu(self):
        self.decimal = 0
        menu_layout = [  # Creates the layout for the menu window
        [sg.Text("Light/dark mode")],
        [sg.Text("Number of decimalplaces"), sg.Input(), sg.Button("Enter")],
        [sg.Text("PLACEHOLDER")],
        [sg.Text("PLACEHOLDER")],
        [sg.Text("PLACEHOLDER")],
        [sg.Text("PLACEHOLDER")],
        ]

        menu_win = sg.Window("Menu", menu_layout)
        while True:
            event, values = menu_win.read()
            if event == "Exit" or sg.WIN_CLOSED:
                break
            
            if event == "Enter" and values[0].isdigit():
                self.decimal = values[0]
                menu_win[1].update(self.decimal)
        menu_win.close()

    # Opens the main window
    # Use a while loop to keep the window running and read the events and values from main
    while True:
        event, values = main.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break

        if event in numbers or event in operators:
            main[0].update(f"{values[0]}{event}")

        if event == "BKSP":
            if values[0] == "":
                continue
            my_string = values[0]
            # Might be worth changing the slicing thing
            new_string = my_string[:-1]
            main[0].update(new_string)

        if event == "HIS":
            open_history()
        
        if event == "MENU":
            MENU = open_menu(MENU)
        
        if event == "Enter":
            if deci <= 0:
                deci = 2
            res = calout(values[0], deci)
            history.append([values[0],res])
            main[0].update(res)
    main.close(); del main

if __name__ == "__main__":
    main()
        
