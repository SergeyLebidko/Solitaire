from settings import pg, W, H, SUITS, RANKS
from classes import Card


def create_deck():
    return [Card(rank, suit) for suit in SUITS for rank in RANKS]


def draw_background(surface):
    step = 100
    colors = [(20, 130, 30), (20, 120, 30)]
    for x in range(0, W, step):
        for y in range(0, H, step):
            pg.draw.rect(surface, colors[(x // step + y // step) % 2], (x, y, step, step))


def draw_cards(surface, cards):
    for card in cards:
        surface.blit(card.image, card.rect)


def refresh_animations(animations):
    for animation in animations:
        animation.next_step()
    return list(filter(lambda x: not x.stop, animations))
