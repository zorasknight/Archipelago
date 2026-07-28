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

    MONETARY_MIN = int(world.options.item_cost_min)
    MONETARY_MAX = int(world.options.item_cost_max)

    POINT_MIN = int(world.options.item_cost_point_min)
    POINT_MAX = int(world.options.item_cost_point_max)

    if MONETARY_MIN > MONETARY_MAX:
        raise ValueError(
            "Item Cost Minimum cannot be greater than Item Cost Maximum"
        )

    if POINT_MIN > POINT_MAX:
        raise ValueError(
            "Item Point Minimum cannot be greater than Item Cost Point Maximum"
        )

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

    # --------------------------------------------------
    # Add JUNK region filler checks
    # --------------------------------------------------

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

    patch_files = {
        "patch.csv": csv_buffer.getvalue()
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