import csv
import os
from typing import TYPE_CHECKING

import orjson
import pkgutil


if TYPE_CHECKING:
    from .world import YakuzaGaiden


def load_json_data(data_name: str):
    return orjson.loads(
        pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig")
    )


ITEMS = load_json_data("items.json")
LOCATIONS = load_json_data("locations.json")


# Lookup item metadata by Archipelago item name
ITEM_NAME_TO_DATA = {
    item["label"]: item
    for item in ITEMS.values()
}


# Lookup location metadata by Archipelago location name
LOCATION_NAME_TO_DATA = {
    location["label"]: location
    for location in LOCATIONS.values()
}


def generate_output(world: "YakuzaGaiden", output_directory: str) -> None:
    file_path = os.path.join(
        output_directory,
        f"{world.multiworld.get_out_file_name_base(world.player)}.csv"
    )

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "file_name",
            "table_name",
            "row_id",
            "column_id",
            "item_id",
            "item_name",
            "purchase_price",
            "purchase_points",
        ])

        for location in world.get_locations():

            # Skip events / empty locations
            if location.address is None:
                continue

            if location.item is None:
                continue

            # Get extracted location metadata
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

            # Native YakuzaGaiden item
            if item.player == world.player:
                item_data = ITEM_NAME_TO_DATA[item.name]

                row.extend([
                    int(item_data["item_id"]),
                    "",
                    int(item_data.get("purchase_price") or 0),
                    int(item_data.get("purchase_points") or 0),
                ])

            # Cross-world item
            else:
                row.extend([
                    "",
                    item.name,
                    "",
                    "",
                ])

            writer.writerow(row)

    print(f"Wrote patch data to {file_path}")