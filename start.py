import sys

from settings import pg, W, H, WINDOW_TITLE, FPS
from functions import refresh_animations, draw_cards, draw_background, draw_places
from classes import Deck, Storage, Animation


def main():
    pg.init()
    sc = pg.display.set_mode((W, H))
    pg.display.set_caption(WINDOW_TITLE)
    clock = pg.time.Clock()

    # Колода карт
    deck = Deck()

    # Полный список карт в игре
    cards = deck.cards[:]

    # Хранилище, из которого игрок будет брать карты
    storage = Storage()

    # Список мест на столе, на которых могут лежать карты
    places = [deck, storage]

    # Список активных анимаций
    animations = []

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if animations:
                continue

            if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
                if deck.click(*event.pos):
                    if deck.empty:
                        delay = 0
                        while not storage.empty:
                            card = storage.get_card()
                            animations.append(Animation(card, *deck.coords, deck, delay=delay, turn=True))
                            delay += 2
                    else:
                        card = deck.get_card()
                        animations.append(Animation(card, *storage.coords, storage, turn=True))

        refresh_animations(animations)
        draw_background(sc)
        draw_places(sc, places)
        draw_cards(sc, cards)

        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
