import tkinter as tk
from tkinter import messagebox, font
import json
import os

DATA_FILE = "tasks.json"

# ── Persistence ──────────────────────────────────────────────────────────────

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# ── App ───────────────────────────────────────────────────────────────────────

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✅ To-Do List  |  CodSoft Internship")
        self.root.geometry("520x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.tasks = load_tasks()   # list of {"text": str, "done": bool}

        self._build_ui()
        self._refresh_list()

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        BG        = "#1e1e2e"
        CARD      = "#313244"
        ACCENT    = "#cba6f7"   # lavender-purple
        TEXT      = "#cdd6f4"
        SUBTEXT   = "#a6adc8"
        GREEN     = "#a6e3a1"
        RED       = "#f38ba8"
        ENTRY_BG  = "#45475a"

        title_font  = font.Font(family="Segoe UI", size=18, weight="bold")
        label_font  = font.Font(family="Segoe UI", size=11)
        btn_font    = font.Font(family="Segoe UI", size=10, weight="bold")
        entry_font  = font.Font(family="Segoe UI", size=12)
        task_font   = font.Font(family="Segoe UI", size=11)
        done_font   = font.Font(family="Segoe UI", size=11, overstrike=True)

        self._task_font = task_font
        self._done_font = done_font
        self._TEXT      = TEXT
        self._SUBTEXT   = SUBTEXT
        self._CARD      = CARD
        self._GREEN     = GREEN
        self._RED       = RED
        self._ACCENT    = ACCENT
        self._BG        = BG

        # ── Header ──
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=20, pady=(20, 5))

        tk.Label(header, text="📝  My To-Do List", bg=BG, fg=ACCENT,
                 font=title_font).pack(side="left")

        self.count_label = tk.Label(header, text="", bg=BG, fg=SUBTEXT,
                                    font=label_font)
        self.count_label.pack(side="right", pady=6)

        # ── Input row ──
        input_frame = tk.Frame(self.root, bg=BG)
        input_frame.pack(fill="x", padx=20, pady=8)

        self.task_var = tk.StringVar()
        entry = tk.Entry(input_frame, textvariable=self.task_var,
                         font=entry_font, bg=ENTRY_BG, fg=TEXT,
                         insertbackground=ACCENT, relief="flat",
                         bd=0, highlightthickness=2,
                         highlightcolor=ACCENT,
                         highlightbackground=CARD)
        entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        entry.bind("<Return>", lambda e: self._add_task())

        add_btn = tk.Button(input_frame, text="+ Add", font=btn_font,
                            bg=ACCENT, fg="#1e1e2e", relief="flat",
                            activebackground="#b4befe",
                            padx=14, pady=6, cursor="hand2",
                            command=self._add_task)
        add_btn.pack(side="right")

        # ── Filter bar ──
        filter_frame = tk.Frame(self.root, bg=BG)
        filter_frame.pack(fill="x", padx=20, pady=(0, 6))

        self.filter_var = tk.StringVar(value="All")
        for label in ("All", "Pending", "Done"):
            rb = tk.Radiobutton(filter_frame, text=label,
                                variable=self.filter_var, value=label,
                                bg=BG, fg=SUBTEXT, selectcolor=BG,
                                activebackground=BG, activeforeground=ACCENT,
                                font=label_font, cursor="hand2",
                                command=self._refresh_list)
            rb.pack(side="left", padx=(0, 12))

        # ── Task list canvas with scrollbar ──
        list_outer = tk.Frame(self.root, bg=BG)
        list_outer.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.canvas = tk.Canvas(list_outer, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_outer, orient="vertical",
                                 command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=BG)

        self.scroll_frame.bind("<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>",
            lambda e: self.canvas.yview_scroll(-1*(e.delta//120), "units"))

        # ── Bottom action bar ──
        bottom = tk.Frame(self.root, bg=CARD)
        bottom.pack(fill="x", padx=20, pady=(0, 16))

        tk.Button(bottom, text="☑  Mark All Done", font=btn_font,
                  bg=GREEN, fg="#1e1e2e", relief="flat",
                  padx=10, pady=6, cursor="hand2",
                  command=self._mark_all_done).pack(side="left", padx=8, pady=8)

        tk.Button(bottom, text="🗑  Clear Done", font=btn_font,
                  bg=RED, fg="#1e1e2e", relief="flat",
                  padx=10, pady=6, cursor="hand2",
                  command=self._clear_done).pack(side="right", padx=8, pady=8)

    # ── Core logic ────────────────────────────────────────────────────────────

    def _add_task(self):
        text = self.task_var.get().strip()
        if not text:
            messagebox.showwarning("Empty task", "Please enter a task first.")
            return
        self.tasks.append({"text": text, "done": False})
        save_tasks(self.tasks)
        self.task_var.set("")
        self._refresh_list()

    def _toggle_done(self, index):
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        save_tasks(self.tasks)
        self._refresh_list()

    def _delete_task(self, index):
        self.tasks.pop(index)
        save_tasks(self.tasks)
        self._refresh_list()

    def _edit_task(self, index):
        win = tk.Toplevel(self.root)
        win.title("Edit Task")
        win.geometry("380x130")
        win.configure(bg=self._BG)
        win.grab_set()

        ef = font.Font(family="Segoe UI", size=12)
        bf = font.Font(family="Segoe UI", size=10, weight="bold")

        var = tk.StringVar(value=self.tasks[index]["text"])
        e = tk.Entry(win, textvariable=var, font=ef, bg="#45475a",
                     fg=self._TEXT, insertbackground=self._ACCENT,
                     relief="flat", bd=0, highlightthickness=2,
                     highlightcolor=self._ACCENT,
                     highlightbackground=self._CARD)
        e.pack(fill="x", padx=16, pady=20, ipady=8)
        e.focus_set()

        def save():
            new_text = var.get().strip()
            if not new_text:
                return
            self.tasks[index]["text"] = new_text
            save_tasks(self.tasks)
            self._refresh_list()
            win.destroy()

        e.bind("<Return>", lambda ev: save())
        tk.Button(win, text="Save", font=bf, bg=self._ACCENT,
                  fg="#1e1e2e", relief="flat", padx=12, pady=4,
                  command=save).pack()

    def _mark_all_done(self):
        for t in self.tasks:
            t["done"] = True
        save_tasks(self.tasks)
        self._refresh_list()

    def _clear_done(self):
        if not any(t["done"] for t in self.tasks):
            messagebox.showinfo("Nothing to clear", "No completed tasks to remove.")
            return
        if messagebox.askyesno("Confirm", "Remove all completed tasks?"):
            self.tasks = [t for t in self.tasks if not t["done"]]
            save_tasks(self.tasks)
            self._refresh_list()

    # ── Render list ───────────────────────────────────────────────────────────

    def _refresh_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        filt = self.filter_var.get()
        visible = [(i, t) for i, t in enumerate(self.tasks)
                   if filt == "All"
                   or (filt == "Done"    and t["done"])
                   or (filt == "Pending" and not t["done"])]

        total   = len(self.tasks)
        pending = sum(1 for t in self.tasks if not t["done"])
        self.count_label.config(
            text=f"{pending} pending / {total} total")

        if not visible:
            tk.Label(self.scroll_frame,
                     text="No tasks here yet ✨",
                     bg=self._BG, fg=self._SUBTEXT,
                     font=font.Font(family="Segoe UI", size=11)
                     ).pack(pady=30)
            return

        for i, task in visible:
            self._render_task_card(i, task)

    def _render_task_card(self, index, task):
        CARD  = self._CARD
        BG    = self._BG
        GREEN = self._GREEN
        RED   = self._RED
        TEXT  = self._TEXT
        done  = task["done"]

        card = tk.Frame(self.scroll_frame, bg=CARD, pady=0)
        card.pack(fill="x", pady=4, padx=2)

        # Colour stripe on left
        stripe_color = GREEN if done else self._ACCENT
        stripe = tk.Frame(card, bg=stripe_color, width=4)
        stripe.pack(side="left", fill="y")

        # Checkbox
        cb_var = tk.BooleanVar(value=done)
        cb = tk.Checkbutton(card, variable=cb_var, bg=CARD,
                            activebackground=CARD,
                            selectcolor=CARD,
                            command=lambda i=index: self._toggle_done(i),
                            cursor="hand2")
        cb.pack(side="left", padx=(6, 0))

        # Task text
        lbl_font = self._done_font if done else self._task_font
        lbl_color = self._SUBTEXT if done else TEXT
        lbl = tk.Label(card, text=task["text"], bg=CARD, fg=lbl_color,
                       font=lbl_font, anchor="w", wraplength=300,
                       justify="left")
        lbl.pack(side="left", fill="x", expand=True, padx=8, pady=10)

        # Edit button
        edit_btn = tk.Button(card, text="✏", bg=CARD, fg=self._ACCENT,
                             relief="flat", font=font.Font(size=12),
                             cursor="hand2", activebackground=CARD,
                             command=lambda i=index: self._edit_task(i))
        edit_btn.pack(side="right", padx=4)

        # Delete button
        del_btn = tk.Button(card, text="✕", bg=CARD, fg=RED,
                            relief="flat", font=font.Font(size=12),
                            cursor="hand2", activebackground=CARD,
                            command=lambda i=index: self._delete_task(i))
        del_btn.pack(side="right", padx=(4, 8))


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
