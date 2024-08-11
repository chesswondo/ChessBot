import tkinter as tk
from typing import List
from interface.interface_base import InterfaceBase
from utils.interface_utils import ButtonValue, LabelValue

class InterfaceTkinter(InterfaceBase):
    '''Class for program interface using Tkinter library.'''

    def __init__(self, config: dict) -> None:
        '''
        Initializes an instance of InterfaceTkinter.

        : param config: (dict) - tkinter configuration object.
        
        : return: (None) - this function does not return any value.
        '''
        super().__init__(config)
        self._window_size = config["window_size"]
        self._font = config["font"]
        self._font_size = config["font_size"]

    def _main_asking_menu(self, title: str, question: str, option_values: List[str]) -> str:
        '''
        Creates main asking menu for different questions.

        : param title: (str) - title on the window.
        : param question: (str) - question on the window.
        : param option_values: (List[str]) - list of the values bounded with buttons and also their names.

        : return: (str) - selected option.
        '''
        def on_close():
            pass
    
        def submit_action(window):
            window.destroy()

        window = tk.Tk()
        window.title(title)
        window.geometry(self._window_size)
        window.resizable(False, False)

        radio_var = tk.StringVar(value=option_values[0])

        radio_buttons = []
        num_options = len(option_values)
        for i in range(num_options):
            radio_button = tk.Radiobutton(window,
                                          text=option_values[i],
                                          variable=radio_var,
                                          value=option_values[i],
                                          font=(self._font, self._font_size))
            radio_buttons.append(radio_button)

        question_label = tk.Label(window, text=question, font=(self._font, self._font_size))
        question_label.pack(pady=10)

        for radio_button in radio_buttons:
            radio_button.pack(pady=10)

        submit_button = tk.Button(window, text="Submit", command=lambda: submit_action(window), font=(self._font, self._font_size))
        submit_button.pack(pady=15)

        window.protocol("WM_DELETE_WINDOW", on_close)
        window.mainloop()

        return radio_var.get()

    def get_color(self) -> str:
        '''
        Launch program interface and get color from user.

        : return: (str) - user choice of which color they play.
        '''
        return self._main_asking_menu(LabelValue.COLOR_TITLE,
                                     LabelValue.COLOR_QUESTION,
                                     [ButtonValue.WHITE, ButtonValue.BLACK])
    
    def get_program_mode(self) -> str:
        '''
        Launch program interface and get program mode from user.

        : return: (str) - user choice of program mode that will be run.
        '''
        return self._main_asking_menu(LabelValue.MODE_TITLE,
                                     LabelValue.MODE_QUESTION,
                                     [ButtonValue.AUTO_MODE, ButtonValue.SPEECH_RECOGNITION, ButtonValue.DETECTION_MODE])