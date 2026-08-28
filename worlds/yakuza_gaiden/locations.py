from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location
import re
import orjson
import pkgutil

if TYPE_CHECKING:
    from .world import YakuzaGaiden


def load_json_data(data_name: str):
    return orjson.loads(
        pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig")
    )


LOCATIONS = load_json_data("locations.json")


# Every location must have a unique integer ID associated with it.
# Lookup from location name to ID.
LOCATION_NAME_TO_ID = {
    location["label"]: int(location["id"])
    for location in LOCATIONS.values()
    if location.get("region", "").upper() != "JUNK"
}


OPTION_TAGS = {
    "POCKET CIRCUIT": "pocket_circuit",
    "WEIRD SHOPS": "weird_shops",
    "SHOPS": "shops",
    "CONSUMABLE SHOPS": "consumable_shops",
    "CASINO": "casino",
    "DARTS": "darts",
    "POOL": "pool",
    "GOLF": "golf",
    "SHOGI": "shogi",
    "AKAME TASKS": "akame_tasks",
    "AKAME TRIAL": "akame_trial",
    "AKAME COMBAT": "akame_combat",
    "AKAME FETCH": "akame_fetch",
    "AKAME PHOTO": "akame_photo",
    "AKAME OUTFIT": "akame_outfit",
    "SUBSTORY": "substory",
}


# Each Location instance must correctly report the "game" it belongs to.
class YakuzaGaidenLocation(Location):
    game = "YakuzaGaiden"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: YakuzaGaiden) -> None:
    create_regular_locations(world)
    create_events(world)

def get_grapple_limit(world, region_name):
    if region_name == "YOKOHAMA":
        return world.options.important_grapple_items_yokohama.value

    if region_name.startswith("SOTENBORI"):
        return world.options.important_grapple_items_sotenbori.value

    if region_name.startswith("COLOSSEUM"):
        return world.options.important_grapple_items_colosseum.value

    return 0

def create_regular_locations(world: YakuzaGaiden) -> None:
    # Grab regions created in regions.py
    yokohama = world.get_region("Yokohama")

    sotenbori_1 = world.get_region("Sotenbori 1")
    sotenbori_2 = world.get_region("Sotenbori 2")
    sotenbori_3 = world.get_region("Sotenbori 3")
    sotenbori_4 = world.get_region("Sotenbori 4")

    colosseum_1 = world.get_region("Colosseum 1")
    colosseum_2 = world.get_region("Colosseum 2")
    colosseum_3 = world.get_region("Colosseum 3")
    colosseum_4 = world.get_region("Colosseum 4")

    pocket_circuit_1 = world.get_region("Pocket Circuit 1")
    pocket_circuit_2 = world.get_region("Pocket Circuit 2")
    pocket_circuit_3 = world.get_region("Pocket Circuit 3")
    pocket_circuit_4 = world.get_region("Pocket Circuit 4")

    region_lookup = {
        "YOKOHAMA": yokohama,

        "SOTENBORI_1": sotenbori_1,
        "SOTENBORI_2": sotenbori_2,
        "SOTENBORI_3": sotenbori_3,
        "SOTENBORI_4": sotenbori_4,

        "COLOSSEUM_1": colosseum_1,
        "COLOSSEUM_2": colosseum_2,
        "COLOSSEUM_3": colosseum_3,
        "COLOSSEUM_4": colosseum_4,

        "POCKET_CIRCUIT_1": pocket_circuit_1,
        "POCKET_CIRCUIT_2": pocket_circuit_2,
        "POCKET_CIRCUIT_3": pocket_circuit_3,
        "POCKET_CIRCUIT_4": pocket_circuit_4,
    }

    for location in LOCATIONS.values():

        if location["region"] == "JUNK":
            continue
        if location["region"] == "GOAL":
            continue

        tags = location.get("tags", "").upper()

        if location.get("region", "").upper() == "JUNK" or "JUNK" in tags:
            continue

        # Skip locations whose option is disabled
        skip = False

        for tag, option_name in OPTION_TAGS.items():
            # This intentionally catches:
            # POCKET CIRCUIT_1
            # POCKET CIRCUIT_2
            # POCKET CIRCUIT_3
            # POCKET CIRCUIT_4
            if tag in tags and not getattr(world.options, option_name):
                skip = True
                break

        if skip:
            continue

        # Progressive Grapple locations
        # Progressive Wire locations
        if "PROGRESSIVE WIRE" in tags:

            if not world.options.progressive_grapple_items:
                continue

            max_grapple = get_grapple_limit(
                world,
                location["region"]
            )

            match = re.search(
                r"(\d+)$",
                location["label"]
            )

            if match:
                grapple_number = int(match.group(1))

                if grapple_number > max_grapple:
                    continue

        if "WIRE" in tags and "PROGRESSIVE WIRE" not in tags:
            if world.options.progressive_grapple_items:
                continue

        region = region_lookup.get(location["region"], sotenbori_1)

        region.add_locations(
            {location["label"]: int(location["id"])},
            YakuzaGaidenLocation,
        )


def create_events(world: YakuzaGaiden) -> None:
    yokohama = world.get_region("Yokohama")

    yokohama.add_event(
        "Collect All Golden Balls",
        "EVENT_GOLDEN_BALLS"
    )
    
    yokohama.add_event(
        "[Goal] Defeat Shishido",
        "EVENT_DEFEAT_SHISHIDO"
    )

    yokohama.add_event(
        "[Goal] Defeat Pocket Circuit Owner Rival Race",
        "EVENT_DEFEAT_POCKET_CIRCUIT_OWNER"
    )