from flet import *
from widgets import *
from sahih_al_bukhari import Bukhari
import asyncio

bukhari = Bukhari()

random_hadith = bukhari.getRandom()


def getcard():
    card = CarV(
        content = Column(
            controls = [
                
            ]
        )
    )
    
    return card
    pass


hadith_card = CarV(
    content = Column(
        controls = [
            Row(
                controls = [
                    Text("Китоби " + str(random_hadith.chapterId)),
                    Row(
                        controls = [
                            IconButton(Icons.BOOKMARK_ADD_OUTLINED),
                            IconButton(Icons.SHARE_ROUNDED),
                            IconButton(Icons.COPY_ROUNDED),
                            PopupMenuButton(
                                items = [
                                    PopupMenuItem("Хато", Icons.ERROR_ROUNDED)
                                ]
                            )
                        ]
                    ),
                ],
                alignment = MainAxisAlignment.SPACE_BETWEEN
            ),
            Divider(),
            Text("Ҳадиси № - " + str(random_hadith.id)),
            Text(str(random_hadith.arabic)),
            Divider(),
            Text(str(random_hadith.english["text"])),
        ]
    )
)

hadith_card2 = CarV(
    content = Column(
        controls = [
            ListTile(
                title = "Саҳеҳи Бухороӣ",
                leading = Icons.BOOK_ROUNDED,
                on_click = lambda e: asyncio.create_task(
                    e.page.push_route("/hadith/sahih_al_bukhari")
                )
            ),
            ListTile(
                title = "Саҳеҳи Муслим",
                leading = Icons.BOOK_ROUNDED,
            ),
            
        ],
        alignment = MainAxisAlignment.CENTER,
        horizontal_alignment = CrossAxisAlignment.CENTER
    ),
    # padding = 0
)


def favorite(e: Event[ListTile]):
    if e.control.trailing == None:
        e.control.trailing = Icon(Icons.BOOKMARK_ROUNDED)
    else:
        e.control.trailing = None
    pass


def press(e: Event[ListTile]):
    hadith_card3.controls.clear()
    Id = bukhari.get(e.control.leading.value)
    hadith_card3.controls.append(ListTile(title = Id.text))
    
    pass





hadith_card3 = ListView(
    controls = [
        ListTile(
            leading = Text(i.id),
            title = i.english,
            subtitle = i.arabic,
            on_click = lambda e: open_book(e)
        ) for i in bukhari.chapters
    ]
)



def open_book(e: ControlEvent):
    hadith_card3.controls.clear()
    chaps = bukhari.getByChapter(int(e.control.leading.value))
    
    hadith_card3.controls = [
        ListTile(
            leading = Text(h.id),
            title = Text(h.narrator),
            subtitle = Text(h.text, overflow = TextOverflow.ELLIPSIS),
            on_click = lambda e: press(e),
            on_long_press = lambda e: favorite(e),
        ) for h in chaps
    ]
    pass


def HadithChId():
    view = View(
        can_pop = False,
        route = "/hadith/sahih_al_bukhari/view",
        appbar = AppBar(
            leading = IconButton(
                icon = Icons.CHEVRON_LEFT_ROUNDED,
                on_click = lambda e: asyncio.create_task(
                    e.page.push_route("/hadith/sahih_al_bukhari/")
                )
            ),
            title = "Ҳадис",
        ),
    )
    
    # view.controls.append(
        
    # )
    
    
    return view


def Hadith():
    view = View(
        can_pop = False,
        route = "/hadith",
        appbar = AppBar(
            leading = IconButton(
                icon = Icons.CHEVRON_LEFT_ROUNDED,
                on_click = lambda e: asyncio.create_task(
                    e.page.push_route("/")
                )
            ),
            title = "Ҳадис",
        ),
        controls = [
            hadith_card,
            Divider(
                height = 3,
                radius = 10,
                thickness = 3,
                trailing_indent = 60,
                leading_indent = 60
            ),
            hadith_card2,
        ],
        scroll = ScrollMode.HIDDEN
    )
    
    return view


def HadithSahihAlBukhari():
    view = View(
        padding = 0,
        can_pop = False,
        route = "/hadith/sahih_al_bukhari",
        appbar = AppBar(
            leading = IconButton(
                icon = Icons.CHEVRON_LEFT_ROUNDED,
                on_click = lambda e: asyncio.create_task(
                    e.page.push_route("/hadith")
                )
            ),
            title = "Sahih al Bukhari",
            actions = [
                IconButton(Icons.BOOKMARKS_ROUNDED),
                IconButton(Icons.FORMAT_ALIGN_RIGHT_ROUNDED),
                IconButton(Icons.SEARCH_ROUNDED),
            ]
        ),
        controls = [
            hadith_card3
        ],
        horizontal_alignment = CrossAxisAlignment.CENTER,
        spacing = 18,
        scroll = Scrollbar(True, False, 8, 60, True, ScrollbarOrientation.RIGHT)
    )
    
    # return view

    return view