from flet import *
from style.colors import *

class CarV(Container):
    def __init__(self, content, padding = 20):
        super().__init__()
        self.bgcolor = Colors.SURFACE
        self.border_radius = 20
        self.padding = padding
        self.margin = 8
        # self.expand = True
        self.shadow = BoxShadow(
            spread_radius = 3,
            blur_radius = 3,
            color = GOLD,
        )
        self.border = Border.all(1, GOLD)
        self.content = content
