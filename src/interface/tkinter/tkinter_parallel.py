import tkinter as tk
from typing import List
from interface.interface_base import InterfaceBase
from utils.interface_utils import ButtonValue, LabelValue

class TkinterParallel(InterfaceBase):
    '''Class for program interface using Tkinter library.'''

    def __init__(self, config: dict) -> None:
        '''
        Initializes an instance of TkinterParallel.

        : param config: (dict) - tkinter configuration object.
        
        : return: (None) - this function does not return any value.
        '''
        super().__init__(config)
        self._window_size = config["window_size"]
        self._font = config["font"]
        self._font_size = config["font_size"]
        self._pause = True

    def run(self) -> None:
        '''
        Creates main asking menu for different questions.

        : return: (None) - this function does not return any value.
        '''
        def on_close():
            pass

        def on_selection():
            self._color = left_var.get()
            self._mode = right_var.get()
            print(f"Color: {self._color}, Program mode: {self._mode}")

        def toggle_pause_run():
            self._pause = not self._pause
            if switch_var.get() == "Pause":
                switch_var.set("Run")
            else:
                switch_var.set("Pause")
    
        window = tk.Tk()
        window.title(LabelValue.TITLE)
        window.geometry(self._window_size)
        window.resizable(False, False)

        # Set up the left question with two radio buttons
        left_question_frame = tk.Frame(window)
        left_question_frame.pack(side=tk.LEFT, padx=20, pady=20)

        left_label = tk.Label(left_question_frame, text=LabelValue.COLOR_QUESTION)
        left_label.pack(anchor=tk.W)

        left_var = tk.StringVar(value=ButtonValue.WHITE)  # Default selection

        left_radio1 = tk.Radiobutton(left_question_frame, text=ButtonValue.WHITE, variable=left_var, value=ButtonValue.WHITE, command=on_selection)
        left_radio1.pack(anchor=tk.W)

        left_radio2 = tk.Radiobutton(left_question_frame, text=ButtonValue.BLACK, variable=left_var, value=ButtonValue.BLACK, command=on_selection)
        left_radio2.pack(anchor=tk.W)

        # Set up the right question with three radio buttons
        right_question_frame = tk.Frame(window)
        right_question_frame.pack(side=tk.RIGHT, padx=20, pady=20)

        right_label = tk.Label(right_question_frame, text=LabelValue.MODE_QUESTION)
        right_label.pack(anchor=tk.W)

        right_var = tk.StringVar(value=ButtonValue.AUTO_MODE)  # Default selection

        right_radio1 = tk.Radiobutton(right_question_frame, text=ButtonValue.AUTO_MODE, variable=right_var, value=ButtonValue.AUTO_MODE, command=on_selection)
        right_radio1.pack(anchor=tk.W)

        right_radio2 = tk.Radiobutton(right_question_frame, text=ButtonValue.SPEECH_RECOGNITION, variable=right_var, value=ButtonValue.SPEECH_RECOGNITION, command=on_selection)
        right_radio2.pack(anchor=tk.W)

        right_radio3 = tk.Radiobutton(right_question_frame, text=ButtonValue.DETECTION_MODE, variable=right_var, value=ButtonValue.DETECTION_MODE, command=on_selection)
        right_radio3.pack(anchor=tk.W)

        # Add the Pause/Run switch below the radio buttons
        switch_frame = tk.Frame(window)
        switch_frame.pack(side=tk.BOTTOM, pady=20)

        switch_var = tk.StringVar(value="Run")  # Default state

        switch_button = tk.Button(switch_frame, textvariable=switch_var, command=toggle_pause_run, width=10)
        switch_button.pack()

        window.protocol("WM_DELETE_WINDOW", on_close)
        window.mainloop()
    
    def get_color(self) -> str:
        '''
        Gets color from user.

        : return: (str) - user choice of which color they play.
        '''
        return self._color
    
    def get_program_mode(self) -> str:
        '''
        Gets program mode from user.

        : return: (str) - user choice of program mode that will be run.
        '''
        return self._mode
    
    def is_on_pause(self) -> bool:
        '''
        Gets program state from user.

        : return: (bool) - user choice whether the program will be active or not.
        '''
        return self._pause