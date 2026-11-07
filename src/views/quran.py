from flet import *
from style import *
import asyncio

def Quran():
    view = View(
        route = "/qur'an",
        appbar = AppBar(
            leading = IconButton(
                icon = Icons.CHEVRON_LEFT_ROUNDED,
                on_click = lambda e: asyncio.create_task(
                    e.page.push_route("/")
                )
            ),
        ),
        controls = [
            PageView(
                expand = True,
                horizontal = True,
                reverse = True,
                selected_index = 600,
                viewport_fraction = 1,
                controls = [
                    Container(
                        bgcolor = EMERALD,
                        border = Border.symmetric(
                            horizontal = BorderSide(2.0, Colors.SURFACE)
                        ),
                        content = Column(
                            alignment = MainAxisAlignment.CENTER,
                            horizontal_alignment = CrossAxisAlignment.CENTER,
                            controls = [
                                Text(f"Page {i}", size = 57, weight = FontWeight.BOLD)
                            ]
                        ),
                    ) for i in range(1, 604 + 1)
                ]
            )
        ]
    )
    
    return view
    pass