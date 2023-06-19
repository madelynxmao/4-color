import tkinter as tk


def create_grid(event=None):
    w = c.winfo_width() # Get current width of canvas
    h = c.winfo_height() # Get current height of canvas
    c.delete('grid_line') # Will only remove the grid_line

    for i in range(0, w, w//lineNumber): # <-- CHANGED
        c.create_line([(i, 0), (i, h)], tag='grid_line')

    for i in range(0, h, h//lineNumber): # <-- CHANGED
        c.create_line([(0, i), (w, i)], tag='grid_line')


lineNumber = 10 # <-- CHANGED

root = tk.Tk()

c = tk.Canvas(root, height=1000, width=1000, bg='white')
c.pack(fill=tk.BOTH, expand=True)

c.bind('<Configure>', create_grid)

root.mainloop()