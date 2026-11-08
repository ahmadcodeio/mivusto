"""
Scientific Calculator built with Flet
Install:  pip install flet
Run:      python calculator.py
"""

import ast
import math
import operator
import re

import flet as ft

# ---------------------------------------------------------------- evaluator
BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}
UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def make_env(degrees: bool):
    to_rad = (lambda x: math.radians(x)) if degrees else (lambda x: x)
    from_rad = (lambda x: math.degrees(x)) if degrees else (lambda x: x)

    def fact(x):
        if x < 0 or int(x) != x:
            raise ValueError("factorial domain")
        return math.factorial(int(x))

    funcs = {
        "sin": lambda x: math.sin(to_rad(x)),
        "cos": lambda x: math.cos(to_rad(x)),
        "tan": lambda x: math.tan(to_rad(x)),
        "asin": lambda x: from_rad(math.asin(x)),
        "acos": lambda x: from_rad(math.acos(x)),
        "atan": lambda x: from_rad(math.atan(x)),
        "sinh": math.sinh,
        "cosh": math.cosh,
        "tanh": math.tanh,
        "log": math.log10,
        "ln": math.log,
        "sqrt": math.sqrt,
        "cbrt": lambda x: math.copysign(abs(x) ** (1 / 3), x),
        "exp": math.exp,
        "abs": abs,
        "fact": fact,
    }
    consts = {"pi": math.pi, "e": math.e, "ans": 0}
    return funcs, consts


def safe_eval(expr: str, degrees: bool, ans: float):
    funcs, consts = make_env(degrees)
    consts["ans"] = ans

    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.Name) and node.id in consts:
            return consts[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in BIN_OPS:
            left, right = ev(node.left), ev(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 10000:
                raise ValueError("exponent too large")
            return BIN_OPS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPS:
            return UNARY_OPS[type(node.op)](ev(node.operand))
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in funcs
            and len(node.args) == 1
        ):
            return funcs[node.func.id](ev(node.args[0]))
        raise ValueError("invalid expression")

    s = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
    s = s.replace("^", "**").replace("π", "pi").replace("√", "sqrt")
    s = s.replace("%", "/100").replace("#", "%")
    # implicit multiplication: 2(3) 2pi (1+2)(3) 3sin(
    s = re.sub(r"(\d|\)|pi)\s*(?=\(|[a-df-zA-Z]|e(?![+\-\d]))", r"\1*", s)
    s = re.sub(r"\)\s*(?=\d)", ")*", s)
    return ev(ast.parse(s, mode="eval"))


def fmt(x) -> str:
    if isinstance(x, int):
        return str(x) if abs(x) < 10**15 else f"{x:.10e}"
    if math.isnan(x) or math.isinf(x):
        raise ValueError("undefined")
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    r = f"{x:.12g}"
    return r


# ---------------------------------------------------------------------- UI
BG = "#17181c"
PANEL = "#1f2127"
NUM = "#2b2e36"
OP = "#ff9f0a"
FUNC = "#3a3f4b"
SPECIAL = "#a5a5a5"
EQ = "#34c759"


def main(page: ft.Page):
    page.title = "Calculator"
    page.bgcolor = BG
    page.padding = 12
    page.window.width = 420
    page.window.height = 780
    page.theme_mode = ft.ThemeMode.DARK

    state = {"expr": "", "degrees": True, "ans": 0.0, "memory": 0.0, "just_eval": False,
             "inv": False, "history": []}

    expr_text = ft.Text("", size=20, color="#9aa0aa", text_align=ft.TextAlign.RIGHT,
                        max_lines=2, overflow=ft.TextOverflow.ELLIPSIS)
    result_text = ft.Text("0", size=46, weight=ft.FontWeight.W_300, color="white",
                          text_align=ft.TextAlign.RIGHT, max_lines=1,
                          overflow=ft.TextOverflow.ELLIPSIS)
    mode_text = ft.Text("DEG", size=12, color=OP, weight=ft.FontWeight.BOLD)
    mem_text = ft.Text("", size=12, color="#9aa0aa")
    history_list = ft.ListView(expand=True, spacing=6, auto_scroll=False)

    # ----- helpers
    def refresh():
        expr_text.value = state["expr"]
        expr_text.update()
        mode_text.value = "DEG" if state["degrees"] else "RAD"
        mem_text.value = "M" if state["memory"] != 0 else ""
        page.update()

    def live_preview():
        if not state["expr"]:
            result_text.value = "0"
            return
        try:
            val = safe_eval(close_brackets(state["expr"]), state["degrees"], state["ans"])
            result_text.value = fmt(val)
        except Exception:
            pass

    def close_brackets(s):
        return s + ")" * max(0, s.count("(") - s.count(")"))

    def add(token):
        if state["just_eval"]:
            # operators continue from the result; anything else starts fresh
            if token in ("+", "-", "×", "÷", "^", "^2", "%", "#", "^(-1)"):
                state["expr"] = result_text.value if result_text.value != "Error" else ""
            else:
                state["expr"] = ""
            state["just_eval"] = False
        state["expr"] += token
        live_preview()
        refresh()

    def clear(_=None):
        state["expr"] = ""
        state["just_eval"] = False
        result_text.value = "0"
        refresh()

    def backspace(_=None):
        if state["just_eval"]:
            return clear()
        s = state["expr"]
        # remove a whole function token like "sin(" at once
        m = re.search(r"(asin|acos|atan|sinh|cosh|tanh|sin|cos|tan|log|ln|sqrt|cbrt|exp|abs|fact|ans)\($|ans$", s)
        state["expr"] = s[: m.start()] if m else s[:-1]
        live_preview()
        if not state["expr"]:
            result_text.value = "0"
        refresh()

    def equals(_=None):
        if not state["expr"]:
            return
        try:
            expr = close_brackets(state["expr"])
            val = safe_eval(expr, state["degrees"], state["ans"])
            out = fmt(val)
            state["history"].insert(0, (expr, out))
            state["ans"] = float(val)
            result_text.value = out
            expr_text.value = expr + " ="
            state["expr"] = out
            state["just_eval"] = True
            update_history()
        except ZeroDivisionError:
            result_text.value = "Error"
            expr_text.value = "Cannot divide by zero"
            state["just_eval"] = True
            state["expr"] = ""
        except Exception:
            result_text.value = "Error"
            expr_text.value = "Invalid input"
            state["just_eval"] = True
            state["expr"] = ""
        page.update()

    def negate(_=None):
        s = state["expr"]
        if not s:
            return
        if state["just_eval"]:
            state["just_eval"] = False
        m = re.search(r"(\d+\.?\d*|pi|π|ans)$", s)
        if m:
            start = m.start()
            if s[:start].endswith("(-"):
                state["expr"] = s[: start - 2] + s[start:]
            else:
                state["expr"] = s[:start] + "(-" + s[start:]
        else:
            state["expr"] = "(-" + s if not s.startswith("(-") else s[2:]
        live_preview()
        refresh()

    def toggle_deg(_=None):
        state["degrees"] = not state["degrees"]
        live_preview()
        refresh()

    def toggle_inv(_=None):
        state["inv"] = not state["inv"]
        for key, (a, b) in INV_PAIRS.items():
            btn = inv_buttons[key]
            btn.content.value = b if state["inv"] else a
        inv_toggle.bgcolor = OP if state["inv"] else FUNC
        page.update()

    def current_value():
        try:
            return safe_eval(close_brackets(state["expr"]), state["degrees"], state["ans"])
        except Exception:
            return None

    def mem(action):
        def handler(_=None):
            if action == "MC":
                state["memory"] = 0.0
            elif action == "MR":
                add(fmt(state["memory"]))
                return
            else:
                v = current_value()
                if v is None:
                    v = float(result_text.value) if result_text.value not in ("Error", "") else 0
                state["memory"] += v if action == "M+" else -v
            refresh()
        return handler

    # ----- history drawer
    def update_history():
        history_list.controls.clear()
        for e, r in state["history"][:50]:
            history_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(e, size=13, color="#9aa0aa", text_align=ft.TextAlign.RIGHT),
                        ft.Text(r, size=20, color="white", text_align=ft.TextAlign.RIGHT),
                    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.END),
                    padding=8, bgcolor=NUM, border_radius=8,
                    on_click=lambda _, rr=r: (close_drawer(), add(rr)),
                )
            )
        if history_list.page:
            history_list.update()

    def clear_history(_=None):
        state["history"].clear()
        update_history()

    def close_drawer(_=None):
        try:
            page.pop_dialog()
        except Exception:
            try:
                page.close(history_dialog)
            except Exception:
                history_dialog.open = False
                page.update()

    history_dialog = ft.AlertDialog(
        title=ft.Row([ft.Text("History"), ft.TextButton("Clear", on_click=clear_history)],
                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        content=ft.Container(content=history_list, width=320, height=420),
        actions=[ft.TextButton("Close", on_click=close_drawer)],
        bgcolor=PANEL,
    )

    def open_history(_=None):
        update_history()
        if hasattr(page, "show_dialog"):
            page.show_dialog(history_dialog)
        else:
            page.open(history_dialog)

    # ----- button factory
    def btn(label, on_click, color=NUM, text_color="white", size=18, store=None):
        t = ft.Text(label, size=size, color=text_color, weight=ft.FontWeight.W_500)
        c = ft.Container(
            content=t, bgcolor=color, border_radius=12, expand=True, height=52,
            alignment=ft.Alignment(0, 0), ink=True, on_click=on_click,
        )
        if store is not None:
            store[label] = c
        return c

    inv_buttons = {}
    INV_PAIRS = {
        "sin": ("sin", "asin"), "cos": ("cos", "acos"), "tan": ("tan", "atan"),
        "log": ("log", "10ˣ"), "ln": ("ln", "eˣ"),
    }

    def trig(name):
        def h(_=None):
            a, b = INV_PAIRS[name]
            tok = {"sin": "sin(", "asin": "asin(", "cos": "cos(", "acos": "acos(",
                   "tan": "tan(", "atan": "atan(", "log": "log(", "10ˣ": "10^(",
                   "ln": "ln(", "eˣ": "exp("}[b if state["inv"] else a]
            add(tok)
        return h

    def inv_btn(name):
        b = btn(INV_PAIRS[name][0], trig(name), FUNC, size=15)
        inv_buttons[name] = b
        return b

    inv_toggle = btn("2nd", toggle_inv, FUNC, size=15)
    deg_btn = btn("Deg/Rad", toggle_deg, FUNC, size=14)

    def row(*controls):
        return ft.Row(list(controls), spacing=8)

    def A(tok):
        return lambda _=None: add(tok)

    rows = [
        row(btn("MC", mem("MC"), FUNC, size=14), btn("MR", mem("MR"), FUNC, size=14),
            btn("M+", mem("M+"), FUNC, size=14), btn("M−", mem("M-"), FUNC, size=14),
            btn("📜", open_history, FUNC, size=16)),
        row(inv_toggle, deg_btn, btn("π", A("π"), FUNC, size=16),
            btn("e", A("e"), FUNC, size=16), btn("Ans", A("ans"), FUNC, size=14)),
        row(inv_btn("sin"), inv_btn("cos"), inv_btn("tan"), inv_btn("log"), inv_btn("ln")),
        row(btn("x²", A("^2"), FUNC, size=15), btn("xʸ", A("^"), FUNC, size=15),
            btn("√", A("sqrt("), FUNC, size=16), btn("∛", A("cbrt("), FUNC, size=16),
            btn("n!", A("fact("), FUNC, size=15)),
        row(btn("1/x", A("^(-1)"), FUNC, size=14), btn("|x|", A("abs("), FUNC, size=15),
            btn("sinh", A("sinh("), FUNC, size=13), btn("cosh", A("cosh("), FUNC, size=13),
            btn("tanh", A("tanh("), FUNC, size=13)),
        row(btn("AC", clear, SPECIAL, "black"), btn("(", A("("), SPECIAL, "black"),
            btn(")", A(")"), SPECIAL, "black"), btn("⌫", backspace, SPECIAL, "black"),
            btn("÷", A("÷"), OP, size=24)),
        row(btn("7", A("7")), btn("8", A("8")), btn("9", A("9")),
            btn("%", A("%"), SPECIAL, "black"), btn("×", A("×"), OP, size=24)),
        row(btn("4", A("4")), btn("5", A("5")), btn("6", A("6")),
            btn("±", negate, SPECIAL, "black"), btn("−", A("-"), OP, size=24)),
        row(btn("1", A("1")), btn("2", A("2")), btn("3", A("3")),
            btn("mod", A("#"), SPECIAL, "black", size=14), btn("+", A("+"), OP, size=24)),
        row(btn("0", A("0")), btn("00", A("00")), btn(".", A(".")),
            btn("=", equals, EQ, size=26)),
    ]
    # the last row has 4 buttons; make "=" twice as wide
    rows[-1].controls[-1].expand = 2

    # ----- keyboard support
    def on_key(e: ft.KeyboardEvent):
        k = e.key
        if k in "0123456789":
            add(k)
        elif k in ("Numpad 0", "Numpad 1", "Numpad 2", "Numpad 3", "Numpad 4",
                   "Numpad 5", "Numpad 6", "Numpad 7", "Numpad 8", "Numpad 9"):
            add(k[-1])
        elif k in (".", "Numpad Decimal", ","):
            add(".")
        elif k in ("+", "Numpad Add"):
            add("+")
        elif k in ("-", "Numpad Subtract"):
            add("-")
        elif k in ("*", "Numpad Multiply", "X"):
            add("×")
        elif k in ("/", "Numpad Divide"):
            add("÷")
        elif k == "^":
            add("^")
        elif k in ("(", ")"):
            add(k)
        elif k == "%":
            add("%")
        elif k in ("Enter", "Numpad Enter", "="):
            equals()
        elif k == "Backspace":
            backspace()
        elif k in ("Escape", "Delete"):
            clear()

    page.on_keyboard_event = on_key

    display = ft.Container(
        content=ft.Column(
            [ft.Row([mode_text, mem_text], spacing=10), expr_text, result_text],
            horizontal_alignment=ft.CrossAxisAlignment.END, spacing=2,
        ),
        bgcolor=PANEL, border_radius=16, padding=16,
        alignment=ft.Alignment(1, 0),
    )

    page.add(
        display,
        ft.Container(height=6),
        ft.Column(rows, spacing=8, expand=True),
    )


if __name__ == "__main__":
    ft.app(target=main)
