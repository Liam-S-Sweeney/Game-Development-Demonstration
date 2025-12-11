import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("400x300")

# Create canvas + scrollbar container
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

# Bind scrollbar to frame
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

# Make window-like window
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Add widgets to scrollable frame
for i in range(50):
    ttk.Label(scrollable_frame, text=f"Label {i}").pack()

root.mainloop()

