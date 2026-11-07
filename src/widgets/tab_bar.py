from flet import *

from flet_charts import *
from style.colors import *
from views.zikr import Dhikr

from json import *



import asyncio


def change_page(e):
    index = e.control.selected_index
    e.page.controls.clear()
    e.page.scroll = ScrollMode.HIDDEN
    if index == 0:
        asyncio.create_task(
            e.page.push_route("/zikr-after-prayer")
        )
        pass
    elif index == 1:
        asyncio.create_task(
            e.page.push_route("/qur'an")
        )
        pass
    elif index == 2:
        asyncio.create_task(
            e.page.push_route("/zikr")
        )
        pass
    
    elif index == 3:
        asyncio.create_task(
            e.page.push_route("/hadith")
        )
        pass
    
    e.page.update()


tabs_bar = Container(
    content = Tabs(
        length = 5,
        
        expand = True,
        selected_index = 1,
        
        content = Column(
            expand = True,
            controls = [
                TabBarView(
                    expand = True,
                    controls = [
                        Text("A simple tab Hadith"),
                        Dhikr(),
                        Text("A simple tab Home"),
                        Button(
                            content = "A simple tab Quran",
                            on_click = lambda e: asyncio.create_task(
                                e.page.push_route("/qur'an")
                            )
                        ),
                        Text("A simple tab More"),
                    ],
                ),
                
                TabBar(
                    tab_alignment = TabAlignment.FILL,
                    scrollable = False,
                    tabs = [
                        
                        Tab(
                            label = "Hadith",
                            icon = Icons.LIBRARY_BOOKS_ROUNDED,
                        ),
                        Tab(
                            label = "Azkar",
                            icon = Icons.CHECKLIST_ROUNDED,
                        ),
                        Tab(
                            label = "Home",
                            icon = Icons.MOSQUE_ROUNDED,
                        ),
                        
                        Tab(
                            label = "Quran",
                            icon = Icons.BOOK_ROUNDED,
                        ),
                        Tab(
                            label = "More",
                            icon = Icons.MORE_HORIZ_ROUNDED,
                        ),
                    ]
                ),
            ]
        )
    ),
    expand = True,
    padding = 10
)