class ClickableOptionButton():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, WINDOW, rect=False, transform=False):
        WINDOW.blit(self.image, self.rect)

    # MAKE MORE GENERIC, WILL NEVER NEED A CLICKABLE BUTTON FOR DRAWING CARD, THIS WAS WRITTEN FOR TESTING PURPOSES ONLY
    def doclicked(self):
        return False

    def setImage(self, image):
        self.image = image