import sys

from settings import pg, W, H, WINDOW_TITLE, FPS, WORK_POOLS_LINE, CARD_W
from functions import refresh_animations, draw_cards, draw_background, draw_places
from classes import Deck, Storage, Animation, WorkPool, FinalPool, Drag


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

    # Список рабочих пулов
    work_pools = []
    for index in range(7):
        work_pools.append(WorkPool(150 + index * (3 * CARD_W // 2), WORK_POOLS_LINE))

    # Список пулов назначения
    final_pools = []
    for index in range(4):
        final_pools.append(FinalPool(546 + index * (3 * CARD_W // 2), 44))

    # Список мест на столе, на которых могут лежать карты
    places = [deck, storage]
    places.extend(work_pools)
    places.extend(final_pools)

    # Список активных анимаций
    animations = []

    # Первые анимации - раздача карт в рабочие пулы
    delay = 0
    for number, pool in enumerate(work_pools, 1):
        for index in range(number):
            card = deck.get_card()
            if index == (number - 1):
                animations.append(Animation(card, *pool.coords_for_append(count=index), pool, delay=delay, turn=True))
            else:
                animations.append(Animation(card, *pool.coords_for_append(count=index), pool, delay=delay))
            delay += 4

    # Объект для реализации drag'n'drop
    drag = Drag(storage, work_pools, final_pools, animations)

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if animations:
                continue

            if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
                if deck.is_click(*event.pos):
                    if deck.empty:
                        delay = 0
                        while not storage.empty:
                            card = storage.get_card()
                            animations.append(Animation(card, *deck.coords_for_append(), deck, delay=delay, turn=True))
                            delay += 2
                    else:
                        card = deck.get_card()
                        animations.append(Animation(card, *storage.coords_for_append(), storage, turn=True))
                else:
                    drag.accept(*event.pos)

            if event.type == pg.MOUSEMOTION:
                drag.move(*event.rel)

            if event.type == pg.MOUSEBUTTONUP and event.button == pg.BUTTON_LEFT:
                drag.drop()

        refresh_animations(animations)
        draw_background(sc)
        draw_places(sc, places)
        draw_cards(sc, cards)

        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
