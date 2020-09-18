import pygame as pg

W, H = 1180, 792
WINDOW_TITLE = "Solitaire"
FPS = 60

BACKGROUND_COLOR = (20, 120, 30)
PLACE_COLOR = (20, 150, 30)

SOURCE_DIR = 'source/'

RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

# noinspection SpellCheckingInspection
SUITS = 'CBKP'

CARDS_COUNT = len(RANKS) * len(SUITS)
CARD_W, CARD_H = 88, 132

DECK_PLACE = (150, 44)
STORAGE_PLACE = (282, 44)
