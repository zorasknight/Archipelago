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


def set_all_rules(world: YakuzaGaiden) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: YakuzaGaiden) -> None:

    yokohama_to_sotenbori = world.get_entrance(
        "Yokohama to Sotenbori"
    )

    sotenbori_to_sotenbori_akame_3 = world.get_entrance(
        "Sotenbori to Sotenbori Akame 3"
    )

    sotenbori_akame_3_to_colosseum = world.get_entrance(
        "Sotenbori Akame 3 to Colosseum"
    )

    colosseum_to_pocket_circuit = world.get_entrance(
        "Colosseum to Pocket Circuit"
    )


    world.set_rule(
        yokohama_to_sotenbori,
        True_()
    )

    world.set_rule(
        sotenbori_to_sotenbori_akame_3,
        create_key_item_check_rule(2)
    )

    world.set_rule(
        sotenbori_akame_3_to_colosseum,
        create_key_item_check_rule(6)
    )

    world.set_rule(
        colosseum_to_pocket_circuit,
        create_key_item_check_rule(6)
    )


def set_all_location_rules(world: YakuzaGaiden) -> None:

    if world.options.pocket_circuit:
        basic_pocket_circuit_items = (
            Has("High Capacity Battery")
            |
            Has("Regular Battery")
            &
            Has("High Torque Motor")
            |
            Has("Godspeed Motor")
        )

        for location in world.get_locations():

            location_data = LOCATION_NAME_TO_DATA.get(
                location.name
            )

            if location_data is None:
                continue

            tags = location_data.get(
                "tags",
                ""
            )

            if "Pocket Circuit" in tags:
                world.set_rule(
                    location,
                    basic_pocket_circuit_items
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