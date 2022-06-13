from time import sleep

import pygame as pg
from pygame.time import wait
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

from utils.colors import *
from utils.utils import load_sprite

pg.init()
screen = pg.display.set_mode((800, 800))
COLOR_INACTIVE = pg.Color(WHITE)
COLOR_ACTIVE = pg.Color(LIGHT)
FONT = pg.font.Font(None, 32)
FONT_register = pg.font.Font(None, 20)
FONT_errors = pg.font.Font(None, 26)
nr_chard = 0


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event, index_pass):
        if event.type == pg.MOUSEBUTTONDOWN:
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
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                if index_pass == 1:
                    self.txt_surface = FONT.render(self.text, True, self.color)
                else:
                    self.txt_surface = FONT.render("*"*len(self.text), True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 22)
        self.rect.w = width

    def draw(self, screen, screen_type):
        # the banner
        sprite = load_sprite("banner", True)
        blit_position = pg.Vector2((200, 200))
        screen.blit(sprite, blit_position)
        # the text
        text = FONT.render("Username: ", True, WHITE)
        screen.blit(text, (280, 420))
        text = FONT.render("Password: ", True, WHITE)
        screen.blit(text, (280, 520))
        if screen_type == "login":
            pg.draw.rect(screen, DARK_SHADE, [320, 650, 100, 45], border_radius=30)
            text = FONT.render("Log In", True, WHITE)
            screen.blit(text, (335, 660))
            text = FONT_register.render("You don't have an account?", True, WHITE)
            screen.blit(text, (240, 720))
            text = FONT_register.render("Register Here", True, (163, 0, 174))
            screen.blit(text, (420, 720))
        else:
            pg.draw.rect(screen, DARK_SHADE, [320, 650, 120, 45], border_radius=30)
            text = FONT.render("Register", True, WHITE)
            screen.blit(text, (335, 660))
            text = FONT_register.render("You already have an account?", True, WHITE)
            screen.blit(text, (240, 720))
            text = FONT_register.render("Login Here", True, (163, 0, 174))
            screen.blit(text, (440, 720))
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 15, self.rect.y + 15))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2, border_radius=30)


def login_menu():
    clock = pg.time.Clock()
    input_box1 = InputBox(280, 450, 400, 50)
    input_box2 = InputBox(280, 550, 400, 50)
    input_boxes = [input_box1, input_box2]
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                col, line = event.pos
                if 320 <= col <= 420 and 650 <= line <= 695:
                    screen.blit(FONT_errors.render("Just a moment...", True, WHITE), (300, 620))
                    pg.display.flip()
                    response = database_login(input_box1.text, input_box2.text)
                    pg.draw.rect(screen, BLACK, [290, 620, 200, 30], border_radius=30)
                    pg.display.flip()
                    if response is not False:
                        screen.blit(FONT_errors.render("Now you are logged in!", True, WHITE), (260, 620))
                        pg.display.flip()
                        sleep(4)
                        print("userul este: ", response)
                        return response
                    screen.blit(FONT_errors.render("Your username or password are not valid!", True, WHITE),(220, 620))
                    pg.display.flip()
                    sleep(4)
                if 420 <= col <= 500 and 720 <= line <= 750:
                    print("Redirect to Register Menu")
                    register_menu()
                    return 0
            index = 1
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event, index)
                index += 1

        for box in input_boxes:
            box.update()

        screen.fill(BLACK)

        for box in input_boxes:
            box.draw(screen, "login")

        pg.display.flip()
        clock.tick(30)


def register_menu():
    clock = pg.time.Clock()
    input_box1 = InputBox(280, 450, 400, 50)
    input_box2 = InputBox(280, 550, 400, 50)
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                col, line = event.pos
                if 320 <= col <= 420 and 650 <= line <= 695:
                    print("Register")
                    response = insert_register(input_box1.text, input_box2.text)
                    print(response)
                    return 0
                if 440 <= col <= 500 and 720 <= line <= 750:
                    print("Register")
                    login_menu()
                    return 0
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill(BLACK)
        for box in input_boxes:
            box.draw(screen, "register")

        pg.display.flip()
        clock.tick(30)


def login_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://DBLicenta:DBLicentaDB@cluster0.nh6uz.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    return client['myFirstDatabase']['user']


def database_login(username, password):
    collection_name = login_database()
    item_details = collection_name.find()
    for item in item_details:
        if item["username"] == username and check_password_hash(item["password"], password):
            return item
    return False


def insert_register(username, password):
    collection_name = login_database()
    user_data = {"username": username,
                 "password": generate_password_hash(password),
                 "games_won": 0,
                 "games_loses": 0,
                 "games_total": 0}
    collection_name.insert_one(user_data)
    return True
