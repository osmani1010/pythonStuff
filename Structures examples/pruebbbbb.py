import tkinter as tk

# Create main window
root = tk.Tk()
root.title("Advanced Label Example")
root.geometry("400x300")

# Label 1 (centered)
label1 = tk.Label(root, text="Welcome!", font=("Verdana", 18, "bold"), fg="green")
label1.pack(pady=20)

# Label 2 (left-aligned using grid)
label2 = tk.Label(root, text="This is a left-aligned label", font=("Helvetica", 14), fg="black")
label2.grid(row=1, column=0, sticky="w", padx=10)

# Label 3 (custom position using place)
label3 = tk.Label(root, text="Positioned at x=100, y=200", font=("Times", 12), fg="purple")
label3.place(x=100, y=200)

# Run the application
root.mainloop()
