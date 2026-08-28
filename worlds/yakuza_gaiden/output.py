import csv
import io
import os
import zipfile
from datetime import datetime, UTC
from typing import TYPE_CHECKING
from BaseClasses import ItemClassification
import orjson
import pkgutil
import Utils
import yaml

from worlds.Files import APPlayerContainer


if TYPE_CHECKING:
    from .world import YakuzaGaiden


def load_json_data(data_name: str):
    return orjson.loads(
        pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig")
    )


ITEMS = load_json_data("items.json")
LOCATIONS = load_json_data("locations.json")


ITEM_NAME_TO_DATA = {
    item["label"]: item
    for item in ITEMS.values()
}

OPTION_EXPORT_MAP = {
    "randomize_enemy_stats": "randomize_enemy_stats",
    "intro_skip": "intro_skip",
    "shop_key": "shop_key",
    "minigame_shop_key": "minigame_shop_key",

    "skill_money_min": "skill_money_min",
    "skill_money_max": "skill_money_max",

    "skill_point_min": "skill_akame_min",
    "skill_point_max": "skill_akame_max",

    "part_time_money_min": "part_time_money_min",
    "part_time_money_max": "part_time_money_max",

    "part_time_point_min": "part_time_akame_min",
    "part_time_point_max": "part_time_akame_max",

    "attack_defense_min": "attack_and_defense_min",
    "attack_defense_max": "attack_and_defense_max",

    "resist_min": "resist_min",
    "resist_max": "resist_max",

    "enemy_hp_mult": "enemy_hp_mult",
    "enemy_attack_mult": "enemy_attack_mult",

    "golf_modifier": "golf_modifier", 
    "pool_modifier": "pool_modifier", 
    "casino_modifier": "casino_modifier", 
    "shogi_modifier": "shogi_modifier", 
    "pocket_circuit_modifier": "pocket_circuit_modifier", 
    "akame_shop_modifier": "akame_shop_modifier",

    "golden_ball_wincon": "golden_ball_wincon",
    "defeat_shishido_wincon": "defeat_shishido_wincon",
    "defeat_pocket_circuit_owner_wincon": "defeat_pocket_circuit_owner_wincon",

    "substory": "substory",

    "akame_tasks": "akame_tasks",
    "akame_combat": "akame_combat",
    "akame_fetch": "akame_fetch",
    "akame_photo": "akame_photo",
    "akame_trial": "akame_trial",
    "akame_outfit": "akame_outfit",

    "max_golden_ball_count": "max_golden_ball_count", 
    "required_golden_ball_count": "required_golden_ball_count",

    "progressive_grapple_items": "progressive_grapple_items",
    "important_grapple_items_yokohama": "important_grapple_items_yokohama",
    "important_grapple_items_sotenbori": "important_grapple_items_sotenbori",
    "important_grapple_items_colosseum": "important_grapple_items_colosseum"
}

LOCATION_NAME_TO_DATA = {
    location["label"]: location
    for location in LOCATIONS.values()
}


LOCATION_ID_TO_DATA = {
    location["id"]: location
    for location in LOCATIONS.values()
}


class GaidenContainer(APPlayerContainer):
    game: str = "Yakuza Gaiden"
    patch_file_ending = ".zip"

    def __init__(
        self,
        patch_data: dict,
        base_path: str,
        output_directory: str,
        player=None,
        player_name: str = "",
        server: str = "",
    ):
        self.patch_data = patch_data
        self.file_path = base_path

        container_path = os.path.join(
            output_directory,
            base_path + ".zip"
        )

        super().__init__(
            container_path,
            player,
            player_name,
            server
        )

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for filename, contents in self.patch_data.items():
            opened_zipfile.writestr(
                filename,
                contents
            )

        super().write_contents(opened_zipfile)


def weighted_rand(rng, min_val, max_val):
    span = max_val - min_val + 1

    cheap_max = min_val + int(span * 0.08) - 1
    average_max = min_val + int(span * 0.35) - 1
    expensive_max = min_val + int(span * 0.65) - 1

    r = rng.random()

    if r < 0.50:
        return rng.randint(min_val, cheap_max)
    elif r < 0.85:
        return rng.randint(cheap_max + 1, average_max)
    elif r < 0.95:
        return rng.randint(average_max + 1, expensive_max)
    else:
        return rng.randint(expensive_max + 1, max_val)




def generate_output(world: "YakuzaGaiden", output_directory: str) -> None:

    MONETARY_MIN, MONETARY_MAX = sorted([
        int(world.options.item_cost_min),
        int(world.options.item_cost_max),
    ])

    POINT_MIN, POINT_MAX = sorted([
        int(world.options.item_cost_point_min),
        int(world.options.item_cost_point_max),
    ])

    GOLDEN_BALL_MIN, GOLDEN_BALL_MAX = sorted([
        int(world.options.required_golden_ball_count),
        int(world.options.max_golden_ball_count),
    ])

    SKILL_MONEY_MIN, SKILL_MONEY_MAX = sorted([
        int(world.options.skill_money_min),
        int(world.options.skill_money_max),
    ])

    SKILL_POINT_MIN, SKILL_POINT_MAX = sorted([
        int(world.options.skill_point_min),
        int(world.options.skill_point_max),
    ])

    PART_TIME_MONEY_MIN, PART_TIME_MONEY_MAX = sorted([
        int(world.options.part_time_money_min),
        int(world.options.part_time_money_max),
    ])

    PART_TIME_POINT_MIN, PART_TIME_POINT_MAX = sorted([
        int(world.options.part_time_point_min),
        int(world.options.part_time_point_max),
    ])

    ATTACK_DEFENSE_MIN, ATTACK_DEFENSE_MAX = sorted([
        int(world.options.attack_defense_min),
        int(world.options.attack_defense_max),
    ])

    RESIST_MIN, RESIST_MAX = sorted([
        int(world.options.resist_min),
        int(world.options.resist_max),
    ])

    def rand_money(rng):
        return weighted_rand(rng, MONETARY_MIN, MONETARY_MAX)

    def rand_points(rng):
        return weighted_rand(rng, POINT_MIN, POINT_MAX)

    patch_rows = []

    rng = world.random

    for location in world.get_locations():

        if location.address is None:
            continue

        if location.item is None:
            continue

        location_data = LOCATION_NAME_TO_DATA.get(location.name)

        if location_data is None:
            continue

        row = [
            location_data["source"],
            location_data["location"],
            int(location_data["slot"]),
            "replacement_item_id",
        ]

        item = location.item

        item_quality = ""

        if item.player == world.player:
            item_data = ITEM_NAME_TO_DATA[item.name]

            row.extend([
                int(item_data["item_id"]),
                item.name,
                rand_money(rng),
                rand_points(rng),
            ])

        else:
            owner_name = world.multiworld.get_file_safe_player_name(
                item.player
            )

            display_name = f"({owner_name}) {item.name}"

            if item.classification & ItemClassification.progression:
                item_quality = "progression"

            elif item.classification & ItemClassification.useful:
                item_quality = "useful"

            elif item.classification & ItemClassification.trap:
                item_quality = "trap"

            else:
                item_quality = "filler"

            row.extend([
                "",
                display_name,
                rand_money(rng),
                rand_points(rng),
            ])

        row.append(
            location_data["id"]
        )

        row.append(
            item_quality
        )

        row.append(
            "False"
        )

        patch_rows.append(row)

    for location_name, location_data in LOCATION_NAME_TO_DATA.items():

        if location_data.get("region") != "JUNK":
            continue

        junk_item = world.create_filler()

        junk_item_data = ITEM_NAME_TO_DATA.get(
            junk_item.name,
            {}
        )

        patch_rows.append([
            location_data["source"],
            location_data["location"],
            int(location_data["slot"]),
            "replacement_item_id",
            int(junk_item_data.get("item_id", 0)),
            junk_item.name,
            rand_money(rng),
            rand_points(rng),
            location_data["id"],
            "filler",
            "True",
        ])

    csv_buffer = io.StringIO(newline="")

    writer = csv.writer(csv_buffer)

    writer.writerow([
        "file_name",
        "table_name",
        "row_id",
        "column_id",
        "item_id",
        "item_name",
        "purchase_price",
        "purchase_points",
        "location_id",
        "item_quality",
        "junk_check"
    ])

    writer.writerows(patch_rows)

    curr_timestamp = datetime.strftime(
        datetime.now(UTC),
        "%d%b%Y-%H%M%S"
    )

    mod_name = (
        f"AP-{world.multiworld.seed_name}-"
        f"P{world.player}-"
        f"{world.multiworld.get_file_safe_player_name(world.player)}-"
        f"{curr_timestamp}"
    )

    mod_dir = os.path.join(
        output_directory,
        mod_name + "_" + Utils.__version__
    )

    #
    # Export world options
    #
    options_yaml = {}

    for ap_name, yaml_name in OPTION_EXPORT_MAP.items():

        if hasattr(world.options, ap_name):

            option = getattr(
                world.options,
                ap_name
            )

            try:
                options_yaml[yaml_name] = option.value

            except AttributeError:
                options_yaml[yaml_name] = option

        options_yaml["item_cost_min"] = MONETARY_MIN
        options_yaml["item_cost_max"] = MONETARY_MAX

        options_yaml["item_cost_point_min"] = POINT_MIN
        options_yaml["item_cost_point_max"] = POINT_MAX

        options_yaml["required_golden_ball_count"] = GOLDEN_BALL_MIN
        options_yaml["max_golden_ball_count"] = GOLDEN_BALL_MAX

        options_yaml["skill_money_min"] = SKILL_MONEY_MIN
        options_yaml["skill_money_max"] = SKILL_MONEY_MAX

        options_yaml["skill_akame_min"] = SKILL_POINT_MIN
        options_yaml["skill_akame_max"] = SKILL_POINT_MAX

        options_yaml["part_time_money_min"] = PART_TIME_MONEY_MIN
        options_yaml["part_time_money_max"] = PART_TIME_MONEY_MAX

        options_yaml["part_time_akame_min"] = PART_TIME_POINT_MIN
        options_yaml["part_time_akame_max"] = PART_TIME_POINT_MAX

        options_yaml["attack_and_defense_min"] = ATTACK_DEFENSE_MIN
        options_yaml["attack_and_defense_max"] = ATTACK_DEFENSE_MAX

        options_yaml["resist_min"] = RESIST_MIN
        options_yaml["resist_max"] = RESIST_MAX


    #options_yaml["seed"] = world.multiworld.seed_name
    options_yaml["seed"] = int(world.multiworld.seed_name) + world.player


    yaml_buffer = yaml.dump(
        options_yaml,
        sort_keys=False
    )


    patch_files = {
        "patch.csv": csv_buffer.getvalue(),
        "options.yaml": yaml_buffer
    }

    mod = GaidenContainer(
        patch_files,
        mod_dir,
        output_directory,
        world.player,
        world.multiworld.get_file_safe_player_name(world.player)
    )

    mod.write()

    print(
        f"Wrote Yakuza Gaiden patch zip for player {world.player}"
    )