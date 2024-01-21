import secrets
import string
import time

import pyperclip as pc
import PySimpleGUI as sg


class GenPass:

    def __init__(self):
        self.lower = True
        self.upper = True
        self.numbers = False
        self.symbols = False
        self.length = 14
        
    def genpass(self):
        seed = ""

        if self.lower:
            seed += string.ascii_lowercase
        if self.upper:
            seed += string.ascii_uppercase
        if self.numbers:
            seed += string.digits
        if self.symbols:
            seed += string.punctuation

        if seed:
            return ''.join(secrets.choice(seed) for i in range(int(self.length)))

        return seed
    

class GenPassGUI:

    def __init__(self):
        self.genpass = GenPass()

        sg.theme('Dark Blue 3')

        layout = [  
            [sg.Checkbox("Lower case", key="-LOWER CASE-", expand_x=True, enable_events=True, default=True), sg.Checkbox("Upper case", key="-UPPER CASE-", expand_x=True, enable_events=True, default=True)],
            [sg.Checkbox("Numbers", key="-NUMBERS-", expand_x=True, enable_events=True), sg.Checkbox("Symbols", key="-SYMBOLS-", expand_x=True, enable_events=True)],
            [sg.Slider((8, 20), default_value=14, key="-LENGTH-", orientation="h", enable_events=True, expand_x=True)],
            [sg.Input("", key="-PASSWORD-", readonly=True, pad=((0,0), (20,10)), justification="center", size=(35, 0)), sg.Button("Generate", key="-GENERATE-")],
            [sg.Text("Password copied!", key="-PASSWORD COPIED-", justification="center", expand_x=True, visible=False)]
        ]

        self.window = sg.Window("Password generator", layout, finalize=True, size=(350, 200))
        self.window["-PASSWORD-"].bind("<Button-1>", "+COPY PASSWORD+")
        self.window["-PASSWORD-"].update(self.genpass.genpass())

    def password_copied(self):
        self.window["-PASSWORD COPIED-"].update(visible=True)
        time.sleep(2)
        self.window["-PASSWORD COPIED-"].update(visible=False)

    def run(self):

        while True:
            event, values = self.window.read()
            
            print(event, values)

            if event in (None, 'Exit'):
                break

            elif event in ["-LOWER CASE-", "-UPPER CASE-", "-NUMBERS-", "-SYMBOLS-", "-LENGTH-"]:
                self.genpass.lower = values["-LOWER CASE-"]
                self.genpass.upper = values["-UPPER CASE-"]
                self.genpass.numbers = values["-NUMBERS-"]
                self.genpass.symbols = values["-SYMBOLS-"]
                self.genpass.length = values["-LENGTH-"]
                self.window["-PASSWORD-"].update(self.genpass.genpass())
                
            elif event == "-GENERATE-":
                self.window["-PASSWORD-"].update(self.genpass.genpass())

            elif event == "-PASSWORD-+COPY PASSWORD+":
                pc.copy(values["-PASSWORD-"])
                self.window.perform_long_operation(self.password_copied, "-LONG OPERATION DONE-")

        self.window.close()


if __name__ == "__main__":
    gpg = GenPassGUI()
    gpg.run()