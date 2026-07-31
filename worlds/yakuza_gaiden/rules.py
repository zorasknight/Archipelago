from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasFromListUnique, True_, Rule

import orjson
import pkgutil


if TYPE_CHECKING:
    from .world import YakuzaGaiden


def load_json_data(data_name: str):
    return orjson.loads(
        pkgutil.get_data(
            "worlds.yakuza_gaiden",
            "data/" + data_name
        ).decode("utf-8-sig")
    )


LOCATIONS = load_json_data("locations.json")


LOCATION_NAME_TO_DATA = {
    location["label"]: location
    for location in LOCATIONS.values()
}


def create_key_item_check_rule(n: int) -> Rule:
    return HasFromListUnique(
        "Sneakers",
        "Soccer Ball",
        "Wedding Ring",
        "Hat",
        "Crawfish",
        "Baby Tooth",
        "Underwear",
        "Signed Ball",
        count=n
    )


def create_golden_ball_check_rule(n: int) -> Rule:
    return Has(
        "Golden Ball",
        count=n
    )

POCKET_CIRCUIT_TIER_ORDER = {
    "PLUS": 1,
    "EXTRA": 2,
    "SUPER": 3,
    "ULTRA": 4,
}


def get_pocket_circuit_part_type(item_name: str) -> str | None:
    name = item_name.upper()

    if "TIRE" in name:
        return "Tire"

    if "FRAME" in name:
        return "Frame"

    if "MOTOR" in name:
        return "Motor"

    if "GEAR" in name or "GEARS" in name:
        return "Gear"

    return None

def create_pocket_circuit_car_check_rule(n: int) -> Rule:
    return HasFromListUnique(
        "DRAG-ON Ultra",
        "Super Devil Killer",
        "Banging' Killer Bee",
        "Golem Tiger",
        "Alpha Cool Striker",
        "DRAG-ON",
        "Golem Jaguar",
        "Killer Bee",
        "Devil Killer",
        "Cool Striker",
        count=n
    )

def get_pocket_circuit_item_tier(item_name: str) -> int:
    name = item_name.upper()

    for tier_name, tier_value in POCKET_CIRCUIT_TIER_ORDER.items():
        if name.startswith(tier_name + " "):
            return tier_value

        if name.endswith(" " + tier_name):
            return tier_value

    return 0


def build_pocket_circuit_part_requirements(
    world: YakuzaGaiden,
) -> dict[str, dict[int, list[Rule]]]:

    parts = {}

    for item_name in world.item_name_to_id:

        part_type = get_pocket_circuit_part_type(item_name)

        if part_type is None:
            continue

        tier = get_pocket_circuit_item_tier(item_name)

        if part_type not in parts:
            parts[part_type] = {}

        if tier not in parts[part_type]:
            parts[part_type][tier] = []

        parts[part_type][tier].append(
            Has(item_name)
        )

    return parts


def create_pocket_circuit_rule(
    parts: dict,
    required_tier: int,
) -> Rule:

    required_parts = []

    for part_type in ["Tire", "Motor", "Gear", "Frame"]:

        possible_parts = []

        for tier, rules in parts.get(part_type, {}).items():

            if tier >= required_tier:
                possible_parts.extend(rules)

        part_rule = None

        for rule in possible_parts:
            if part_rule is None:
                part_rule = rule
            else:
                part_rule |= rule

        if part_rule is None:
            return True_()
        
        required_parts.append(part_rule)

    final_rule = None

    for rule in required_parts:
        if final_rule is None:
            final_rule = rule
        else:
            final_rule &= rule

    return final_rule


def set_all_rules(world: YakuzaGaiden) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: YakuzaGaiden) -> None:

    yokohama_to_sotenbori_1 = world.get_entrance("Yokohama to Sotenbori 1")

    sotenbori_1_to_sotenbori_2 = world.get_entrance("Sotenbori 1 to Sotenbori 2")

    sotenbori_2_to_colosseum_1 = world.get_entrance("Sotenbori 2 to Colosseum 1")

    sotenbori_3_to_colosseum_3 = world.get_entrance("Sotenbori 3 to Colosseum 3")

    sotenbori_3_to_sotenbori_4 = world.get_entrance("Sotenbori 3 to Sotenbori 4")

    sotenbori_4_to_colosseum_4 = world.get_entrance("Sotenbori 4 to Colosseum 4")

    colosseum_1_to_pocket_circuit_1 = world.get_entrance("Colosseum 1 to Pocket Circuit 1")

    colosseum_1_to_colosseum_2 = world.get_entrance("Colosseum 1 to Colosseum 2")

    colosseum_1_to_sotenbori_3 = world.get_entrance("Colosseum 1 to Sotenbori 3")

    colosseum_2_to_pocket_circuit_2 = world.get_entrance("Colosseum 2 to Pocket Circuit 2")

    colosseum_3_to_pocket_circuit_3 = world.get_entrance("Colosseum 3 to Pocket Circuit 3")

    colosseum_4_to_pocket_circuit_4 = world.get_entrance("Colosseum 4 to Pocket Circuit 4")


    world.set_rule(
        yokohama_to_sotenbori_1,
        True_()
    )

    world.set_rule(
        sotenbori_1_to_sotenbori_2,
        create_key_item_check_rule(2)
    )

    world.set_rule(
        sotenbori_2_to_colosseum_1,
        create_key_item_check_rule(2)
    )

    world.set_rule(
        colosseum_1_to_pocket_circuit_1,
        create_key_item_check_rule(2)
    )

    world.set_rule(
        colosseum_1_to_colosseum_2,
        create_key_item_check_rule(2)
    )

    world.set_rule(
        colosseum_1_to_sotenbori_3,
        create_key_item_check_rule(6)
    )

    world.set_rule(
        colosseum_2_to_pocket_circuit_2,
        create_key_item_check_rule(6)
    )

    world.set_rule(
        sotenbori_3_to_colosseum_3,
        create_key_item_check_rule(6)
    )

    world.set_rule(
        colosseum_3_to_pocket_circuit_3,
        create_key_item_check_rule(6)
    )

    world.set_rule(
        sotenbori_3_to_sotenbori_4,
        create_key_item_check_rule(6)
    )

    world.set_rule(
        sotenbori_4_to_colosseum_4,
        create_key_item_check_rule(6)
    )

    world.set_rule(
        colosseum_4_to_pocket_circuit_4,
        create_key_item_check_rule(6)
    )


def set_all_location_rules(world: YakuzaGaiden) -> None:

    if world.options.pocket_circuit:

        pocket_parts = build_pocket_circuit_part_requirements(world)

        pocket_circuit_1_items = (
            create_pocket_circuit_car_check_rule(1)
            &
            create_pocket_circuit_rule(pocket_parts, 2)
            &
            (
                (
                    Has("Regular Battery")
                    |
                    Has("High Capacity Battery")
                )
                &
                (
                    Has("Godspeed Motor")
                    |
                    Has("High Torque Motor")
                )
            )
        )

        pocket_circuit_2_items = (
            create_pocket_circuit_car_check_rule(2)
            &
            create_pocket_circuit_rule(pocket_parts, 3)
            &
            (
                (
                    Has("Regular Battery")
                    &
                    Has("High Capacity Battery")
                )
                &
                (
                    Has("Godspeed Motor Mark II")
                    |
                    Has("High Torque Motor Mark II")
                )
            )
        )

        pocket_circuit_3_items = (
            create_pocket_circuit_car_check_rule(4)
            &
            create_pocket_circuit_rule(pocket_parts, 4)
            &
            (
                (
                    Has("Regular Battery")
                    &
                    Has("High Capacity Battery")
                    &
                    Has("High Speed Battery")
                    &
                    Has("Flat Wing")
                    &
                    Has("Light Suspension")
                )
                &
                (
                    Has("Godspeed Motor Mark II")
                    |
                    Has("High Torque Motor Mark II")
                )
            )
        )

        pocket_circuit_4_items = (
            create_pocket_circuit_car_check_rule(6)
            &
            create_pocket_circuit_rule(pocket_parts, 4)
            &
            (
                (
                    Has("Regular Battery")
                    &
                    Has("High Capacity Battery")
                    &
                    Has("High Speed Battery")
                    &
                    Has("Rainbow Wing")
                    &
                    Has("Heavy Suspension")
                )
                &
                (
                    Has("Ultra Godspeed Motor")
                    |
                    Has("Ultra High Torque Motor")
                )
            )
        )


        for location in world.get_locations():

            location_data = LOCATION_NAME_TO_DATA.get(location.name)

            if location_data is None:
                continue

            tags = location_data.get("tags", "").upper()

            if "POCKET CIRCUIT_1" in tags:
                world.set_rule(
                    location,
                    pocket_circuit_1_items
                )

            elif "POCKET CIRCUIT_2" in tags:
                world.set_rule(
                    location,
                    pocket_circuit_2_items
                )
            elif "POCKET CIRCUIT_3" in tags:
                world.set_rule(
                    location,
                    pocket_circuit_3_items
                )
            elif "POCKET CIRCUIT_4" in tags:
                world.set_rule(
                    location,
                    pocket_circuit_4_items
                )




def set_completion_condition(world: YakuzaGaiden) -> None:
    golden_ball_event = world.get_location(
        "Collect All Golden Balls"
    )

    world.set_rule(
        golden_ball_event,
        Has("Golden Ball", count=7)
    )

    world.set_completion_rule(
        Has("EVENT_GOLDEN_BALLS")
    )