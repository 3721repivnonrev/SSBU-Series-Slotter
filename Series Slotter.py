import os
import json
import tkinter as tk
from tkinter import filedialog, ttk


#so glad I had this lying around
class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")))
        self.window = self.canvas.create_window((0, 0), window=self.scrollable_frame,
                anchor="nw")

        self.canvas.bind("<Configure>", self._resize_frame)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _resize_frame(self, event):
        self.canvas.itemconfigure(self.window, width=event.width)

    def _on_mousewheel(self, event):
        if hasattr(event, "num"):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-event.delta / 120), "units")


#divider for the main code
blacklist = ['balloonfight', 'bayonetta', 'castlevania', 'donkeykong', 'doubutsu', 'duckhunt', 'etc', 'famicomrobot', 'finalfantasy', 'fireemblem', 'fzero', 'gamewatch', 'iceclimber', 'kirby', 'lightplane', 'mario', 'mariokart', 'metalgear', 'metroid', 'mii', 'miiplaza', 'mother', 'nintendogs', 'none', 'pacman', 'palutena', 'pikmin', 'plankton', 'pokemon', 'punchout', 'rockman', 'smashbros', 'sonic', 'splatoon', 'starfox', 'streetfighter', 'tomodachi', 'touch', 'wario', 'wiifit', 'wreckingcrew', 'wuhuisland', 'xenoblade', 'yoshi', 'zelda']
root_folder = filedialog.askdirectory(title="Select Folder")
series_icons = []
series_0_folder = os.path.join(root_folder, "ui", "replace", "series", "series_0")
series_1_folder = os.path.join(root_folder, "ui", "replace", "series", "series_1")

if os.path.exists(series_0_folder):
    for filename in os.listdir(series_0_folder):
        if filename.endswith(".bntx"):
            series_icons.append(filename.split("series_0_")[1].split(".bntx")[0])

if os.path.exists(series_1_folder):
    for filename in os.listdir(series_1_folder):
        if filename.endswith(".bntx"):
            series_icons.append(filename.split("series_1_")[1].split(".bntx")[0])

series_icons = sorted(set(series_icons))

root = tk.Tk()
root.title("Series Autoslotter Tool")
series_frame = ScrollableFrame(root)
series_frame.pack(fill="both", expand=True)
series_vars = []
series_rows = []

def sanitise(var, *args):
    value = var.get()
    cleaned = value.lower().replace(" ", "_").replace("\n", "")
    if cleaned != value:
        var.set(cleaned)

for series in series_icons:
    var = tk.StringVar(value=series)
    series_vars.append(var)
    frm = ttk.Frame(series_frame.scrollable_frame)
    frm.pack(fill="x", padx=5, pady=2)
    entry = ttk.Entry(frm, textvariable=var, width=30)
    entry.pack(side="left")
    remove = tk.Button(frm, text="Remove", command=lambda var=var: remove_series(var.get()))
    remove.pack(side="right")
    var.trace_add("write", lambda *args, var=var: sanitise(var))
    series_rows.append({"var": var, "frame": frm})

def print_series():
    renamed_set = {var.get().strip() for var in series_vars if var.get().strip()}
    print(renamed_set)

def add_series():
    var = tk.StringVar(value="new_series")
    series_vars.append(var)
    frm = ttk.Frame(series_frame.scrollable_frame)
    frm.pack(fill="x", padx=5, pady=2)
    entry = ttk.Entry(frm, textvariable=var, width=30)
    entry.pack(side="left")
    remove = tk.Button(frm, text="Remove", command=lambda var=var: remove_series(var.get()))
    remove.pack(side="right")
    var.trace_add("write", lambda *args, var=var: sanitise(var))
    series_rows.append({"var": var, "frame": frm})

def remove_series(name):
    name = name.lower().replace(" ", "_")
    for row in series_rows[:]:
        if row["var"].get() == name:
            row["frame"].destroy()
            series_rows.remove(row)
            series_vars.remove(row["var"])
            break

ttk.Button(root, text="Add Series", command=add_series).pack(pady=5, padx=5)

root.mainloop()

series = sorted({var.get().strip() for var in series_vars if var.get().strip()})
final_set = [serie for serie in series if serie not in blacklist]

data = {"series_database_entries": []}

for series in final_set:
    data["series_database_entries"].append({
            "clone_from_series_id": "ui_series_mario",
            "ui_series_id": f"ui_series_{series}",
            "name_id": series,
            "disp_order_sound": -1
        })
folder = os.path.join(root_folder, "database")
os.makedirs(folder, exist_ok=True)
path = os.path.join(folder, "series.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
