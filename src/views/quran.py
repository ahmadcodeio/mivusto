from flet import *
from style import *
import asyncio


play_bar = Column(
    spacing = 6,
    controls = [
        Row(
            controls = [
                Text("00:00"),
                Slider(
                    expand = True,
                    value = 0.57,
                ),
                Text("19:57"),
                
            ],
            spacing = 1,
            alignment = MainAxisAlignment.CENTER
        ),
        Row(
            controls = [
                IconButton(Icons.SKIP_PREVIOUS_ROUNDED),
                IconButton(Icons.PLAY_ARROW_ROUNDED, width = 80, height = 80),
                IconButton(Icons.SKIP_NEXT_ROUNDED),
                
            ],
            spacing = 3,
            alignment = MainAxisAlignment.CENTER,
            vertical_alignment = CrossAxisAlignment.CENTER
        )

    ]
)

page_view = PageView(
    expand = True,
    horizontal = True,
    reverse = True,
    selected_index = 600,
    viewport_fraction = 1,
    controls = [
        Container(
            bgcolor = Colors.SURFACE_CONTAINER_LOW,
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
            page_view,
        ]
    )
    
    return view
    pass