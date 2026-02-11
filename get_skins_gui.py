import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import filedialog
import subprocess
import sys
# function to run client skin scraping
def run_scraper():
    save_path = entry.get()

    if not save_path:
        messagebox.showerror("Error", "Please choose a file destination.")
        return

    subprocess.run([sys.executable, "GetSkins.py", save_path])
    messagebox.showinfo("Done", f"CSV saved to:\n{save_path}")


# function to choose csv destination
def choose_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="owned_skins.csv"
    )
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)


root = tk.Tk()
root.title("LoL Skin Scraper")
# root.geometry("420x320")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

BG = "#494950"
SURFACE = "#242426"
ACCENT = "#ff4d62"
ACCENT_HOVER = "#ff6666"
TEXT = "#ddd5d5"
MUTED = "#bfbfbf"

root.configure(bg=BG)
style.configure(".", background=BG, foreground=TEXT, font=("Segoe UI", 10))

# Title style
style.configure(
    "Title.TLabel",
    font=("Segoe UI Semibold", 15),
    foreground=ACCENT
)

style.configure(
    "Body.TLabel",
    foreground=MUTED
)

style.configure(
    "TEntry",
    fieldbackground=SURFACE,
    foreground=TEXT,
    bordercolor=ACCENT,
    lightcolor=ACCENT,
    darkcolor=SURFACE,
    padding=6
)

style.configure(
    "Accent.TButton",
    background=ACCENT,
    foreground="white",
    borderwidth=0,
    padding=8
)

style.map(
    "Accent.TButton",
    background=[("active", ACCENT_HOVER), ("pressed", "#cc3a3a")]
)


main_frame = ttk.Frame(root, padding=15)
main_frame.grid(row=0, column=0, sticky="nsew")

top_frame = ttk.Frame(main_frame)
top_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15))

explanation = ttk.Label(
    top_frame,
    text=(
        "Open your league client and click 'Get Skins' to run the scraper.\n"
        "This will generate an owned_skins.csv file"
        "with all of your League skins!\n"
        "Upload it to vibzy.pet to find matching skins :3"
    ),
    wraplength=300,
    justify="left",
    style="Explanation.TLabel"
)
explanation.pack(side="left", padx=(0, 15))

image = PhotoImage(file="sqrk40ruok3f11.png")
image = image.subsample(2, 2)

image_label = ttk.Label(top_frame, image=image)
image_label.image = image
image_label.pack(side="right")


ttk.Label(main_frame, text="File Destination:").grid(
    row=1, column=0, sticky="w", padx=(0, 10), pady=5
)

entry = ttk.Entry(main_frame, width=25)
entry.grid(row=1, column=1, sticky="w", pady=5)
entry.insert(0, "owned_skins.csv")

entry.bind("<Button-1>", lambda e: choose_file())


btn = ttk.Button(
    main_frame,
    text="Get Skins",
    style="Accent.TButton",
    command=run_scraper
)
btn.grid(row=2, column=0, columnspan=2, pady=(15, 0), sticky="ew")



root.mainloop()
