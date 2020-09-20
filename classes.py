import math
import random

from settings import pg, SOURCE_DIR, SUITS, RANKS, CARD_W, CARD_H, DECK_PLACE, STORAGE_PLACE, PLACE_COLOR, \
    CARDS_COUNT, RED_SUITS, BLACK_SUITS


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
        self.rect = self._images[self.SHIRT_STATE].get_rect()
        self.state = self.SHIRT_STATE
        self.z = 0

    @property
    def image(self):
        return self._images[self.state]

    def turn(self):
        self.state = {self.FACE_STATE: self.SHIRT_STATE, self.SHIRT_STATE: self.FACE_STATE}[self.state]


class Deck:

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        self.place_rect = pg.Rect(*DECK_PLACE, CARD_W, CARD_H)
        random.shuffle(self.cards)
        for z, card in enumerate(self.cards, 0):
            card.z = z
            card.rect.x, card.rect.y = DECK_PLACE

    def draw_place(self, surface):
        if self.cards:
            return
        pg.draw.rect(surface, PLACE_COLOR, self.place_rect)

    def is_click(self, x_click, y_click):
        return self.place_rect.collidepoint(x_click, y_click)

    def get_card(self):
        return self.cards.pop()

    def accept_card(self, card):
        card.z = len(self.cards)
        self.cards.append(card)

    @property
    def empty(self):
        return len(self.cards) == 0

    def coords_for_append(self):
        return self.place_rect.x, self.place_rect.y


class Storage:

    def __init__(self):
        self.cards = []
        self.place_rect = pg.Rect(*STORAGE_PLACE, CARD_W, CARD_H)

    def draw_place(self, surface):
        if self.cards:
            return
        pg.draw.rect(surface, PLACE_COLOR, self.place_rect)

    def is_click(self, x_click, y_click):
        return self.place_rect.collidepoint(x_click, y_click)

    def get_card(self):
        return self.cards.pop()

    def accept_card(self, card):
        card.z = len(self.cards)
        self.cards.append(card)

    @property
    def empty(self):
        return len(self.cards) == 0

    def coords_for_append(self):
        return self.place_rect.x, self.place_rect.y


class WorkPool:

    def __init__(self, x, y):
        self.cards = []
        self.place_rect = pg.Rect(x, y, CARD_W, CARD_H)

    def draw_place(self, surface):
        if self.cards:
            return
        pg.draw.rect(surface, PLACE_COLOR, self.place_rect)

    def is_click(self, x_click, y_click):
        if self.empty:
            return self.place_rect.collidepoint(x_click, y_click)
        for card in self.cards:
            if card.state == Card.SHIRT_STATE:
                continue
            if card.rect.collidepoint(x_click, y_click):
                return True
        return False

    def accept_card(self, card):
        _, line_for_append = self.coords_for_append()
        card.z = len(self.cards)
        card.rect.y = line_for_append
        self.cards.append(card)

    @property
    def empty(self):
        return len(self.cards) == 0

    def coords_for_append(self, count=None):
        if count is None:
            count = len(self.cards)
        return self.place_rect.x, self.place_rect.y + (CARD_H // 3) * count

    def get_cards_for_click(self, x_click, y_click):
        last_card_index = None
        for index in range(len(self.cards)):
            card = self.cards[index]
            if card.state == Card.SHIRT_STATE:
                continue
            if card.rect.collidepoint(x_click, y_click):
                last_card_index = index
        result = self.cards[last_card_index:]
        self.cards[last_card_index:] = []
        return result

    @property
    def last_card(self):
        return self.cards[-1]

    @property
    def size(self):
        return len(self.cards)


class FinalPool:

    def __init__(self, x, y):
        self.cards = []
        self.place_rect = pg.Rect(x, y, CARD_W, CARD_H)

    def draw_place(self, surface):
        if self.cards:
            return
        pg.draw.rect(surface, PLACE_COLOR, self.place_rect)

    def is_click(self, x_click, y_click):
        return self.place_rect.collidepoint(x_click, y_click)

    def get_card(self):
        return self.cards.pop()

    def accept_card(self, card):
        card.z = len(self.cards)
        self.cards.append(card)

    @property
    def empty(self):
        return len(self.cards) == 0

    def coords_for_append(self):
        return self.place_rect.x, self.place_rect.y

    @property
    def last_card(self):
        return self.cards[-1]


class Animation:
    SPEED_1 = 25
    SPEED_2 = 50
    SPEED_3 = 75

    def __init__(self, card, x_final, y_final, destination, delay=0, turn=False):
        self.card = card
        self.card.z += CARDS_COUNT
        x0, y0 = card.rect.x, card.rect.y
        r = math.sqrt((x0 - x_final) ** 2 + (y0 - y_final) ** 2)
        if r < (CARD_H * 2):
            steps_count = r / self.SPEED_1
        elif CARD_H <= r <= (CARD_H * 4):
            steps_count = r / self.SPEED_2
        else:
            steps_count = r / self.SPEED_3

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

        # Добавляем обработку передачи объекту назначения
        self.steps.append(dict(type='final', destination=destination))

    def next_step(self):
        if self.stop:
            return

        step = self.steps.pop(0)
        if step['type'] == 'offset':
            self.card.rect.x, self.card.rect.y = step['x'], step['y']
        elif step['type'] == 'turn':
            self.card.turn()
        elif step['type'] == 'final':
            step['destination'].accept_card(self.card)

    @property
    def stop(self):
        return not self.steps


class Drag:

    def __init__(self, storage, work_pools, final_pools, animations):
        self.cards = []
        self.source_place = None

        self.storage = storage
        self.work_pools = work_pools
        self.final_pools = final_pools
        self.animations = animations

    def accept(self, x_click, y_click):
        # Ищем место, на котором был сделан щелчок мышью
        # Проверяем хранилище
        if not self.storage.empty and self.storage.is_click(x_click, y_click):
            card = self.storage.get_card()
            card.z += CARDS_COUNT
            self.cards = [card]
            self.source_place = self.storage
            return

        # Проверяем конечные пулы
        for pool in self.final_pools:
            if pool.empty:
                continue
            if pool.is_click(x_click, y_click):
                card = pool.get_card()
                card.z += CARDS_COUNT
                self.cards = [card]
                self.source_place = pool
                return

        # Проверяем пулы с цепочками карт - "рабочие" пулы
        for pool in self.work_pools:
            if pool.empty:
                continue
            if pool.is_click(x_click, y_click):
                self.cards = pool.get_cards_for_click(x_click, y_click)
                for card in self.cards:
                    card.z += CARDS_COUNT
                self.source_place = pool
                return

    def move(self, dx, dy):
        if not self.cards:
            return
        for card in self.cards:
            card.rect.move_ip((dx, dy))

    def drop(self):
        if not self.cards:
            return

        # Проверяем, куда мы пытаемся положить карты
        # Сперва ищем угловые точки переносимых карт
        anchor_points = self._create_anchor_points()

        # Формируем список пулов под угловыми точками
        anchor_pools = []
        for x_anchor, y_anchor in anchor_points:
            pool = self._get_pool_for_point(x_anchor, y_anchor)
            if pool:
                anchor_pools.append(pool)

        # Ищем среди найденных пулов первый, который допускает перемещение карт в него
        destination_place = None
        for pool in anchor_pools:
            if self._check_pool_for_append_card(pool):
                destination_place = pool
                break

        # Создаем анимации перемещения карт
        if destination_place:
            # Если пул назначения существует, то перемещаем карты в него
            animations = self._create_animations(destination_place)

            # Если нужно - переворачиваем последнюю карту в "рабочем" пуле
            if isinstance(self.source_place, WorkPool) and not self.source_place.empty:
                if self.source_place.last_card.state == Card.SHIRT_STATE:
                    self.source_place.last_card.turn()
        else:
            # Если пул назначения не существует, то перемещаем карты в тот пул, из которого они были взяты
            animations = self._create_animations(self.source_place)

        self.animations.extend(animations)
        self.cards = []

    def _create_anchor_points(self):
        anchor_rect = self.cards[0].rect.copy()
        anchor_rect.unionall_ip([card.rect for card in self.cards])
        return [
            (anchor_rect.x, anchor_rect.y),
            anchor_rect.topright,
            anchor_rect.bottomright,
            anchor_rect.bottomleft
        ]

    def _get_pool_for_point(self, x, y):
        for pool in self.work_pools + self.final_pools:
            if pool.is_click(x, y):
                return pool
        return None

    def _check_pool_for_append_card(self, pool):
        card = self.cards[0]

        if isinstance(pool, WorkPool):
            if pool.empty:
                if card.rank != 'K':
                    return False
            else:
                if card.rank == 'A':
                    return False
                rank_diff = RANKS.index(pool.last_card.rank) - RANKS.index(card.rank)
                last_card_in_red = pool.last_card.suit in RED_SUITS
                last_card_in_black = pool.last_card.suit in BLACK_SUITS
                card_in_red = card.suit in RED_SUITS
                card_in_black = card.suit in BLACK_SUITS
                if rank_diff != 1:
                    return False
                if not ((last_card_in_red and card_in_black) or (last_card_in_black and card_in_red)):
                    return False

            return True

        elif isinstance(pool, FinalPool):
            if len(self.cards) > 1:
                return False
            if pool.empty:
                if card.rank != 'A':
                    return False
            else:
                rank_diff = RANKS.index(card.rank) - RANKS.index(pool.last_card.rank)
                if rank_diff != 1:
                    return False
                if pool.last_card.suit != card.suit:
                    return False

            return True

    def _create_animations(self, destination_place):
        result = []
        if isinstance(destination_place, WorkPool):
            count = destination_place.size + 1
            for card in self.cards:
                coords_for_append = destination_place.coords_for_append(count=count)
                result.append(Animation(card, *coords_for_append, destination_place))
                count += 1

        elif isinstance(destination_place, FinalPool) or isinstance(destination_place, Storage):
            card = self.cards[0]
            coords_for_append = destination_place.coords_for_append()
            result.append(Animation(card, *coords_for_append, destination_place))

        return result
