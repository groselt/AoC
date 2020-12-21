#! /usr/bin/env python3

import copy
from typing import Dict, List, Set, Tuple

from utils import get_file_lines


class Food:  # pylint: disable=too-few-public-methods
    def __init__(self, line: str):
        ingredients, allergens = line.split(' (contains ')
        self.ingredients = ingredients.split()
        self.allergens = allergens[:-1].split(', ')


def get_definite_allergens(all_food: List[Food]) -> List[Tuple[str, str]]:  # [(ingr, allergen)]
    allergen_candidates: Dict[str, Set[str]] = dict()  # { allergen : [ingredients] }
    for i in range(len(all_food)-1):
        food = all_food[i]
        for allergen in food.allergens:
            if allergen in allergen_candidates:
                continue
            allergen_candidates[allergen] = set(food.ingredients)
            for j in range(i+1, len(all_food)):
                other_food = all_food[j]
                if allergen not in other_food.allergens:
                    continue
                allergen_candidates[allergen].intersection_update(other_food.ingredients)

    return [(list(ingredients)[0], allergen)
                for allergen, ingredients
                in allergen_candidates.items() if len(ingredients) == 1]


def remove_ingredient_allergens(
        all_food: List[Food],
        definite_allergens: List[Tuple[str, str]]) -> None:
    ingredients, allergens = list(zip(*definite_allergens))
    for food in all_food:
        for ingredient in food.ingredients[:]:
            if ingredient in ingredients:
                food.ingredients.remove(ingredient)
        for allergen in food.allergens[:]:
            if allergen in allergens:
                food.allergens.remove(allergen)


def part1(all_food: List[Food]) -> int:
    food = copy.deepcopy(all_food)
    while True:
        definite_allergens = get_definite_allergens(food)
        if not definite_allergens:
            break
        remove_ingredient_allergens(food, definite_allergens)
    return sum(len(f.ingredients) for f in food)


def part2(all_food: List[Food]) -> str:
    food = copy.deepcopy(all_food)
    all_allergens: List[Tuple[str, str]] = []
    while True:
        definite_allergens = get_definite_allergens(food)
        if not definite_allergens:
            break
        remove_ingredient_allergens(food, definite_allergens)
        all_allergens.extend(definite_allergens)
    ingredients = ','.join(x[0] for x in sorted(all_allergens, key=lambda x: x[1]))
    return ingredients


if __name__ == '__main__':
    raw_food = [Food(line) for line in get_file_lines('/mnt/d/code/aoc/2020/input/day21.txt')]
    print(part1(raw_food))  # 2020
    print(part2(raw_food))  # bcdgf,xhrdsl,vndrb,dhbxtb,lbnmsr,scxxn,bvcrrfbr,xcgtv
