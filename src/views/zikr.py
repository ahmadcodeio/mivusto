from flet import *
from widgets import *
from widgets.scrollbar import scroll_bar
# from flet_charts import *
# # from plyer.platforms.android import vibrator

import asyncio

count_value = 95





divid = Divider(
    height = 20,
    leading_indent = 60,
    trailing_indent = 60,
    radius = 10,
    thickness = 4,
    
)


def click_count(e: ControlEvent, ring: ProgressRing):
    global count_value
    
    count_value += 1
    
    ring.value = count_value / 100
    
    e.control.content = str(count_value)
    dlg_success_zikr.open = False
    e.page.show_dialog(dlg_success_zikr)
    if count_value == 33:
        tile_subhonalloh.disabled = True
        tile_subhonalloh.leading = Icons.CHECK_ROUNDED
        tile_subhonalloh.update()
    elif count_value == 66:
        tile_alhamdulilloh.disabled = True
        tile_alhamdulilloh.leading = Icons.CHECK_ROUNDED
        tile_alhamdulilloh.update()
    elif count_value == 99:
        tile_allohu_akbar.disabled = True
        tile_allohu_akbar.leading = Icons.CHECK_ROUNDED
        tile_allohu_akbar.update()
    elif count_value == 100:
        tile_tavhid.disabled = True
        tile_tavhid.leading = Icons.CHECK_ROUNDED
        e.page.show_dialog(dlg_success_zikr)
        tile_tavhid.update()
        
    
    e.page.update()
    pass



def reset(e: ControlEvent, ring: ProgressRing):
    
    dlg = AlertDialog(
        content = Text("Оё шумо мехоҳед аз 0 оғоз кунед?"),
        actions = [
            TextButton("На", on_click = lambda _: clos()),
            TextButton("Ҳа", on_click = lambda _: rst(e, ring)),
        ]
    )
    def clos():
        dlg.open = False
        pass
    
    e.page.show_dialog(dlg)
    
    def rst(e: ControlEvent, ring: ProgressRing):
        global count_value
        dlg.open = False
        count_value = 0
        ring.value = 0.0

        e.control.content = str(count_value)
        tile_subhonalloh.disabled = False
        tile_alhamdulilloh.disabled = False
        tile_allohu_akbar.disabled = False
        tile_tavhid.disabled = False
        tile_subhonalloh.leading = Icons.CIRCLE_OUTLINED
        tile_alhamdulilloh.leading = Icons.CIRCLE_OUTLINED
        tile_allohu_akbar.leading = Icons.CIRCLE_OUTLINED
        tile_tavhid.leading = Icons.CIRCLE_OUTLINED
        e.page.update()
    pass



ring = ProgressRing(
    value = count_value,
    padding = 19,
    stroke_cap = StrokeCap.ROUND,
    stroke_width = 19,
    size_constraints = BoxConstraints(300, 300),
    year_2023 = False,
    track_gap = 6
)


    
zikr_card = Stack(
    controls = [
        ring,
        TextButton(
            content = str(count_value),
            icon = Icons.ADS_CLICK_ROUNDED,
            style = ButtonStyle(
                icon_size = 60,
                text_style = TextStyle(60)
            ),
            left    = 40,
            right   = 40,
            top     = 40,
            bottom  = 40,
            on_click = lambda _: click_count(_, ring),
            on_long_press = lambda _: reset(_, ring)
        )
    ], expand = True
)
# )



tile_subhonalloh = ListTile(
    leading = Icon(Icons.CIRCLE_OUTLINED),
    title = Text("سبحان الله"),
    subtitle = Text("Субҳоналлоҳ • Поку муназзаҳ аст Аллоҳ."),
    trailing = Text("33"),
)

tile_alhamdulilloh = ListTile(
    leading = Icon(Icons.CIRCLE_OUTLINED),
    title = Text("الحمد لله"),
    subtitle = Text("Алҳамдулиллоҳ • Ҳамду сано Аллоҳро."),
    trailing = Text("33"),
)

tile_allohu_akbar = ListTile(
    leading = Icon(Icons.CIRCLE_OUTLINED),
    title = Text("الله أكبر"),
    subtitle = Text("Аллоҳу Акбар • Аллоҳ бузург аст."),
    trailing = Text("33"),
)

tile_tavhid = ListTile(
    leading = Icon(Icons.CIRCLE_OUTLINED),
    title = Text("Lo iloha illalloh"),
    subtitle = Text("Ло илоҳа иллаллоҳ • Ҳеҷ маъбуде нест ҷуз Аллоҳ."),
    trailing = Text("1"),
)


zikr_card2 = CarV(
    ListView(
        controls = [
            tile_subhonalloh,
            tile_alhamdulilloh,
            tile_allohu_akbar,
            tile_tavhid,
        ]
    ),
    padding = 0
)



tab_0 = Column(
    controls = [
        zikr_card,
        divid,
        zikr_card2
    ],
    expand = True,
    alignment = MainAxisAlignment.START,
    horizontal_alignment = CrossAxisAlignment.CENTER,
    scroll = ScrollMode.HIDDEN
)


def Zikr():
    view = View(
        route = "/zikr-after-prayer",
        appbar = AppBar(
            leading = IconButton(
                icon = Icons.CHEVRON_LEFT_ROUNDED,
                on_click = lambda e: asyncio.create_task(
                    e.page.push_route("/")
                )
            ),
            title = Text("Зикри баъди намоз"),
            actions = [
                PopupMenuButton(
                    items = [
                        PopupMenuItem(content = "Садо", icon = Icons.VOLUME_UP_ROUNDED, checked = True),
                        PopupMenuItem(content = "Ларзиш", icon = Icons.VIBRATION_ROUNDED, checked = True),
                    ]
                )
            ]
        ),
        controls = [
            tab_0
        ],

        vertical_alignment = MainAxisAlignment.START,
        horizontal_alignment = CrossAxisAlignment.CENTER,
    )
    
    return view

categories = {
    "Ҳама": Icons.GRID_VIEW_ROUNDED,
    "Субҳ": Icons.WB_TWILIGHT_ROUNDED,
    "Шом": Icons.WB_SUNNY_ROUNDED,
    "Баъди намоз": Icons.MOSQUE_ROUNDED,
    "Пеш аз хоб": Icons.BEDTIME_ROUNDED,
    "Рӯзона": Icons.WB_SUNNY_ROUNDED,
    "Дуоҳо": Icons.FRONT_HAND_ROUNDED,
    "Истиғфор": Icons.SHIELD_MOON_ROUNDED,
    "Салавот": Icons.AUTO_AWESOME_ROUNDED,
    "Руқия": Icons.SELF_IMPROVEMENT_ROUNDED,
    "Сафар": Icons.FLIGHT,
}


def Dhikr():
    content = Container(
        
        content = Column(
            controls = [
                Column(
                    controls = [
                        Container(content = Text("Dhikr"), padding = 60),
                        SearchBar(
                            controls = [
                            ],
                            view_trailing = IconButton(Icons.CLOSE_ROUNDED),
                            bar_leading = Icon(Icons.SEARCH_ROUNDED),
                            bar_padding = Padding.only(left = 19, right = 19),
                            bar_hint_text = "Ҷӯстӯҷӯи зикр",
                        ),
                        Row(
                            controls = [
                                Chip(
                                    label = Text(str(i)),
                                    selected = True if i == "Ҳама" else False,
                                    leading = Icon(categories[i]),
                                    on_select = print
                                ) for i in categories
                            ],
                            scroll = ScrollMode.ADAPTIVE,
                            spacing = 7
                        ),
                    ]
                ),
                ListView(
                    controls = [
                        ListTile(
                            title = "Astaghfirulloh",
                            subtitle = ListTile(
                                title = "Astaghfirulloh",
                                subtitle = Row(
                                    controls = [
                                        Row(
                                            controls = [
                                                IconButton(Icons.RESTART_ALT_ROUNDED),
                                                IconButton(Icons.COPY_ROUNDED),
                                                IconButton(Icons.SHARE_ROUNDED),
                                                
                                            ]
                                        ),
                                        Button("Add Goal", icon = Icons.ADD_ROUNDED),
                                    ],
                                    alignment = MainAxisAlignment.SPACE_BETWEEN,
                                    spacing = 2
                                ),
                                content_padding = 0
                                
                            ),
                            on_click = print
                            # content_padding = 0
                        ) for i in range(0, 10)
                    ],
                    scroll = scroll_bar
                )
                
                
            ],
            horizontal_alignment = CrossAxisAlignment.CENTER
        ),
        
    )
    
    return content