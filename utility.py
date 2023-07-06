
import pyglet
from typing import Optional

def scaleTexture(texture: pyglet.image.Texture, viewport: tuple[int, int]):
    scale = min(viewport[0] / texture.width, viewport[1] / texture.height)
    texture.width *= scale
    texture.height *= scale

    return texture

def createSprite(texture: pyglet.image.Texture, viewport: tuple[int, int] = (0, 0)):
    return pyglet.sprite.Sprite(texture, x=viewport[0], y=viewport[1])
