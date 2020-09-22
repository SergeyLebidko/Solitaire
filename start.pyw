import sys

from settings import pg, W, H, WINDOW_TITLE, FPS, CARD_W, WORK_POOLS_ANCHOR, FINAL_POOLS_ANCHOR, CARDS_COUNT
from functions import refresh_animations, draw_cards, draw_background, draw_places, deal_cards, collect_cards
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
    work_pools, work_pools_x_start, work_pools_y_start = [], *WORK_POOLS_ANCHOR
    for index in range(7):
        work_pools.append(WorkPool(work_pools_x_start + index * (3 * CARD_W // 2), work_pools_y_start))

    # Список пулов назначения
    final_pools, final_pool_x_start, final_pools_y_start = [], *FINAL_POOLS_ANCHOR
    for index in range(4):
        final_pools.append(FinalPool(final_pool_x_start + index * (3 * CARD_W // 2), final_pools_y_start))

    # Список мест на столе, на которых могут лежать карты
    places = [deck, storage]
    places.extend(work_pools)
    places.extend(final_pools)

    # Список активных анимаций
    animations = []

    # Первые анимации - раздача карт в рабочие пулы
    deal_cards(deck, work_pools, animations)

    # Объект для реализации drag'n'drop
    drag = Drag(storage, work_pools, final_pools, animations)

    # Флаг раздачи карт после завершения всех анимаций
    deal_after_animations = False

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if animations:
                continue

            # Если нажата клавиша "Пробел", то собираем карты, перемешиваем колоду и создаем новую раскладку
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                collect_cards(deck, storage, work_pools, final_pools, animations)
                deal_after_animations = True

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
        if not animations and deal_after_animations:
            deal_cards(deck, work_pools, animations)
            deal_after_animations = False

        draw_background(sc)
        draw_places(sc, places)
        draw_cards(sc, cards)

        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
