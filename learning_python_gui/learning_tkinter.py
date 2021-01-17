import tkinter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

root = tkinter.Tk()
root.wm_title("Testing Tkinter")


def make_sin_graph(master):
    fig = Figure(figsize=(5, 4), dpi=100)

    t = np.arange(0, 3, 0.01)
    handle = fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


    def on_key_press(event):
        print(f"You pressed {event.key}")
        handle[0].set_ydata(np.sin(2*np.pi * t))
        canvas.draw()
        # key_press_handler(event, canvas, toolbar)

    def on_slider_change(new_slider_val):
        handle[0].set_ydata(np.sin(float(new_slider_val) * np.pi * t))
        canvas.draw()
        print(f"New slider val is {new_slider_val}")

    canvas.mpl_connect("key_press_event", on_key_press)

    sli = tkinter.Scale(master, from_=10.0, to=20.5, orient=tkinter.HORIZONTAL, command=on_slider_change,
                        variable=tkinter.DoubleVar, digits=4, label="A")
    sli.pack()


def make_quit_button():
    def quit():
        root.quit()
        root.destroy()

    button = tkinter.Button(master=root, text="Quit", command=quit)
    button.pack(side=tkinter.BOTTOM)


if __name__ == "__main__":
    make_sin_graph(root)
    make_quit_button()
    tkinter.mainloop()
