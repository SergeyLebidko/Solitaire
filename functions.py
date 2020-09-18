def draw_background(surface):
    surface.fill((20, 120, 30))


def draw_cards(surface, cards):
    for card in cards:
        surface.blit(card.image, card.rect)


def draw_animations(animations):
    tmp_animations = []
    while animations:
        animation = animations.pop()
        animation.next_step()
        if not animation.stop:
            tmp_animations.append(animation)
    animations.extend(tmp_animations)
