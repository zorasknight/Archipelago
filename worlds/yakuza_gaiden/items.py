from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import YakuzaGaiden
import orjson

import pkgutil


from typing import Dict, Any, Union, List


def load_json_data(data_name: str) -> Union[List[Any], Dict[str, Any]]:
    return orjson.loads(
        pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig")
    )


ITEMS = load_json_data("items.json")
LOCATIONS = load_json_data("locations.json")

ITEM_NAME_TO_ID = {
    item["label"]: int(item["item_id"])
    for item in ITEMS.values()
}


# --------------------------------------------------
# Item Tag Helpers
# --------------------------------------------------

CLASSIFICATION_MAP = {
    "IMPORTANT": ItemClassification.progression,
    "USEFUL": ItemClassification.useful,
    "FILLER": ItemClassification.filler,
    "TRAP": ItemClassification.trap,
}

OPTION_TAG_RULES = {
    "POCKET_CIRCUIT": "pocket_circuit",
    "MINIGAME_SHOP_KEY": "minigame_shop_key",
    "SHOP_KEY": "shop_key",
    "MINIGAMES": "minigames",
    "SHOPS": "shops",
    "POOL": "pool",
    "SHOGI": "shogi",
    "GOLF": "golf",
    "CASINO": "casino",
    "DARTS": "darts",
    "CONSUMABLE_SHOPS": "consumable_shops",
    "WEIRD_SHOPS": "weird_shops",
}

AKAME_FETCH_MINIMUMS = {
    "Luxury Yakiniku Bento": 3,
    "Oden": 1,
    "Pine Candy": 1,
    "SEGA Taiyaki": 1,
    "Sushi Set": 1,
    "Okonomiyaki": 1,
    "Takoyaki with Large Octopus": 1,
    "Kitty Kat (Tiger)": 3,
    "Tauriner": 2,
    "Azuki Bar BOX": 1,
    "Ono Michio Pixel Figure": 1,
    "Luxury Timepiece": 1,
    "Star Crossed Earrings": 1,
    "Ichiban Senbei (Salt)": 1,
    "Pocket Tissues": 2,
    "Sake": 1,
    "Staminan Light": 1,
    "Egg": 1,
}


def get_item_tags(item):
    return [
        tag.upper()
        for tag in item.get("tags", [])
    ]


def get_item_classification(item):
    """
    Convert tags into Archipelago classification.
    """

    tags = get_item_tags(item)

    for tag in [
        "IMPORTANT",
        "TRAP",
        "USEFUL",
        "FILLER",
    ]:
        if tag in tags:
            return CLASSIFICATION_MAP[tag]

    # Default fallback
    return ItemClassification.filler



DEFAULT_ITEM_CLASSIFICATIONS = {
    item["label"]: get_item_classification(item)
    for item in ITEMS.values()
}

PROGRESSIVE_SKILL_COUNTS = { 
    "Skill Book: Progressive HP Up": 23, 
    "Skill Book: Progressive Damage Up": 18, 
    "Skill Book: Progressive Heat Gauge Up": 4, 
    "Skill Book: Progressive Extreme Heat Damage Up": 2, 
    "Skill Book: Progressive Drunk Heat Gauge Increase": 2, 
    "Skill Book: Progressive Drunk Attack Heat Gauge Increase": 2, 
    "Skill Book: Progressive Equipment Up": 3, 
    "Skill Book: Progressive Recovery From Food Up": 3, 
    "Skill Book: Progressive Heat Action Damage Up in ExH": 2, 
    "Skill Book: Progressive Evasion Up in ExH": 2, 
    "Skill Book: Progressive Extra Wire": 4, 
    "Skill Book: Progressive Extra Bomb": 4, 
    "Skill Book: Progressive Extra Drone": 4, 
    "Skill Book: Progressive Extra Shoe Boost": 4, 
    }

FILLER_ITEMS = [
    item["label"]
    for item in ITEMS.values()
    if "FILLER" in get_item_tags(item)
]


TRAP_ITEMS = [
    item["label"]
    for item in ITEMS.values()
    if "TRAP" in get_item_tags(item)
]


def item_allowed(world, item):

    tags = get_item_tags(item)

    for tag, option in OPTION_TAG_RULES.items():

        if tag not in tags:
            continue

        if not getattr(world.options, option):
            return False

    if "PROGRESSIVE_SKILLS" in tags:
        if not world.options.progressive_skills:
            return False

    if "REMOVE_SKILLS" in tags:
        if world.options.progressive_skills:
            return False

    return True

class YakuzaGaidenItem(Item):
    game = "YakuzaGaiden"

def get_random_filler_item_name(world: YakuzaGaiden) -> str:
    if world.random.randint(0, 99) < world.options.trap_chance and TRAP_ITEMS:
        return world.random.choice(TRAP_ITEMS)

    return world.random.choice(FILLER_ITEMS)


def create_item_with_correct_classification(world: YakuzaGaiden, name: str) -> YakuzaGaidenItem:

    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    return YakuzaGaidenItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: YakuzaGaiden) -> None:

    itempool: list[Item] = [
        world.create_item(item["label"])
        for item in ITEMS.values()
        if item_allowed(world, item)
        and (
            "IMPORTANT" in get_item_tags(item)
            or "USEFUL" in get_item_tags(item)
        )
        and "PROGRESSIVE_SKILLS" not in get_item_tags(item)
        and item["label"] != "Golden Ball"
    ]

    
    golden_ball_min = int(world.options.required_golden_ball_count)
    golden_ball_max = int(world.options.max_golden_ball_count)

    if golden_ball_min > golden_ball_max:
        golden_ball_min, golden_ball_max = golden_ball_max, golden_ball_min

    for _ in range(golden_ball_max):
        itempool.append(
            world.create_item("Golden Ball")
        )

    if world.options.progressive_skills:
        for item_name, count in PROGRESSIVE_SKILL_COUNTS.items():
            for _ in range(count):
                itempool.append(
                    world.create_item(item_name)
                )

    if world.options.akame_tasks and world.options.akame_fetch:
        for item_name, count in AKAME_FETCH_MINIMUMS.items():
            for _ in range(count):
                itempool.append(
                    world.create_item(item_name)
                )

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool
