import sys
import math
import random
import pygame as pg

W, H = 1200, 800
WINDOW_TITLE = "Solitaire"
FPS = 60

SOURCE_DIR = 'source/'

RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITS = 'CBKP'


class Card:
    FACE_STATE = 'face'
    SHIRT_STATE = 'shirt'

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self._images = {
            self.FACE_STATE: pg.image.load(f'{SOURCE_DIR}{rank}_{suit}.png'),
            self.SHIRT_STATE: pg.image.load(f'{SOURCE_DIR}shirt.png')
        }
        self.rect = self._images['face'].get_rect()
        self.state = self.FACE_STATE

    @property
    def image(self):
        return self._images[self.state]

    def turn(self):
        self.state = {self.FACE_STATE: self.SHIRT_STATE, self.SHIRT_STATE: self.FACE_STATE}[self.state]


class Animation:
    SPEED = 60

    def __init__(self, card, x_final, y_final, delay=0, turn=False):
        self.card = card
        x0, y0 = card.rect.x, card.rect.y
        r = math.sqrt((x0 - x_final) ** 2 + (y0 - y_final) ** 2)
        steps_count = r / self.SPEED

        # Добавляем задержку (если она есть)
        self.steps = []
        for _ in range(delay):
            self.steps.append(dict(type='offset', x=x0, y=y0))

        # Добавляем координаты отдельных шагов
        if steps_count:
            x, y = x0, y0
            delta_x, delta_y = (x_final - x0) / steps_count, (y_final - y0) / steps_count
            for index in range(int(steps_count) - 1):
                x, y = x + delta_x, y + delta_y
                self.steps.append(dict(type='offset', x=int(x), y=int(y)))
            self.steps.append(dict(type='offset', x=x_final, y=y_final))

        # Добавляем переворот (если нужно)
        if turn:
            self.steps.append(dict(type='turn'))

    def next_step(self):
        if self.stop:
            return

        step = self.steps.pop(0)
        if step['type'] == 'offset':
            self.card.rect.x, self.card.rect.y = step['x'], step['y']
        elif step['type'] == 'turn':
            self.card.turn()

    @property
    def stop(self):
        return not self.steps


def create_deck():
    return [Card(rank, suit) for suit in SUITS for rank in RANKS]


def draw_background(surface):
    colors = [(80, 100, 220), (80, 120, 250)]
    for x in range(0, W, 10):
        for y in range(0, H, 10):
            pg.draw.rect(surface, colors[(x // 10 + y // 10) % 2], (x, y, 10, 10))


def draw_cards(surface, cards):
    for card in cards:
        surface.blit(card.image, card.rect)


def refresh_animations(animations):
    for animation in animations:
        animation.next_step()
    return list(filter(lambda x: not x.stop, animations))


def main():
    pg.init()
    sc = pg.display.set_mode((W, H))
    pg.display.set_caption(WINDOW_TITLE)

    clock = pg.time.Clock()

    deck = create_deck()
    cards = [random.choice(deck)]
    animations = []

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if animations:
                continue

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_LEFT:
                    animations.append(Animation(cards[0], *event.pos))
                if event.button == pg.BUTTON_MIDDLE:
                    animations.append(Animation(cards[0], *event.pos, delay=15))
                if event.button == pg.BUTTON_RIGHT:
                    animations.append(Animation(cards[0], *event.pos, turn=True))

        if animations:
            animations = refresh_animations(animations)

        draw_background(sc)
        draw_cards(sc, cards)
        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
