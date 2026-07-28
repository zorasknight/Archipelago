from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md


# The first type of Option we'll discuss is the Toggle.
# A toggle is an option that can either be on or off. This will be represented by a checkbox on the website.
# The default for a toggle is "off".
# If you want a toggle to be on by default, you can use the "DefaultOnToggle" class instead of the "Toggle" class.
class PocketCircuit(Toggle):
    """
    Enables Pocket Circuit items and related checks.
    Disabling this also removes all extra pocket circuit items from the world that are outside of the pocket circuit room.
    """

    display_name = "Enable Pocket Circuit Items Checks"
    default = True


class Shops(Toggle):
    """
    Enables Basic shops into the pool.
    This changes all shop items to be single purchase, but does not effect conveniance stores, the pharmacy, or any strange one off shops.
    """

    display_name = "Enable Basic Shop Rando"
    default = True

class WeirdShops(Toggle):
    """
    Enables the Weird shops into the pool.
    This changes all shop items to be single purchase, this only enables weird one off stores like ichiban confections, or take out food places like smile cart.
    """

    display_name = "Enable Weird Shop Rando"
    default = True

class ConsumableShops(Toggle):
    """
    Enables the Consumable shops into the pool.
    This changes all shop items to be single purchase, this effects all poppo marts and the pharmacy.
    """

    display_name = "Enable Consumable Shop Rando"
    default = False

class Minigames(Toggle):
    """
    Enables the randomization of Minigames.
    Only randomizes minigames with rewards attached. this excludes pocket circuit as that has its own section. If this is off, all below related settings are off as well.
    """

    display_name = "Enable Minigame Reward Rando"
    default = True

class Darts(Toggle):
    """
    Enables the randomization of Darts.
    Only randomizes Dart Rival rewards, If "Enable Minigame Reward Rando" is off, this setting is ignored.
    """

    display_name = "Enable Dart Rival Reward Rando"
    default = True

class Pool(Toggle):
    """
    Enables the randomization of the Pool Point Shop.
    Only randomizes Pool Point Shop rewards, If "Enable Minigame Reward Rando" is off, this setting is ignored.
    """

    display_name = "Enable Pool Point Shop Rando"
    default = True

class Golf(Toggle):
    """
    Enables the randomization of the Golf Point Shop.
    Only randomizes Golf Point Shop rewards, If "Enable Minigame Reward Rando" is off, this setting is ignored.
    """

    display_name = "Enable Golf Point Shop Rando"
    default = True

class Casino(Toggle):
    """
    Enables the randomization of the Casino Point Shops.
    Only randomizes Casino Point Shop rewards, This includes Yokohama, Sotenbori, and Colossuem. If "Enable Minigame Reward Rando" is off, this setting is ignored.
    """

    display_name = "Enable Casino Point Shop Rando"
    default = True

class Shogi(Toggle):
    """
    Enables the randomization of the Shogi Point Shops.
    Only randomizes Shogi Point Shop rewards, This includes Yokohama, and Sotenbori. If "Enable Minigame Reward Rando" is off, this setting is ignored.
    """

    display_name = "Enable Shogi Point Shop Rando"
    default = True

class TrapChance(Range):
    """
    Percentage chance that any given Confetti Cannon will be replaced by a Math Trap.
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 10


# A Range is a numeric option with a min and max value. This will be represented by a slider on the website.
class ItemCostMin(Range):
    """
    How expensive each item can be, note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Item Cost Minimum"

    range_start = 0
    range_end = 3000000

    # Range options must define an explicit default value.
    default = 1000

class ItemCostMax(Range):
    """
    How expensive each item can be, note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Item Cost Maximum"

    range_start = 0
    range_end = 3000000

    # Range options must define an explicit default value.
    default = 1000

class ItemCostPointMin(Range):
    """
    How expensive each item can be in point stores, note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Item Cost Point Minimum"

    range_start = 0
    range_end = 10000

    # Range options must define an explicit default value.
    default = 100

class ItemCostPointMax(Range):
    """
    How expensive each item can be in point stores, note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Item Cost Point Maximum"

    range_start = 0
    range_end = 10000

    # Range options must define an explicit default value.
    default = 8000


# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class YakuzaGaidenOptions(PerGameCommonOptions):
    pocket_circuit: PocketCircuit
    minigames: Minigames
    trap_chance: TrapChance
    shops: Shops
    weird_shops: WeirdShops
    consumable_shops: ConsumableShops
    darts: Darts
    pool: Pool
    golf: Golf
    casino: Casino
    shogi: Shogi
    item_cost_min: ItemCostMin
    item_cost_max: ItemCostMax
    item_cost_point_min: ItemCostPointMin
    item_cost_point_max: ItemCostPointMax


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Primary Settings",
        [PocketCircuit, Minigames, TrapChance],
    ),
    OptionGroup(
        "Shops",
        [Shops, WeirdShops, ConsumableShops],
    ),
    OptionGroup(
        "Minigames",
        [Darts, Pool, Golf, Casino, Shogi],
    ),
    OptionGroup(
        "Cost Options",
        [ItemCostMin, ItemCostMax, ItemCostPointMin, ItemCostPointMax],
    ),
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {

}
