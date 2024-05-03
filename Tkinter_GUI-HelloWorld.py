import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Hello World Example")

# Create a label widget
label = tk.Label(root, text="Hello, World!")
label.pack()  # Pack the label in the window

# Print "Hello, World!" to the console
print("Hello, World!")
print("If You Dont Want To See This Console or Shell Window. \nThen Rename Your Python file from example.py to example.pyw")

# Run the Tkinter event loop
root.mainloop()
