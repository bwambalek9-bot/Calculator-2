"""
Scientific Calculator - Kivy GUI version (Casio fx-991 style)
This is the entry point Buildozer looks for: main.py with a App subclass.
"""

import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton


class CalculatorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.angle_mode = "DEG"
        self.expression = ""

        # Display
        self.display = TextInput(
            text="",
            font_size=32,
            size_hint=(1, 0.2),
            readonly=True,
            halign="right",
            multiline=False,
        )
        self.add_widget(self.display)

        # DEG/RAD toggle
        self.mode_button = ToggleButton(text="DEG", size_hint=(1, 0.08))
        self.mode_button.bind(on_press=self.toggle_mode)
        self.add_widget(self.mode_button)

        # Button grid
        grid = GridLayout(cols=5, size_hint=(1, 0.72))

        buttons = [
            "sin", "cos", "tan", "DEL", "C",
            "asin", "acos", "atan", "(", ")",
            "log", "ln", "√", "^", "/",
            "7", "8", "9", "!", "*",
            "4", "5", "6", "π", "-",
            "1", "2", "3", "e", "+",
            "0", ".", "=", "",  "",
        ]

        for label in buttons:
            if label == "":
                grid.add_widget(Button(text="", disabled=True, opacity=0))
                continue
            btn = Button(text=label, font_size=20)
            btn.bind(on_press=self.on_button_press)
            grid.add_widget(btn)

        self.add_widget(grid)

    def toggle_mode(self, instance):
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        instance.text = self.angle_mode

    def on_button_press(self, instance):
        label = instance.text

        if label == "C":
            self.expression = ""
        elif label == "DEL":
            self.expression = self.expression[:-1]
        elif label == "=":
            self.evaluate()
            return
        elif label == "√":
            self.expression += "sqrt("
        elif label == "π":
            self.expression += "pi"
        elif label == "!":
            self.expression += "factorial("
        elif label in ("sin", "cos", "tan", "asin", "acos", "atan", "log", "ln"):
            self.expression += label + "("
        else:
            self.expression += label

        self.display.text = self.expression

    def evaluate(self):
        expr = self.expression

        # Map calculator functions/names to Python math equivalents
        safe_dict = {
            "sqrt": math.sqrt,
            "factorial": lambda x: math.factorial(int(x)),
            "log": math.log10,
            "ln": math.log,
            "pi": math.pi,
            "e": math.e,
            "sin": self._sin,
            "cos": self._cos,
            "tan": self._tan,
            "asin": self._asin,
            "acos": self._acos,
            "atan": self._atan,
        }

        try:
            result = eval(expr, {"__builtins__": {}}, safe_dict)
            self.expression = str(result)
            self.display.text = self.expression
        except Exception:
            self.display.text = "Error"
            self.expression = ""

    # Trig helpers that respect the DEG/RAD toggle
    def _to_rad(self, x):
        return math.radians(x) if self.angle_mode == "DEG" else x

    def _from_rad(self, x):
        return math.degrees(x) if self.angle_mode == "DEG" else x

    def _sin(self, x):
        return math.sin(self._to_rad(x))

    def _cos(self, x):
        return math.cos(self._to_rad(x))

    def _tan(self, x):
        return math.tan(self._to_rad(x))

    def _asin(self, x):
        return self._from_rad(math.asin(x))

    def _acos(self, x):
        return self._from_rad(math.acos(x))

    def _atan(self, x):
        return self._from_rad(math.atan(x))


class CalculatorApp(App):
    def build(self):
        return CalculatorLayout()


if __name__ == "__main__":
    CalculatorApp().run()
