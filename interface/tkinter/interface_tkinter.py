import tkinter as tk
from interface.interface_base import InterfaceBase

class InterfaceTkinter(InterfaceBase):
    '''Class for program interface using Tkinter library.'''

    def __init__(self, config: dict) -> None:
        '''
        Initializes an instance of InterfaceTkinter.

        : param config: (dict) - tkinter configuration object.
        
        : return: (None) - this function does not return any value.
        '''
        super().__init__(config)

    def get_color(self) -> bool:
        '''
        Launch program interface and get color from user.

        : return: (bool) - user choice of which color they play.
        '''
        def submit_choice():
            root.destroy()

        # Create the main window
        root = tk.Tk()
        root.title("Choose a Color")
        root.geometry("400x250")  # Set the window size

        # Variable to store the selected color (using 0 for "white" and 1 for "black")
        selected_color = tk.IntVar(value=0)

        # Create a label for the question
        question_label = tk.Label(root, text="Choose the color", font=("Helvetica", 14))
        question_label.pack(pady=10)

        # Create radio buttons for white and black
        white_button = tk.Radiobutton(root, text="White", variable=selected_color, value=0)
        black_button = tk.Radiobutton(root, text="Black", variable=selected_color, value=1)

        # Create submit button
        submit_button = tk.Button(root, text="Submit", command=submit_choice)

        # Pack the buttons into the window
        white_button.pack(pady=5)
        black_button.pack(pady=5)
        submit_button.pack(pady=15)

        root.mainloop()

        return selected_color.get()