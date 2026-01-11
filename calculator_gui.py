"""
Luxe Calculator - A premium Python GUI calculator with BODMAS support.
"""

import tkinter as tk
from tkinter import font as tkfont
from calculator import calculate, CalculatorError


class LuxeCalculator:
    """Modern GUI Calculator with luxury dark theme."""

    # Color palette
    COLORS = {
        "bg_deep": "#0a0a0c",
        "bg_card": "#121216",
        "bg_display": "#0d0d10",
        "bg_button": "#1e1e24",
        "bg_button_hover": "#2a2a32",
        "bg_function": "#252530",
        "bg_function_hover": "#32323e",
        "accent_gold": "#d4a853",
        "accent_gold_hover": "#e0b860",
        "text_primary": "#ffffff",
        "text_secondary": "#888899",
        "text_tertiary": "#555566",
        "border": "#2a2a35",
        "error": "#e85454",
    }

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Luxe Calculator")
        self.window.configure(bg=self.COLORS["bg_deep"])
        self.window.resizable(False, False)

        # Center window on screen
        window_width = 400
        window_height = 650
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # State
        self.expression = ""
        self.result = "0"
        self.memory = 0.0
        self.last_result = 0.0

        # Setup fonts
        self._setup_fonts()

        # Build UI
        self._build_ui()

        # Keyboard bindings
        self._setup_keyboard()

    def _setup_fonts(self):
        """Configure custom fonts."""
        self.font_brand = tkfont.Font(family="Segoe UI", size=11, weight="normal")
        self.font_expression = tkfont.Font(family="Consolas", size=12)
        self.font_result = tkfont.Font(family="Segoe UI Light", size=42, weight="normal")
        self.font_result_error = tkfont.Font(family="Segoe UI", size=18)
        self.font_memory = tkfont.Font(family="Segoe UI", size=10)
        self.font_button = tkfont.Font(family="Segoe UI", size=18)
        self.font_button_small = tkfont.Font(family="Segoe UI", size=14)

    def _build_ui(self):
        """Build the calculator UI."""
        # Main container with padding
        self.main_frame = tk.Frame(
            self.window,
            bg=self.COLORS["bg_card"],
            padx=24,
            pady=24,
        )
        self.main_frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Header
        self._build_header()

        # Display
        self._build_display()

        # Memory buttons
        self._build_memory_row()

        # Main buttons
        self._build_buttons()

        # Footer
        self._build_footer()

    def _build_header(self):
        """Build header with brand and memory indicator."""
        header = tk.Frame(self.main_frame, bg=self.COLORS["bg_card"])
        header.pack(fill="x", pady=(0, 16))

        # Brand
        brand = tk.Label(
            header,
            text="LUXE",
            font=self.font_brand,
            fg=self.COLORS["text_tertiary"],
            bg=self.COLORS["bg_card"],
        )
        brand.pack(side="left")

        # Memory indicator
        self.memory_frame = tk.Frame(header, bg=self.COLORS["bg_card"])
        self.memory_frame.pack(side="right")

        self.memory_dot = tk.Canvas(
            self.memory_frame,
            width=8,
            height=8,
            bg=self.COLORS["bg_card"],
            highlightthickness=0,
        )
        self.memory_dot.pack(side="left", padx=(0, 4))

        memory_label = tk.Label(
            self.memory_frame,
            text="M",
            font=self.font_memory,
            fg=self.COLORS["text_tertiary"],
            bg=self.COLORS["bg_card"],
        )
        memory_label.pack(side="left")

        self._update_memory_indicator()

    def _build_display(self):
        """Build the calculator display."""
        display_frame = tk.Frame(
            self.main_frame,
            bg=self.COLORS["bg_display"],
            padx=20,
            pady=20,
        )
        display_frame.pack(fill="x", pady=(0, 16))

        # Expression label
        self.expression_label = tk.Label(
            display_frame,
            text="",
            font=self.font_expression,
            fg=self.COLORS["text_secondary"],
            bg=self.COLORS["bg_display"],
            anchor="e",
        )
        self.expression_label.pack(fill="x")

        # Result label
        self.result_label = tk.Label(
            display_frame,
            text="0",
            font=self.font_result,
            fg=self.COLORS["text_primary"],
            bg=self.COLORS["bg_display"],
            anchor="e",
        )
        self.result_label.pack(fill="x", pady=(8, 0))

    def _build_memory_row(self):
        """Build memory function buttons."""
        memory_frame = tk.Frame(self.main_frame, bg=self.COLORS["bg_card"])
        memory_frame.pack(fill="x", pady=(0, 12))

        memory_buttons = [
            ("MC", self._memory_clear),
            ("MR", self._memory_recall),
            ("M+", self._memory_add),
            ("M−", self._memory_subtract),
        ]

        for text, command in memory_buttons:
            btn = tk.Button(
                memory_frame,
                text=text,
                font=self.font_memory,
                fg=self.COLORS["text_secondary"],
                bg=self.COLORS["bg_card"],
                activeforeground=self.COLORS["accent_gold"],
                activebackground=self.COLORS["bg_card"],
                border=0,
                padx=12,
                pady=6,
                cursor="hand2",
                command=command,
            )
            btn.pack(side="left", expand=True)
            self._bind_hover(btn, self.COLORS["bg_card"], self.COLORS["bg_button"])

    def _build_buttons(self):
        """Build the main calculator buttons."""
        buttons_frame = tk.Frame(self.main_frame, bg=self.COLORS["bg_card"])
        buttons_frame.pack(fill="both", expand=True)

        # Button layout
        button_layout = [
            [("AC", "function"), ("+/−", "function"), ("%", "function"), ("÷", "operator")],
            [("7", "number"), ("8", "number"), ("9", "number"), ("×", "operator")],
            [("4", "number"), ("5", "number"), ("6", "number"), ("−", "operator")],
            [("1", "number"), ("2", "number"), ("3", "number"), ("+", "operator")],
            [("0", "number", 2), (".", "number"), ("=", "operator")],
        ]

        for row_idx, row in enumerate(button_layout):
            row_frame = tk.Frame(buttons_frame, bg=self.COLORS["bg_card"])
            row_frame.pack(fill="x", pady=6)

            for item in row:
                text = item[0]
                btn_type = item[1]
                colspan = item[2] if len(item) > 2 else 1

                btn = self._create_button(row_frame, text, btn_type, colspan)
                btn.pack(side="left", expand=True, fill="x", padx=6)

    def _create_button(self, parent, text, btn_type, colspan=1):
        """Create a styled button."""
        # Determine colors based on type
        if btn_type == "operator":
            bg = self.COLORS["accent_gold"]
            fg = self.COLORS["bg_deep"]
            hover_bg = self.COLORS["accent_gold_hover"]
            hover_fg = self.COLORS["bg_deep"]
        elif btn_type == "function":
            bg = self.COLORS["bg_function"]
            fg = self.COLORS["text_secondary"]
            hover_bg = self.COLORS["bg_function_hover"]
            hover_fg = self.COLORS["text_primary"]
        else:  # number
            bg = self.COLORS["bg_button"]
            fg = self.COLORS["text_primary"]
            hover_bg = self.COLORS["bg_button_hover"]
            hover_fg = self.COLORS["text_primary"]

        # Calculate width based on colspan
        width = 4 if colspan == 1 else 10

        btn = tk.Button(
            parent,
            text=text,
            font=self.font_button,
            fg=fg,
            bg=bg,
            activeforeground=hover_fg,
            activebackground=hover_bg,
            border=0,
            width=width,
            height=1,
            pady=14,
            cursor="hand2",
            command=lambda t=text: self._on_button_click(t),
        )

        self._bind_hover(btn, bg, hover_bg)

        return btn

    def _bind_hover(self, widget, normal_bg, hover_bg):
        """Bind hover effects to a widget."""
        widget.bind("<Enter>", lambda e: widget.configure(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.configure(bg=normal_bg))

    def _build_footer(self):
        """Build footer branding."""
        footer = tk.Label(
            self.main_frame,
            text="PRECISION ENGINEERED",
            font=tkfont.Font(family="Segoe UI", size=8),
            fg=self.COLORS["text_tertiary"],
            bg=self.COLORS["bg_card"],
        )
        footer.pack(pady=(16, 0))

    def _setup_keyboard(self):
        """Setup keyboard bindings."""
        self.window.bind("<Key>", self._on_key_press)
        self.window.bind("<Return>", lambda e: self._on_button_click("="))
        self.window.bind("<Escape>", lambda e: self._on_button_click("AC"))
        self.window.bind("<BackSpace>", lambda e: self._backspace())

    def _on_key_press(self, event):
        """Handle keyboard input."""
        key = event.char
        if key.isdigit() or key == ".":
            self._on_button_click(key)
        elif key == "+":
            self._on_button_click("+")
        elif key == "-":
            self._on_button_click("−")
        elif key == "*":
            self._on_button_click("×")
        elif key == "/":
            self._on_button_click("÷")
        elif key == "%":
            self._on_button_click("%")
        elif key in ("=", "\r"):
            self._on_button_click("=")

    def _on_button_click(self, text):
        """Handle button clicks."""
        if text == "AC":
            self._clear()
        elif text == "=":
            self._calculate()
        elif text == "+/−":
            self._negate()
        elif text in ("+", "−", "×", "÷", "%"):
            self._append_operator(text)
        else:
            self._append_digit(text)

    def _append_digit(self, digit):
        """Append a digit to the expression."""
        self.expression += digit
        self._update_display()

    def _append_operator(self, op):
        """Append an operator to the expression."""
        self.expression += op
        self._update_display()

    def _clear(self):
        """Clear the calculator."""
        self.expression = ""
        self.result = "0"
        self._update_display()

    def _backspace(self):
        """Remove the last character."""
        self.expression = self.expression[:-1]
        self._update_display()

    def _negate(self):
        """Negate the current result."""
        if self.result not in ("0", "Error"):
            try:
                value = float(self.result) * -1
                self.result = self._format_result(value)
                self.last_result = value
                self._update_display()
            except ValueError:
                pass

    def _calculate(self):
        """Calculate the expression."""
        if not self.expression:
            return

        # Convert display operators to calculation operators
        calc_expr = (
            self.expression
            .replace("×", "*")
            .replace("÷", "/")
            .replace("−", "-")
        )

        try:
            result = calculate(calc_expr)
            self.last_result = float(result)
            self.result = self._format_result(result)
            self.expression = ""
            self.result_label.configure(
                font=self.font_result,
                fg=self.COLORS["text_primary"]
            )
        except CalculatorError as e:
            self.result = "Error"
            self.result_label.configure(
                font=self.font_result_error,
                fg=self.COLORS["error"]
            )
        except Exception:
            self.result = "Error"
            self.result_label.configure(
                font=self.font_result_error,
                fg=self.COLORS["error"]
            )

        self._update_display()

    def _format_result(self, num):
        """Format the result for display."""
        if isinstance(num, int):
            return str(num)

        # Handle floats
        if abs(num) >= 1e9:
            return f"{num:.4e}"

        # Remove trailing zeros
        formatted = f"{num:.10g}"
        return formatted

    def _memory_clear(self):
        """Clear memory."""
        self.memory = 0.0
        self._update_memory_indicator()

    def _memory_recall(self):
        """Recall memory value."""
        if self.memory != 0:
            mem_str = self._format_result(self.memory)
            self.expression += mem_str
            self._update_display()

    def _memory_add(self):
        """Add to memory."""
        self.memory += self.last_result
        self._update_memory_indicator()

    def _memory_subtract(self):
        """Subtract from memory."""
        self.memory -= self.last_result
        self._update_memory_indicator()

    def _update_memory_indicator(self):
        """Update the memory indicator dot."""
        self.memory_dot.delete("all")
        if self.memory != 0:
            self.memory_dot.create_oval(
                1, 1, 7, 7,
                fill=self.COLORS["accent_gold"],
                outline=""
            )

    def _update_display(self):
        """Update the display labels."""
        self.expression_label.configure(text=self.expression)
        self.result_label.configure(text=self.result)

    def run(self):
        """Start the calculator."""
        self.window.mainloop()


def main():
    """Main entry point."""
    calculator = LuxeCalculator()
    calculator.run()


if __name__ == "__main__":
    main()
