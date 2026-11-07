from flet import *
from widgets import *
import asyncio

from views import *


def mode(e: ControlEvent):
    if e.control.icon == Icons.LIGHT_MODE_ROUNDED:
        e.control.icon = Icons.DARK_MODE_ROUNDED
        e.page.theme_mode = ThemeMode.LIGHT
    else:
        e.control.icon = Icons.LIGHT_MODE_ROUNDED
        e.page.theme_mode = ThemeMode.DARK
        
    pass


def Home():
    view = View(
        appbar = AppBar(
            title = "Vusto",
            leading = IconButton(
                icon = Icons.MENU_ROUNDED,
                on_click = lambda _: asyncio.create_task(_.page.show_drawer())
            ),
        ),
        controls = [
            tabs_bar
        ],
        padding = 5,
        drawer = NavigationDrawer(
            controls = [
                Shimmer(
                    base_color = CLASSIC_COLOR,
                    highlight_color = GOLD,
                    content = Container(
                        # height = 361,
                        border_radius = BorderRadius.only(bottom_right = 19),
                        padding = 10,
                        content = ListTile(
                            title = Text("Ассалому алейкум", size = 19),
                            subtitle = "14 Jumad 1 1448",
                            trailing = IconButton(Icons.LIGHT_MODE_ROUNDED, on_click = mode, tooltip = Tooltip("Шаб ё Рӯз"))   
                        )
                    ),
                ),
                NavigationDrawerDestination(
                    label = "Намозҳо",
                    icon = Image(src = "images/home.png", width = 40, height = 40),
                ),
                NavigationDrawerDestination(
                    label = "Қуръон",
                    icon = Image(src = "images/quran.png", width = 40, height = 40),
                ),
                NavigationDrawerDestination(
                    label = "Зикр",
                    icon = Image(src = "images/zikr.png", width = 40, height = 40),
                ),
                NavigationDrawerDestination(
                    label = "Ҳадис",
                    icon = Image(src = "images/hadith.png", width = 40, height = 40),
                ),
                Divider(height = 10),
                NavigationDrawerDestination(
                    label = "Бештар",
                    icon = Image(src = "images/settings.png", width = 40, height = 40),
                )
            ],
            tile_padding = 5,
            on_change = change_page,
            width = 361
            
        ),
        expand = True
    )
    
    return view