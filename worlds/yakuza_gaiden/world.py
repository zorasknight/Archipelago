from collections.abc import Mapping
from typing import Any
from BaseClasses import CollectionState
from Fill import FillError, fill_restrictive

from worlds.AutoWorld import World
from .output import generate_output

from . import items, locations, regions, rules, web_world
from . import options as YakuzaGaiden_options  


class YakuzaGaiden(World):
    """
    Yakuza Like a Dragon: Gaiden is a modern day beat em up, mini game fest, role playing game where you play the role of Joryu, totally distinct from Kiryu.
    Baka mi tai.
    """

    game = "Yakuza Gaiden"

    web = web_world.YakuzaGaidenWebWorld()
    generate_output = generate_output

    options_dataclass = YakuzaGaiden_options.YakuzaGaidenOptions
    options: YakuzaGaiden_options.YakuzaGaidenOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Yokohama"

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

    def create_item(self, name: str) -> items.YakuzaGaidenItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_pocket_circuit_locations(self) -> None:
        locations_to_fill = [
            location
            for location in self.multiworld.get_locations(self.player)
            if ( locations.get_pocket_circuit_special_category(location.name) is not None and not location.item )
        ]

        pc_items = [
            item
            for item in self.multiworld.itempool
            if ( item.player == self.player and items.item_has_tag(item.name, "POCKET_CIRCUIT") )
        ]

        if len(locations_to_fill) > len(pc_items):
            raise FillError(
                "Pocket Circuit placement failed: "
                f"need {len(locations_to_fill)} PC items, "
                f"but only {len(pc_items)} exist."
            )

        items_to_fill = pc_items.copy()

        partial_state = CollectionState(self.multiworld)

        for item in self.multiworld.itempool:
            partial_state.collect(item, prevent_sweep=True)

        partial_state.sweep_for_advancements()

        fill_restrictive( self.multiworld, partial_state, locations_to_fill, items_to_fill, single_player_placement=True, lock=True, allow_partial=True, name="Pocket Circuit", )

        # Remove only PC items that were actually placed from the real
        # multiworld item pool. Unused PC parts stay available to normal fill.
        for item in pc_items:
            if item.location is not None:
                self.multiworld.itempool.remove(item)

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
