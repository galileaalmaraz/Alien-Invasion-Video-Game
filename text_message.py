import pygame


def mktext(text, font, color):
    """Render a text.

    Parameters
    ----------
    text : str
    font : tuple (font object, size)
    """
    return font.render(text, True, color)


class Message(pygame.sprite.Sprite):
    """A simple text message sprite.

    Message(pos, text="", font=params.BODY_FONT) -> Message

    Parameters
    ----------
    pos : (float, float)
    text : str
    font : (font object, size)
        Default is BODY_FONT.
    """

    image = None
    rect = None

    def __init__(self, pos, text, font, color):
        super().__init__()
        self._text = text
        self.font = font
        self.image = mktext(text, font, color)
        self.pos = pos

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text
        self.image = mktext(text, self.font)

    text = property(get_text, set_text)

    def blitme(self, screen):
        screen.blit(self.image, self.pos)
