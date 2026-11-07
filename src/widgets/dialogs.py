from flet import *
from style.colors import *
import asyncio

dlg_success_zikr = AlertDialog(
    modal = True,
    content = Icon(Icons.CHECK_ROUNDED, size = 114),
    actions = [
        Container(
            content = Text("Home", color = GOLD),

            padding = 14,
            bgcolor = CLASSIC_COLOR,
            border_radius = 14,
            ink = True,
            on_click = lambda e: asyncio.create_task(
                e.page.push_route("/")
            )
        )
    ],
    actions_alignment = MainAxisAlignment.CENTER,
)