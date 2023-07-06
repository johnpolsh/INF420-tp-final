
import abc
import logging
import pyglet
from utility import *

class SceneElement(abc.ABC):
    def __init__(self, sprite=None):
        self.__sprite = sprite

    @property
    @abc.abstractmethod
    def sprite(self):
        if not self.__sprite:
            raise RuntimeError("scene element does not have an associated sprite")
        
        return self.__sprite

    @abc.abstractmethod
    def batchToScene(self, batch, group):
        sprite = self.sprite
        sprite.batch = batch
        sprite.group = group
    
    @abc.abstractmethod
    def delete(self):
        self.sprite.delete()
        self.__sprite = None

class Scene(abc.ABC):
    FOREGROUND = 'foreground'
    BACKGROUND = 'background'

    def __init__(self, parentWnd: pyglet.window.Window):
        self.parentWnd = parentWnd
        self.__elements = []
        self.batch = pyglet.graphics.Batch()
        self.__groupId = 1
        self.__groups = {
            self.BACKGROUND: pyglet.graphics.Group(0),
            self.FOREGROUND: pyglet.graphics.Group(32)
        }

    def addElement(self, e: SceneElement, group=FOREGROUND):
        if e not in self.__elements:
            if group not in self.__groups:
                raise RuntimeError(f"key {group} group is not in the scene batch groups")

            e.batchToScene(self.batch, self.__groups[group])
            self.__elements.append(e)

    def registerGroup(self, key: str):
        if self.__groupId > 31:
            raise Exception("the number of groups for this scene exceeded the maximum")

        if key not in self.__groups:
            self.__groups[key] = pyglet.graphics.Group(self.__groupId)
            self.__groupId += 1

    def getGroup(self, id: str):
        return self.__groups[id]

    def removeElement(self, e: SceneElement):
        self.__elements.remove(e)
        e.batchToScene(None, None)

    @abc.abstractmethod
    def on_activate(self):
        pass

    @abc.abstractmethod
    def on_deactivate(self):
        pass

    @abc.abstractmethod
    def on_close(self):
        pass

    @abc.abstractmethod
    def on_draw(self):
        pass

    @abc.abstractmethod
    def on_mouse_motion(self, x, y, dx, dy):
        pass

    @abc.abstractmethod
    def on_mouse_press(self, x, y, button, modifiers):
        pass

    @abc.abstractmethod
    def on_mouse_release(self, x, y, button, modifiers):
        pass

    @abc.abstractmethod
    def update(self):
        pass

class EmptyScene(Scene):
    def __init__(self, parentWnd: pyglet.window.Window):
        super().__init__(parentWnd=parentWnd)
    
    def __debug(self, handler):
        logging.debug(f"empty scene handler {handler.__name__} called on parent window {self.parentWnd}")

    def on_activate(self):
        self.__debug(self.on_activate)

    def on_deactivate(self):
        self.__debug(self.on_deactivate)

    def on_close(self):
        self.__debug(self.on_close)

    def on_draw(self):
        self.__debug(self.on_draw)

    def on_mouse_motion(self, x, y, dx, dy):
        self.__debug(self.on_mouse_motion)

    def on_mouse_press(self, x, y, button, modifiers):
        self.__debug(self.on_mouse_press)

    def on_mouse_release(self, x, y, button, modifiers):
        self.__debug(self.on_mouse_release)

    def update(self):
        self.__debug(self.update)
