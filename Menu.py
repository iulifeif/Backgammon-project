import pygame as pg
from pymongo import MongoClient

from utils.colors import *
from utils.utils import load_sprite

pg.init()
# screen = pg.display.set_mode((800, 800))
COLOR_INACTIVE = pg.Color(WHITE)
COLOR_ACTIVE = pg.Color(LIGHT)
FONT = pg.font.Font(None, 32)


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            col, line = event.pos
            # check if login button is pressed
            if 320 <= col <= 420 and 650 <= line <= 695:
                print("1")
                get_database()
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 22)
        self.rect.w = width

    def draw(self, screen):
        # the banner
        sprite = load_sprite("banner", True)
        blit_position = pg.Vector2((200, 200))
        screen.blit(sprite, blit_position)
        # the text
        text = FONT.render("Username: ", True, WHITE)
        screen.blit(text, (280, 420))
        text = FONT.render("Password: ", True, WHITE)
        screen.blit(text, (280, 520))
        pg.draw.rect(screen, DARK_SHADE, [320, 650, 100, 45], border_radius=30)
        text = FONT.render("Log In", True, WHITE)
        screen.blit(text, (335, 660))
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 15, self.rect.y + 15))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2, border_radius=30)


def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(280, 450, 400, 50)
    input_box2 = InputBox(280, 550, 400, 50)
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://DBLicenta:DBLicentaDB@cluster0.nh6uz.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    return client['myFirstDatabase']


if __name__ == '__main__':
    dbname = get_database()
    collection_name=dbname["user"]
    item_details = collection_name.find()
    for item in item_details:
        # This does not give a very readable output
        print(item)
    # print(dbname)
    # main()
    # pg.quit()
