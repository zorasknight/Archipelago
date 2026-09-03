from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import And, Has, HasFromListUnique, True_, Rule
from . import items, locations
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
        "Shoes",
        "Soccer Ball",
        "Wedding Ring",
        "Hat",
        "Crawfish",
        "Baby Tooth",
        "Underwear",
        "Signed Ball",
        count=n
    )

def set_pocket_circuit_item_rules(world):
    for location in world.multiworld.get_locations(world.player):
        category = locations.get_pocket_circuit_special_category(location.name)

        if category is None:
            continue

        allowed_tags = items.POCKET_CIRCUIT_PART_CATEGORIES[category]

        location.item_rule = lambda item, tags=allowed_tags: (
            items.item_has_tag(item.name, "POCKET_CIRCUIT")
            and any(
                items.item_has_tag(item.name, tag)
                for tag in tags
            )
        )

        car_name = get_pocket_circuit_car_name(location.name)

        if car_name is not None:
            world.set_rule(
                location,
                Has(car_name)
            )

def get_pocket_circuit_car_name(location_name: str) -> str | None:
    prefix = "[PC] Car "

    if not location_name.startswith(prefix):
        return None

    name = location_name[len(prefix):]

    for part in [" Frame", " Tires", " Motor", " Gears", " Misc"]:
        if name.endswith(part):
            return name[:-len(part)]

    return None

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
        set_pocket_circuit_item_rules(world)

    #these are the key items
    world.set_rule( world.get_location("[Task] A Dental Dilemma"), Has("Baby Tooth"))
    world.set_rule( world.get_location("[Task] My Best Ball"), Has("Soccer Ball"))
    world.set_rule( world.get_location("[Task] Kickin' the Habit"), Has("Shoes"))
    world.set_rule( world.get_location("[Task] A Priceless Autograph"), Has("Signed Ball"))
    world.set_rule( world.get_location("[Task] You Saw Nothing"), Has("Underwear"))
    world.set_rule( world.get_location("[Task] Catch That Crawdad"), Has("Crawfish"))
    world.set_rule( world.get_location("[Task] The Waterlogged Ring"), Has("Wedding Ring"))
    world.set_rule( world.get_location("[Task] Not Just a Hat"), Has("Hat"))


    if world.options.akame_tasks:


        if world.options.akame_fetch:

            if world.options.shop_key and world.options.weird_shops: 
                shigano_rule = Has("Sotenbori Shigano Shop Unlock") 
            else: 
                shigano_rule = True_()

            world.set_rule( world.get_location("[Task] I Want a Convenience Store Bento!"), shigano_rule),
            world.set_rule( world.get_location("[Task] Today's a Boozin Day"), shigano_rule)
            world.set_rule( world.get_location("[Task] Somethin' for the Pain"), shigano_rule)
            world.set_rule( world.get_location("[Task] Tissue, Wipes, Anything!"), shigano_rule)
            world.set_rule( world.get_location("[Task] When Will I Taste Okonomiyaki!?"), shigano_rule)
            world.set_rule( world.get_location("[Task] Takoyaki on the Brain"), shigano_rule)
            world.set_rule( world.get_location("[Task] Have Mercy Give Food!"), shigano_rule)
            world.set_rule( world.get_location("[Task] Hungry Hungry Bento"), shigano_rule)
            world.set_rule( world.get_location("[Task] In Need of Absorption"), shigano_rule)
            world.set_rule( world.get_location("[Task] Desperate for Staminan Light"), shigano_rule)
            world.set_rule( world.get_location("[Task] An Egg-cellent Idea"), shigano_rule)
            world.set_rule( world.get_location("[Task] The Luxury Yakiniku Bento Dream"), shigano_rule)
            world.set_rule( world.get_location("[Task] If Only I Had an Energy Drink..."), shigano_rule)
            world.set_rule( world.get_location("[Task] Desperate for Takoyaki"), shigano_rule)
            world.set_rule( world.get_location("[Task] A Certain Taiyaki Brand"), shigano_rule)
            world.set_rule( world.get_location("[Task] Hungry For Sushi"), shigano_rule)
            world.set_rule( world.get_location("[Task] Order of Oden"), shigano_rule)
            world.set_rule( world.get_location("[Task] Real-Deal Okonomiyaki"), shigano_rule)
            world.set_rule( world.get_location("[Task] In Need of a UFO Catcher"), shigano_rule)
            world.set_rule( world.get_location("[Task] Can Anyone Conquer the UFO Catcher!?"), shigano_rule)
            world.set_rule( world.get_location("[Task] Kitty Kat, Come Home"), shigano_rule)
            world.set_rule( world.get_location("[Task] Pinin' For Pine Candy"), shigano_rule)
            world.set_rule( world.get_location("[Task] That Tantalizing Tauriner!"), shigano_rule)
            world.set_rule( world.get_location("[Task] Up For an Azuki Bar"), shigano_rule)
            world.set_rule( world.get_location("[Task] A Quest for Ono Michio"), shigano_rule)
            world.set_rule( world.get_location("[Task] Time's a Luxury"), shigano_rule)
            world.set_rule( world.get_location("[Task] In Search of Star-Crossed Earings"), shigano_rule)
            world.set_rule( world.get_location("[Task] Itching for Ichiban Senbei"), shigano_rule)

            # world.set_rule( world.get_location("[Task] I Want a Convenience Store Bento!"), Has("Bento Lunch Set") | Has("Healthy Balanced Bento") | Has("Luxury Yakiniku Bento") | Has("Pork Tonkatsu Bento")),
            # world.set_rule( world.get_location("[Task] Today's a Boozin Day"), Has("Sake"))
            # world.set_rule( world.get_location("[Task] Somethin' for the Pain"), Has("Toughness Light") | Has("Toughness Z") | Has("Toughness ZZ") | Has("Toughness Infinity"))
            # world.set_rule( world.get_location("[Task] Tissue, Wipes, Anything!"), Has("Pocket Tissues"))
            # world.set_rule( world.get_location("[Task] When Will I Taste Okonomiyaki!?"), Has("Okonomiyaki") | Has("Okonomiyaki (Mentai Mayo)") | Has("Okonomiyaki (Mochi & Cheese)"))
            # world.set_rule( world.get_location("[Task] Takoyaki on the Brain"), Has("Takoyaki with Large Octopus") | Has("Shockin' Takoyaki"))
            # world.set_rule( world.get_location("[Task] Have Mercy Give Food!"), Has("Bento Lunch Set") | Has("Healthy Balanced Bento") | Has("Luxury Yakiniku Bento") | Has("Pork Tonkatsu Bento") | Has("Oden") | Has("Pine Candy") | Has("SEGA Taiyaki") | Has("Taiyaki Ice Cream"))
            # world.set_rule( world.get_location("[Task] Hungry Hungry Bento"), Has("Luxury Yakiniku Bento"))
            # world.set_rule( world.get_location("[Task] In Need of Absorption"), Has("Pocket Tissues"))
            # world.set_rule( world.get_location("[Task] Desperate for Staminan Light"), Has("Staminan Light"))
            # world.set_rule( world.get_location("[Task] An Egg-cellent Idea"), Has("Egg") | Has("Quality Egg"))
            # world.set_rule( world.get_location("[Task] The Luxury Yakiniku Bento Dream"), Has("Luxury Yakiniku Bento"))
            # world.set_rule( world.get_location("[Task] If Only I Had an Energy Drink..."), Has("Toughness Light") | Has("Toughness Z") | Has("Toughness ZZ") | Has("Toughness Infinity") | Has("Tauriner") | Has("Tauriner Maximum"))
            # world.set_rule( world.get_location("[Task] Desperate for Takoyaki"), Has("Takoyaki with Large Octopus") | Has("Shockin' Takoyaki"))
            # world.set_rule( world.get_location("[Task] A Certain Taiyaki Brand"), Has("SEGA Taiyaki"))
            # world.set_rule( world.get_location("[Task] Hungry For Sushi"), Has("Sushi Set"))
            # world.set_rule( world.get_location("[Task] Order of Oden"), Has("Oden"))
            # world.set_rule( world.get_location("[Task] Real-Deal Okonomiyaki"), Has("Okonomiyaki") | Has("Okonomiyaki (Mentai Mayo)") | Has("Okonomiyaki (Mochi & Cheese)"))
            # world.set_rule( world.get_location("[Task] In Need of a UFO Catcher"), Has("Chu-Chu Tako Doll (Takoyaki)"))
            # world.set_rule( world.get_location("[Task] Can Anyone Conquer the UFO Catcher!?"), Has("Chu-Chu Tako Doll (Takoyaki)"))
            # world.set_rule( world.get_location("[Task] Kitty Kat, Come Home"), Has("Kitty Kat (Tiger)"))
            # world.set_rule( world.get_location("[Task] Pinin' For Pine Candy"), Has("Pine Candy"))
            # world.set_rule( world.get_location("[Task] That Tantalizing Tauriner!"), Has("Tauriner") | Has("Tauriner Maximum"))
            # world.set_rule( world.get_location("[Task] Up For an Azuki Bar"), Has("Azuki Bar BOX"))
            # world.set_rule( world.get_location("[Task] A Quest for Ono Michio"), Has("Ono Michio Pixel Figure"))
            # world.set_rule( world.get_location("[Task] Time's a Luxury"), Has("Luxury Timepiece"))
            # world.set_rule( world.get_location("[Task] In Search of Star-Crossed Earings"), Has("Star Crossed Earrings"))
            # world.set_rule( world.get_location("[Task] Itching for Ichiban Senbei"), Has("Ichiban Senbei (Shoyu)") | Has("Ichiban Fried Senbei") | Has("Ichiban Senbei (Salt)"))




        if world.options.akame_outfit:

            world.set_rule( world.get_location("[Task] Turn That Frown Upside Down, Clown"), Has("Clown Makeup"))
            world.set_rule( world.get_location("[Task] Please Model for Me!"), Has("Straw Hat") & Has("Straw Sandals") & Has("T-Shirt"))
            world.set_rule( world.get_location("[Task] The Outfit from My Memories"), Has("Single Rose") & Has("Leather Shoes"))
            world.set_rule( world.get_location("[Task] A Taste of Kabuki"), Has("Kabuki Makeup"))
            world.set_rule( world.get_location("[Task] My Friend Needs to Understand"), Has("Snake Eyepatch") & Has("Shirtless Blazer"))
            world.set_rule( world.get_location("[Task] Bring a Smile to My Soulless Face"), Has("Weird Stranger Makeup") & Has("Bodysuit"))



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
            pocket_circuit_1_items
            &
            create_pocket_circuit_car_check_rule(2)
            &
            create_pocket_circuit_rule(pocket_parts, 3)
            &
            (
                (
                    Has("Regular Battery")
                    &
                    Has("High Capacity Battery")
                    &
                    Has("Flat Wing")
                    &
                    Has("Light Suspension")
                    &
                    Has("Godspeed Gears")
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
            pocket_circuit_2_items
            &
            create_pocket_circuit_car_check_rule(3)
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
                    Has("Box Wing")
                    &
                    Has("Medium Suspension")
                    &
                    Has("Extra Godspeed Gears")
                )
                &
                (
                    Has("Ultra Godspeed Motor")
                    |
                    Has("Ultra High Torque Motor")
                )
            )
        )

        pocket_circuit_4_items = (
            pocket_circuit_3_items
            &
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
                    Has("Rainbow Wing")
                    &
                    Has("Heavy Suspension")
                    &
                    Has("Ultra Boost Gears")
                    &
                    Has("Ultra Godspeed Gears")
                )
                &
                (
                    Has("Ultra Godspeed Motor")
                    &
                    Has("Ultra High Torque Motor")
                )
            )
        )
        
        world.set_rule(
            world.get_location("[Goal] Defeat Pocket Circuit Owner Rival Race"),
            pocket_circuit_4_items
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


    if world.options.minigame_shop_key:

        billiards_unlock = (Has("Sotenbori Billiard Point Shop Unlock"))
        yoko_shogi_unlock = (Has("Yokohama Shogi Point Shop Unlock"))
        sote_shogi_unlock = (Has("Sotenbori Shogi Point Shop Unlock"))
        golf_unlock = (Has("Sotenbori Golf Point Shop Unlock"))
        sote_toba_unlock = (Has("Sotenbori Gambling Hall Point Shop Unlock"))
        yoko_toba_unlock = (Has("Yokohama Gambling Hall Point Shop Unlock"))
        colo_toba_unlock = (Has("Colosseum Gambling Hall Point Shop Unlock"))
        colo_casino_unlock = (Has("Colosseum Casino Point Shop Unlock"))

        for location in world.get_locations():
            location_data = LOCATION_NAME_TO_DATA.get(location.name)
            
            if location_data is None:
                continue

            tags = location_data.get("tags", "").upper()

            if "POOL" in tags:
                world.set_rule(
                    location,
                    billiards_unlock
                )
            elif "YOKOHAMA" in tags and "SHOGI" in tags:
                world.set_rule(
                    location,
                    yoko_shogi_unlock
                )
            elif "SOTENBORI_1" in tags and "SHOGI" in tags:
                world.set_rule(
                    location,
                    sote_shogi_unlock
                )
            elif "GOLF" in tags:
                world.set_rule(
                    location,
                    golf_unlock
                )
            elif "YOKOHAMA" in tags and "CASINO" in tags:
                world.set_rule(
                    location,
                    yoko_toba_unlock
                )
            elif "SOTENBORI_1" in tags and "CASINO" in tags:
                world.set_rule(
                    location,
                    sote_toba_unlock
                )
            elif "COLOSSEUM_1" in tags and "CASINO" in tags and "WESTERN" in tags:
                world.set_rule(
                    location,
                    colo_casino_unlock
                )
            elif "COLOSSEUM_1" in tags and "CASINO" in tags:
                world.set_rule(
                    location,
                    colo_toba_unlock
                )


    if world.options.shop_key:

        ebisuya_unlock = (Has("Sotenbori Ebisuya Pawn Shop Unlock"))
        wannpark_unlock = (Has("Sotenbori Wannpark Shop Unlock"))
        sichiya_unlock = (Has("Yokohama Sichiya Pawn Shop Unlock"))
        lovemagic_unlock = (Has("Yokohama Lovemagic Shop Unlock"))
        boutique_unlock = (Has("Colosseum Boutique Shop Unlock"))
        boutique_vip_unlock = (Has("Colosseum Boutique VIP Shop Unlock"))
        mizorogi_unlock = (Has("Mizorogi (Akame house) Shop Unlock"))
        park_poppo_unlock = (Has("Sotenbori Park Poppo Shop Unlock"))
        west_poppo_unlock = (Has("Sotenbori West Poppo Shop Unlock"))
        north_poppo_unlock = (Has("Sotenbori North Poppo Shop Unlock"))
        yoko_poppo_unlock = (Has("Yokohama Poppo Shop Unlock"))
        kukuru_unlock = (Has("Sotenbori Kukuru Shop Unlock"))
        tsuruha_unlock = (Has("Sotenbori Tsuruha Shop Unlock"))
        hiratai_unlock = (Has("Sotenbori Hiratai Shop Unlock"))
        shigano_unlock = (Has("Sotenbori Shigano Shop Unlock"))
        smilewagon_unlock = (Has("Yokohama Smilewagon Shop Unlock"))
        ichiban_unlock = (Has("Yokohama Ichiban Confections Shop Unlock"))





        for location in world.get_locations():
            location_data = LOCATION_NAME_TO_DATA.get(location.name)
            
            if location_data is None:
                continue

            tags = location_data.get("tags", "").upper()

            if "EBISUYA" in tags:
                world.set_rule(
                    location,
                    ebisuya_unlock
                )
            elif "WANNPARK" in tags:
                world.set_rule(
                    location,
                    wannpark_unlock
                )
            elif "SHICHIYA" in tags:
                world.set_rule(
                    location,
                    sichiya_unlock
                )
            elif "LOVEMAGIC" in tags:
                world.set_rule(
                    location,
                    lovemagic_unlock
                )
            elif "BOUTIQUE VIP" in tags:
                world.set_rule(
                    location,
                    boutique_vip_unlock
                )
            elif "BOUTIQUE" in tags:
                world.set_rule(
                    location,
                    boutique_unlock
                )
            elif "MIZOROGI" in tags:
                world.set_rule(
                    location,
                    mizorogi_unlock
                )
            elif "PARK POPPO" in tags:
                world.set_rule(
                    location,
                    park_poppo_unlock
                )
            elif "WEST POPPO" in tags:
                world.set_rule(
                    location,
                    west_poppo_unlock
                )   
            elif "NORTH POPPO" in tags:
                world.set_rule(
                    location,
                    north_poppo_unlock
                )   
            elif "YOKO POPPO" in tags:
                world.set_rule(
                    location,
                    yoko_poppo_unlock
                )   
            elif "KUKURU" in tags:
                world.set_rule(
                    location,
                    kukuru_unlock
                )  
            elif "TSURUHA" in tags:
                world.set_rule(
                    location,
                    tsuruha_unlock
                )               
            elif "HIRATAI" in tags:
                world.set_rule(
                    location,
                    hiratai_unlock
                ) 
            elif "SHIGANO" in tags:
                world.set_rule(
                    location,
                    shigano_unlock
                ) 
            elif "SMILEWAGON" in tags:
                world.set_rule(
                    location,
                    smilewagon_unlock
                ) 
            elif "ICHIBANN" in tags:
                world.set_rule(
                    location,
                    ichiban_unlock
                ) 


def set_completion_condition(world: YakuzaGaiden) -> None:

    golden_ball_event = world.get_location(
        "Collect All Golden Balls"
    )
    defeat_shishido = world.get_location(
        "[Goal] Defeat Shishido"
    )

    
    golden_ball_min = int(world.options.required_golden_ball_count)
    golden_ball_max = int(world.options.max_golden_ball_count)

    if golden_ball_min > golden_ball_max:
        golden_ball_min, golden_ball_max = golden_ball_max, golden_ball_min

    world.set_rule(
        golden_ball_event,
        Has("Golden Ball", count=golden_ball_min)
    )

    world.set_rule(
        defeat_shishido,
        create_key_item_check_rule(6)
    )


    goals = []

    if world.options.golden_ball_wincon:
        goals.append(Has("EVENT_GOLDEN_BALLS"))
    if world.options.defeat_shishido_wincon:
        goals.append(Has("EVENT_DEFEAT_SHISHIDO"))
    if world.options.defeat_pocket_circuit_owner_wincon and world.options.pocket_circuit:
        goals.append(Has("EVENT_DEFEAT_POCKET_CIRCUIT_OWNER"))

    if not goals:
        goals.append(Has("EVENT_DEFEAT_SHISHIDO"))

    world.set_completion_rule(
        And(*goals)
    )