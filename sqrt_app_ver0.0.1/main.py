import os
import logging
import tkinter as tk
from tkinter import ttk

from config import load_config
from localization import LocalizationManager
from controller import Controller

APP_DIR = os.path.dirname(os.path.abspath(__file__))

def setup_logging():
    logging.basicConfig(
        filename=os.path.join(APP_DIR, "app.log"),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sqrt Calculator")
        self.resizable(False, False)

        self.cfg = load_config(os.path.join(APP_DIR, "config.json"))
        self.loc = LocalizationManager(os.path.join(APP_DIR, "locales"), self.cfg.default_language)
        self.controller = Controller(self.loc)

        # state
        self.var_input = tk.StringVar()
        self.var_precision = tk.IntVar(value=max(0, min(5, self.cfg.default_precision)))
        self.var_both = tk.BooleanVar(value=False)
        self.var_lang = tk.StringVar(value=self.loc.lang)

        self._apply_dark_theme()
        self._build_ui()
        self._apply_language()

    def _build_ui(self):
        pad = 10
        root = ttk.Frame(self, padding=pad)
        root.grid(row=0, column=0)

        # Language
        self.lbl_lang = ttk.Label(root)
        self.cmb_lang = ttk.Combobox(
            root, textvariable=self.var_lang,
            values=self.loc.available_languages(),
            state="readonly", width=10
        )
        self.cmb_lang.bind("<<ComboboxSelected>>", self._on_lang_change)

        # Input
        self.lbl_input = ttk.Label(root)
        self.ent_input = ttk.Entry(root, textvariable=self.var_input, width=28)

        # Precision
        self.lbl_precision = ttk.Label(root)
        self.spn_precision = ttk.Spinbox(root, from_=0, to=5, textvariable=self.var_precision, width=5)

        # Both roots
        self.chk_both = ttk.Checkbutton(root, variable=self.var_both)

        # Button
        self.btn_calc = ttk.Button(root, command=self._on_calculate)

        # Result
        self.lbl_result = ttk.Label(root)
        self.txt_result = tk.Text(root, width=34, height=4, wrap="word")
        self.txt_result = tk.Text(root, width=34, height=4, wrap="word")
        self.txt_result.configure(
            bg=self._dark_entry,
            fg=self._dark_fg,
            insertbackground=self._dark_fg,
            highlightbackground=self._dark_border,
            highlightcolor=self._dark_border,
            relief="flat",
        )
        self.txt_result.configure(state="disabled")

        self.txt_result.configure(state="disabled")

        # Layout
        self.lbl_lang.grid(row=0, column=0, sticky="w")
        self.cmb_lang.grid(row=0, column=1, sticky="e")

        self.lbl_input.grid(row=1, column=0, sticky="w", pady=(pad, 0))
        self.ent_input.grid(row=1, column=1, sticky="e", pady=(pad, 0))

        self.lbl_precision.grid(row=2, column=0, sticky="w", pady=(pad, 0))
        self.spn_precision.grid(row=2, column=1, sticky="e", pady=(pad, 0))

        self.chk_both.grid(row=3, column=0, columnspan=2, sticky="w", pady=(pad, 0))

        self.btn_calc.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(pad, 0))

        self.lbl_result.grid(row=5, column=0, sticky="w", pady=(pad, 0))
        self.txt_result.grid(row=6, column=0, columnspan=2, pady=(0, pad))

    def _apply_language(self):
        t = self.loc.t
        self.lbl_lang.config(text=t("ui_lang"))
        self.lbl_input.config(text=t("ui_input"))
        self.lbl_precision.config(text=t("ui_precision"))
        self.chk_both.config(text=t("ui_both_roots"))
        self.btn_calc.config(text=t("ui_calc"))
        self.lbl_result.config(text=t("ui_result"))
        self.title(t("ui_title"))

    def _set_result(self, text: str):
        self.txt_result.configure(state="normal")
        self.txt_result.delete("1.0", "end")
        self.txt_result.insert("1.0", text)
        self.txt_result.configure(state="disabled")

    def _on_calculate(self):
        precision = int(self.var_precision.get())
        precision = max(0, min(5, precision))
        self.var_precision.set(precision)

        result = self.controller.calculate(
            input_text=self.var_input.get(),
            precision=precision,
            both_roots=bool(self.var_both.get()),
        )
        self._set_result(result)

    def _on_lang_change(self, _event=None):
        self.loc.set_language(self.var_lang.get())
        self._apply_language()

    def _apply_dark_theme(self):

        self._dark_bg = "#1e1e1e"
        self._dark_panel = "#252526"
        self._dark_fg = "#e6e6e6"
        self._dark_muted = "#bdbdbd"
        self._dark_entry = "#2d2d30"
        self._dark_border = "#3c3c3c"

        self.configure(bg=self._dark_bg)

        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(".", background=self._dark_bg, foreground=self._dark_fg)
        style.configure("TFrame", background=self._dark_bg)
        style.configure("TLabel", background=self._dark_bg, foreground=self._dark_fg)

        style.configure(
            "TButton",
            background=self._dark_panel,
            foreground=self._dark_fg,
            bordercolor=self._dark_border,
            focusthickness=2,
            focuscolor=self._dark_border,
            padding=6,
        )
        style.map(
            "TButton",
            background=[("active", self._dark_entry)],
        )

        style.configure(
            "TCheckbutton",
            background=self._dark_bg,
            foreground=self._dark_fg,
        )

        style.configure(
            "TEntry",
            fieldbackground=self._dark_entry,
            foreground=self._dark_fg,
            insertcolor=self._dark_fg,
            bordercolor=self._dark_border,
            lightcolor=self._dark_border,
            darkcolor=self._dark_border,
        )

        style.configure(
            "TSpinbox",
            fieldbackground=self._dark_entry,
            foreground=self._dark_fg,
            insertcolor=self._dark_fg,
            bordercolor=self._dark_border,
        )

        style.configure(
            "TCombobox",
            fieldbackground=self._dark_entry,
            foreground=self._dark_fg,
            arrowcolor=self._dark_fg,
            bordercolor=self._dark_border,
        )
if __name__ == "__main__":
    setup_logging()
    App().mainloop()
