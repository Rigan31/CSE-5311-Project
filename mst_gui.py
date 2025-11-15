import tkinter as tk
from gui import MSTApp


def main():
    root = tk.Tk()
    app = MSTApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()