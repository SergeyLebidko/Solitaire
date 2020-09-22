from settings import pg, BACKGROUND_COLOR, CARD_BORDER_COLOR
from classes import Animation, Card


def refresh_animations(animations):
    tmp_animations = []
    while animations:
        animation = animations.pop(0)
        animation.next_step()
        if not animation.stop:
            tmp_animations.append(animation)
    animations.extend(tmp_animations)


def draw_background(surface):
    surface.fill(BACKGROUND_COLOR)


def draw_places(surface, places):
    for place in places:
        place.draw_place(surface)


def draw_cards(surface, cards):
    cards_for_display = {}
    for card in cards:
        coords = card.rect.x, card.rect.y
        card_for_display = cards_for_display.get(coords)
        if (card_for_display and card.z > card_for_display.z) or not card_for_display:
            cards_for_display[coords] = card

    cards_for_display = list(cards_for_display.values())
    cards_for_display.sort(key=lambda x: x.z)

    # Отрисованы будут в конечном итоге только те карты, которые не перекрыты полностью другими картами
    for card in cards_for_display:
        surface.blit(card.image, card.rect)
        pg.draw.rect(surface, CARD_BORDER_COLOR, card.rect, 1)


def deal_cards(deck, work_pools, animations):
    deck.shuffle()
    delay = 0
    for number, pool in enumerate(work_pools, 1):
        for index in range(number):
            card = deck.get_card()
            if index == (number - 1):
                animations.append(Animation(card, *pool.coords_for_append(count=index), pool, delay=delay, turn=True))
            else:
                animations.append(Animation(card, *pool.coords_for_append(count=index), pool, delay=delay))
            delay += 4


def collect_cards(deck, storage, work_pools, final_pools, animations):
    delay = 0
    deck_coords = deck.coords_for_append()
    for pool in [storage] + work_pools + final_pools:
        while not pool.empty:
            card = pool.get_card()
            if card.state == Card.SHIRT_STATE:
                animations.append(Animation(card, *deck_coords, deck, delay=delay))
            else:
                animations.append(Animation(card, *deck_coords, deck, delay=delay, turn=True))
            delay += 4
