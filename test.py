import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()

# Create a dummy label just to create a default root window
dummy_label = tk.Label(root, text="Dummy Label")
dummy_label.pack()

# Get a list of available fonts
all_fonts = tkFont.families()

# Print the list of fonts
for font in all_fonts:
    print(font)
    dummy_label = tk.Label(root, text="Dummy Label", font=("Terminal", 20))
    dummy_label.pack()

root.mainloop()
