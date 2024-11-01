import tkinter as tk
from interface.interface_base import InterfaceBase
from utils.interface_utils import ButtonValue, LabelValue

class InterfaceTkinter(InterfaceBase):
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

    def run(self) -> None:
        '''
        Creates main asking menu for different questions.

        : return: (None) - this function does not return any value.
        '''
        def on_close():
            self._is_running = False
            window.destroy()

        def color_selection():
            self._color = color_var.get()

        def mode_selection():
            self._mode = mode_var.get()

        def toggle_pause_run():
            self._pause = not self._pause
            if switch_var.get() == "Pause":
                switch_var.set("Run")
            else:
                switch_var.set("Pause")
        
        self._is_running = True
        window = tk.Tk()
        window.title(LabelValue.TITLE)
        window.geometry(self._window_size)
        window.resizable(False, False)

        # Set up the color question
        color_frame = tk.Frame(window)
        color_frame.pack(side=tk.LEFT, padx=20, pady=20)

        color_label = tk.Label(color_frame, text=LabelValue.COLOR_QUESTION)
        color_label.pack(anchor=tk.W)

        color_values = [ButtonValue.WHITE, ButtonValue.BLACK]
        color_var = tk.StringVar(value=color_values[0])  # default selection
        self._color = color_var.get()
        for i in range(2):
            color_button = tk.Radiobutton(color_frame,
                                          text=color_values[i],
                                          variable=color_var,
                                          value=color_values[i],
                                          command=color_selection)
            color_button.pack(anchor=tk.W)

        # Set up the mode question
        mode_frame = tk.Frame(window)
        mode_frame.pack(side=tk.RIGHT, padx=20, pady=20)

        mode_label = tk.Label(mode_frame, text=LabelValue.MODE_QUESTION)
        mode_label.pack(anchor=tk.W)

        mode_values = [ButtonValue.AUTO_MODE, ButtonValue.SPEECH_RECOGNITION, ButtonValue.DETECTION_MODE]
        mode_var = tk.StringVar(value=mode_values[0])  # default selection
        self._mode = mode_var.get()
        for i in range(3):
            mode_button = tk.Radiobutton(mode_frame,
                                         text=mode_values[i],
                                         variable=mode_var,
                                         value=mode_values[i],
                                         command=mode_selection)
            mode_button.pack(anchor=tk.W)

        # Add the Pause/Run switch
        switch_frame = tk.Frame(window)
        switch_frame.pack(side=tk.BOTTOM, pady=20)

        self._pause = True
        switch_var = tk.StringVar(value="Run")  # default state
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

        : return: (str) - user choice of which program mode to run.
        '''
        return self._mode
    
    def is_on_pause(self) -> bool:
        '''
        Gets program state from user.

        : return: (bool) - window state whether the program is paused or not.
        '''
        return self._pause
    
    def is_running(self) -> bool:
        '''
        Gets program state from user.

        : return: (bool) - window state whether the program is running or not.
        '''
        return self._is_running