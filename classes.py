import math

from settings import pg, SOURCE_DIR, SUITS, RANKS


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


class Deck:

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]


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
