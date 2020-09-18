def draw_background(surface):
    surface.fill((20, 120, 30))


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


def draw_animations(animations):
    tmp_animations = []
    while animations:
        animation = animations.pop()
        animation.next_step()
        if not animation.stop:
            tmp_animations.append(animation)
    animations.extend(tmp_animations)
