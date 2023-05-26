import PySimpleGUI as sg
import re
from shunting_yard import calout

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8','9']
operators = ['+', '-', '/', '*', '(', ')']

def CBtn(button_text):
    return sg.Button(button_text, button_color=('white', 'blue'), size=(4, 1), font=("Helvetica", 16))

def show_his(num,my_list):
    return f'{my_list[num][0]} = {my_list[num][1]}'

def open_window(my_list):
    headings = ['EQUATION', 'RESULT']
    pop_layout =  [
        [sg.Text('  ')] + [sg.Text(h, size=(14,1)) for h in headings],
        [[sg.Text(size=(15,1), pad=(0,0)) for col in range(2)] for row in range(len(my_list))],
        [sg.Button('Exit')]
        ]


    pophistory = sg.Window('History',pop_layout)
    while True:
        event, values = pophistory.read()
        for i in range(len(my_list)):
            pophistory[i].update(show_his(i,my_list))
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    pophistory.close()

def run_gui():
    sg.theme('Dark Blue 3')   # Add a touch of color
    # All the stuff inside your window.
    history = []
    layout = [  [sg.Text('Input numbers'), sg.Input()],
                [CBtn(t) for t in ('1', '2', '3', '+', 'BKSP')],
                [CBtn(t) for t in ('4', '5', '6', '-', 'HIS')],
                [CBtn(t) for t in ('7', '8', '9', '*')],
                [CBtn(t) for t in ('(','0',')', '/')],
                [sg.Text('Set precision (decimalplaces)'), sg.Input()],
                [sg.Button('Enter'), sg.Button('Cancel')]]
    
    # Create the Window
    window = sg.Window('Calculator', layout)
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
        
        if event == 'HIS' and len(history) != 0:
            open_window(history)
        else:
            pass

        if values[1] == "":
            values[1] = 2
        # If the value dict hadn't updated, line 22 could fix the problem
        #list(minvariable.values())
        if event == 'Enter':
            res = calout(values[0],int(values[1]))
            history.append([values[0],res])
            window[0].update(res)
    window.close()


if __name__ == "__main__":
    run_gui()