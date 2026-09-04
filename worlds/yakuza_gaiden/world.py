from collections.abc import Mapping
from typing import Any
from BaseClasses import CollectionState
from Fill import FillError, fill_restrictive
# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World
from .output import generate_output
# Imports of your world's files must be relative.
from . import items, locations, regions, rules, web_world
from . import options as YakuzaGaiden_options  # rename due to a name conflict with World.options

# APQuest will go through all the parts of the world api one step at a time,
# with many examples and comments across multiple files.
# If you'd rather read one continuous document, or just like reading multiple sources,
# we also have this document specifying the entire world api:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md


# The world class is the heart and soul of an apworld implementation.
# It holds all the data and functions required to build the world and submit it to the multiworld generator.
# You could have all your world code in just this one class, but for readability and better structure,
# it is common to split up world functionality into multiple files.
# This implementation in particular has the following additional files, each covering one topic:
# regions.py, locations.py, rules.py, items.py, options.py and web_world.py.
# It is recommended that you read these in that specific order, then come back to the world class.
class YakuzaGaiden(World):
    """
    Yakuza Like a Dragon: Gaiden is a modern day beat em up, mini game fest, role playing game where you play the role of Joryu, totally distinct from Kiryu.
    Baka mi tai.
    """

    # The docstring should contain a description of the game, to be displayed on the WebHost.

    # You must override the "game" field to say the name of the game.
    game = "Yakuza Gaiden"

    # The WebWorld is a definition class that governs how this world will be displayed on the website.
    web = web_world.YakuzaGaidenWebWorld()
    generate_output = generate_output
    # This is how we associate the options defined in our options.py with our world.
    # (Note: options.py has been imported as "apquest_options" at the top of this file to avoid a name conflict)
    options_dataclass = YakuzaGaiden_options.YakuzaGaidenOptions
    options: YakuzaGaiden_options.YakuzaGaidenOptions  # Common mistake: This has to be a colon (:), not an equals sign (=).

    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    # We define these in regions.py and items.py respectively, so we just set them here.
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    origin_region_name = "Yokohama"

    # Our world class must have certain functions ("steps") that get called during generation.
    # The main ones are: create_regions, set_rules, create_items.
    # For better structure and readability, we put each of these in their own file.
    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def pre_fill(self) -> None:
        if not self.options.pocket_circuit:
            return

        self.fill_pocket_circuit_locations()


    def create_items(self) -> None:
        items.create_all_items(self)

    # Our world class must also have a create_item function that can create any one of our items by name at any time.
    # We also put this in a different file, the same one that create_items is in.
    def create_item(self, name: str) -> items.YakuzaGaidenItem:
        return items.create_item_with_correct_classification(self, name)

    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # You must override this function and return this infinitely repeatable item's name.
    # In our case, we defined a function called get_random_filler_item_name for this purpose in our items.py.
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)


    def fill_pocket_circuit_locations(self) -> None:
        locations_to_fill = [
            location
            for location in self.multiworld.get_locations(self.player)
            if (
                locations.get_pocket_circuit_special_category(location.name)
                is not None
                and not location.item
            )
        ]

        pc_items = [
            item
            for item in self.multiworld.itempool
            if (
                item.player == self.player
                and items.item_has_tag(item.name, "POCKET_CIRCUIT")
            )
        ]

        if len(locations_to_fill) > len(pc_items):
            raise FillError(
                "Pocket Circuit placement failed: "
                f"need {len(locations_to_fill)} PC items, "
                f"but only {len(pc_items)} exist."
            )

        # Give restrictive fill its own copy of all PC items.
        # fill_restrictive() removes successfully placed items from this list,
        # while unused PC items remain available for the normal global fill.
        items_to_fill = pc_items.copy()

        # Build a state representing the currently available item pool.
        partial_state = CollectionState(self.multiworld)

        for item in self.multiworld.itempool:
            partial_state.collect(item, prevent_sweep=True)

        partial_state.sweep_for_advancements()

        fill_restrictive(
            self.multiworld,
            partial_state,
            locations_to_fill,
            items_to_fill,
            single_player_placement=True,
            lock=True,
            allow_partial=True,
            name="Pocket Circuit",
        )

        # Remove only PC items that were actually placed from the real
        # multiworld item pool. Unused PC parts stay available to normal fill.
        for item in pc_items:
            if item.location is not None:
                self.multiworld.itempool.remove(item)

        # We require all 50 PC part locations to have been filled.
        unfilled_locations = [
            location
            for location in locations_to_fill
            if not location.item
        ]

        if unfilled_locations:
            raise FillError(
                "Pocket Circuit placement failed: "
                f"{len(unfilled_locations)} PC locations could not be filled."
            )

    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    # slot_data is just a dictionary using basic types, that will be converted to json when sent to the client.

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "substory",
            "akame_tasks",
            "shop_key",
            "minigame_shop_key",
            "pocket_circuit",
            "minigames",
            "progressive_skills",
            "intro_skip",
            "randomize_enemy_stats",
            "progressive_grapple_items",
            "trap_chance",
            "golden_ball_wincon",
            "defeat_shishido_wincon",
            "defeat_pocket_circuit_owner_wincon",
            "required_golden_ball_count",
            "max_golden_ball_count", 
            "shops",
            "weird_shops",
            "consumable_shops",
            "item_cost_min",
            "item_cost_max",
            "darts",
            "pool",
            "golf",
            "casino",
            "shogi",
            "item_cost_point_min",
            "item_cost_point_max",
            "akame_combat",
            "akame_fetch",
            "akame_photo",
            "akame_trial",
            "akame_outfit",
            "skill_money_min",
            "skill_money_max",
            "skill_point_min",
            "skill_point_max",
            "part_time_money_min",
            "part_time_money_max",
            "part_time_point_min",
            "part_time_point_max",
            "attack_defense_min",
            "attack_defense_max",
            "resist_min",
            "resist_max",
            "important_grapple_items_yokohama",
            "important_grapple_items_sotenbori",
            "important_grapple_items_colosseum",
            "enemy_hp_mult",
            "enemy_attack_mult",
            "pool_modifier", 
            "golf_modifier", 
            "casino_modifier", 
            "shogi_modifier", 
            "pocket_circuit_modifier", 
            "akame_shop_modifier",
        )
