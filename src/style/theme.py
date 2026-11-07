from flet import *
from style.colors import *



theme = Theme(
    color_scheme_seed = "#119933",
    color_scheme = ColorScheme(),
    font_family = "Times New Roman",
    popup_menu_theme = PopupMenuTheme(
        menu_position = PopupMenuPosition.UNDER,
    ),
    text_button_theme = ButtonTheme(
        style = ButtonStyle(
            color = GOLD
        )
    ),
    icon_theme = IconTheme(
        color = GOLD,
        
    ),
    
    icon_button_theme = IconButtonTheme(
        style = ButtonStyle(
            color = "#E9B949",
            side = BorderSide(1.5, "#C9A227"),
            # icon_size = 30,
        )
    ),
    button_theme = ButtonTheme(
        style = ButtonStyle(
            color = "#E9B949",
            side = BorderSide(1.5, "#C9A227"),
            icon_size = 30,
        )
    ),
    text_theme = TextTheme(
        headline_medium = TextStyle(color = "#119933"),
    ),
    list_tile_theme = ListTileTheme(
        icon_color = GOLD,
        # text_color = GOLD,
    ),
    scrollbar_theme = ScrollbarTheme(
        cross_axis_margin = 8,
        main_axis_margin = 6,
        thumb_color = GOLD,
        
        
    ),
    tooltip_theme = TooltipTheme(
        text_style = TextStyle(
            size = 16,
            weight = FontWeight.W_500
        ),
        margin = Margin(0, 5, 0, 10),
        padding = Padding(18, 10, 18, 10),
        decoration = BoxDecoration(
            gradient = LinearGradient(
                colors = [
                    ISLAMIC_GREEN,
                    ISLAMIC_GOLD,
                    # ISLAMIC_GOLD,
                    # ISLAMIC_GREEN,
                    
                ],
                begin = Alignment.TOP_LEFT,
                end = Alignment.BOTTOM_RIGHT
            ),
            # shape = BoxShape.CIRCLE,
            border_radius = 8
        )
    ),
    
)

theme_mode = ThemeMode.DARK