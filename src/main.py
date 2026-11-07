import asyncio
from flet import *

from widgets.card import *

from style.theme import *
from views import *

from home import *

def main(self: Page):
    self.title = "Vusto" 
    self.theme = theme
    self.theme_mode = theme_mode
    self.route = "/"
    

    def route_change():
        self.views.clear()
        if self.route == "/":
            self.views.append(Home())
            pass
        elif self.route == "/zikr-after-prayer":
            self.views.append(Zikr())
            pass
        elif self.route == "/qur'an":
            self.views.append(Quran())
            pass
        elif self.route == "/prayer" :
            pass
        
        elif self.route == "/more":
            pass
        
        self.update()
        

    async def view_pop(e):
        if e.view is not None:
            print("View pop:", e.view)
            self.views.remove(e.view)
            top_view = self.views[-1]
            await self.push_route(top_view.route)

    self.on_route_change = route_change
    self.on_view_pop = view_pop

    route_change()


if __name__ == "__main__":
    run(main)