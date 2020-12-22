#! /usr/bin/env python3

from collections import deque
import itertools
from typing import Deque, List, Set, Tuple

from utils import get_file_lines


Hand = Deque[int]

def parse_input(raw_data: List[str]) -> Tuple[Hand, Hand]:
    hands: List[Hand] = []
    for line in raw_data:
        if not line:
            continue
        if line.startswith('Player'):
            hands.append(deque())
        else:
            hands[-1].append(int(line))
    return tuple(hands[:2])


def move_cards_to_winner(hand1: Hand, hand2: Hand, winner: int) -> None:
    if winner == 1:
        hand1.append(hand1.popleft())
        hand1.append(hand2.popleft())
    else:
        hand2.append(hand2.popleft())
        hand2.append(hand1.popleft())


def play_highest_card_wins(hand1: Hand, hand2: Hand) -> int:
    winner = 1 if hand1[0] > hand2[0] else 2
    move_cards_to_winner(hand1, hand2, winner)
    return winner


def play_recursive(hand1: Hand, hand2: Hand) -> int:
    def get_sub_hand(hand: Hand) -> Hand:
        return deque(itertools.islice(hand, 1, hand[0]+1))
    previous_hands: Set[Tuple[Hand, Hand]] = set()
    while hand1 and hand2:
        current_decks = (tuple(hand1), tuple(hand2))
        if current_decks in previous_hands:
            return 1
        previous_hands.add(current_decks)

        if hand1[0] >= len(hand1) or hand2[0] >= len(hand2):
            play_highest_card_wins(hand1, hand2)
        else:
            sub_hand1 = get_sub_hand(hand1)
            sub_hand2 = get_sub_hand(hand2)
            winner = play_recursive(sub_hand1, sub_hand2)
            move_cards_to_winner(hand1, hand2, winner)

    return 1 if hand1 else 2


def calc_score(hand: Hand) -> int:
    return sum((i+1)*card for i, card in enumerate(reversed(hand)))


def part1(hand1: Hand, hand2: Hand) -> int:
    hand1, hand2 = hand1.copy(), hand2.copy()
    while hand1 and hand2:
        play_highest_card_wins(hand1, hand2)

    return calc_score(hand1 or hand2)


def part2(hand1: Hand, hand2: Hand) -> int:
    if play_recursive(hand1, hand2) == 1:
        return calc_score(hand1)
    return calc_score(hand2)


if __name__ == '__main__':
    raw_hand1, raw_hand2 = parse_input(get_file_lines())
    print(part1(raw_hand1, raw_hand2))  # 30138
    print(part2(raw_hand1, raw_hand2))  # 31587
