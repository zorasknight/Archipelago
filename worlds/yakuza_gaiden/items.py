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

# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.

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
    "POCKET CIRCUIT": "pocket_circuit",
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

# --------------------------------------------------
# Option Tag Filtering
# --------------------------------------------------


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

# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class YakuzaGaidenItem(Item):
    game = "YakuzaGaiden"


# Ontop of our regular itempool, our world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# For now, let's make a function that returns the name of a random filler item here in items.py.
def get_random_filler_item_name(world: YakuzaGaiden) -> str:
    if world.random.randint(0, 99) < world.options.trap_chance and TRAP_ITEMS:
        return world.random.choice(TRAP_ITEMS)

    return world.random.choice(FILLER_ITEMS)


def create_item_with_correct_classification(world: YakuzaGaiden, name: str) -> YakuzaGaidenItem:
    # Our world class must have a create_item() function that can create any of our items by name at any time.
    # So, we make this helper function that creates the item by name with the correct classification.
    # Note: This function's content could just be the contents of world.create_item in world.py directly,
    # but it seemed nicer to have it in its own function over here in items.py.
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    return YakuzaGaidenItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


# With those two helper functions defined, let's now get to actually creating and submitting our itempool.
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

    for _ in range(world.options.max_golden_ball_count.value):
        itempool.append(
            world.create_item("Golden Ball")
        )

    if world.options.progressive_skills:
        for item_name, count in PROGRESSIVE_SKILL_COUNTS.items():
            for _ in range(count):
                itempool.append(
                    world.create_item(item_name)
                )
    # Some items may only exist if the player enables certain options.
    # In our case, If the hammer option is enabled, the sixth item is the Hammer.
    # Otherwise, we add a filler Confetti Cannon.
    #if world.options.hammer:
        # Once again, it is important to stress that even though the Hammer doesn't always exist,
        # it must be present in the worlds item_name_to_id.
        # Whether it is actually in the itempool is determined purely by whether we create and add the item here.
        #itempool.append(world.create_item("Hammer"))

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

    # Sometimes, you might want the player to start with certain items already in their inventory.
    # These items are called "precollected items".
    # They will be sent as soon as they connect for the first time (depending on your client's item handling flag).
    # Players can add precollected items themselves via the generic "start_inventory" option.
    # If you want to add your own precollected items, you can do so via world.push_precollected().
    #if world.options.start_with_one_confetti_cannon:
        # We're adding a filler item, but you can also add progression items to the player's precollected inventory.
        #starting_confetti_cannon = world.create_item("Confetti Cannon")
        #world.push_precollected(starting_confetti_cannon)
