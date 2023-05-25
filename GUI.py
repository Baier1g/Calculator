import PySimpleGUI as sg
import re
from shunting_yard import calout

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8','9']
operators = ['+', '-', '/', '*', '(', ')']

def CBtn(button_text):
    return sg.Button(button_text, button_color=('white', 'blue'), size=(4, 1), font=("Helvetica", 20))

def run_gui():
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text('Input numbers'), sg.Input()],
                [CBtn(t) for t in ('1', '2', '3', '+', 'BKSP')],
                [CBtn(t) for t in ('4', '5', '6', '-')],
                [CBtn(t) for t in ('7', '8', '9', '*')],
                [CBtn(t) for t in ('(','0',')', '/')],
                [sg.Text('Set precision (decimalplaces)'), sg.Input()],
                [sg.Button('Enter'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Calculator', layout)
    history = []
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        
        if event in numbers or event in operators:
            if values[0] == None:
                window[0].update(event)
            else:    
                window[0].update(f'{values[0]}{event}')

        if event == 'BKSP':
            my_string = values[0]
            # Might be worth changing the slicing thing
            new_string = my_string[:-1]
            print(new_string)
            window[0].update(new_string)
        
        if values[1] == "":
            values[1] = 2
        # If the value dict hadn't updated, line 22 could fix the problem
        #list(minvariable.values())
        if event == 'Enter':
            res = calout(values[0],int(values[1]))
            window[0].update(res)
            history.append(res)
    window.close()

if __name__ == "__main__":
    run_gui()