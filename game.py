
import logging
import pyglet
from scene.boardScene import *

class Game():
    def __init__(self):
        # status da aplicação
        self.__isRunning = False

        # gráficos
        self.__window = gameApp.window
        self.__fpsDisplay = gameApp.fpsDisplay
        self.__fpsDisplay.label.y = self.__window.height - BOARD_Y0

        # cenários
        self.__emptyScene = EmptyScene(self.__window)
        self.__boardScene = BoardScene(self.__window)
        self.__currentScene = self.__emptyScene

    def __setEvents(self):
        self.__window.on_activate = self.on_activate
        self.__window.on_close = self.on_close
        self.__window.on_deactivate = self.on_deactivate
        self.__window.on_draw = self.on_draw
        self.__window.on_hide = self.on_hide
        self.__window.on_key_press = self.on_key_press
        self.__window.on_key_release = self.on_key_release
        self.__window.on_mouse_drag = self.on_mouse_drag
        self.__window.on_mouse_enter = self.on_mouse_enter
        self.__window.on_mouse_leave = self.on_mouse_leave
        self.__window.on_mouse_motion = self.on_mouse_motion
        self.__window.on_mouse_press = self.on_mouse_press
        self.__window.on_mouse_release = self.on_mouse_release
        self.__window.on_mouse_scroll = self.on_mouse_scroll
        self.__window.on_show = self.on_show

    # NOTE: revisão
    def __clearEvents(self):
        self.__currentScene = self.__emptyScene

    def on_activate(self):
        self.__currentScene = self.__boardScene
        self.__currentScene.on_activate()
        self.__window.activate()

    def on_close(self):
        self.__currentScene.on_close()
        self.__window.close()

    def on_deactivate(self):
        self.__currentScene = self.__boardScene
        self.__currentScene.on_deactivate()

    def on_draw(self):
        self.__window.clear()
        scene = self.__currentScene
        scene.on_draw()
        self.__fpsDisplay.draw()

    def on_hide(self):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_enter(self, x, y):
        pass

    def on_mouse_leave(self, x, y):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        scene = self.__currentScene
        scene.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        scene = self.__currentScene
        scene.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        scene = self.__currentScene
        scene.on_mouse_release(x, y, button, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass

    def on_show(self):
        pass

    def run(self):
        if not self.__isRunning:
            self.__isRunning = True
            self.__setEvents()
            # ...
                        
            pyglet.app.run() # importante

            self.__clearEvents() # NOTE: revisar
        
        self.__isRunning = False
