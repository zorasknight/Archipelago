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

class GoldenBallWincon(Toggle):
    """
    Having this option on will require collecting Golden Balls to be able to goal the game.
    Having multiple wincons active will require completing each one, if no wincons are selected defeat Shishido will be enabled.
    """

    display_name = "Enable Golden Ball Wincon"
    default = True

class DefeatShishidoWincon(Toggle):
    """
    Having this option on will require defeating Shishido at the end of the game be able to goal the game.
    Having multiple wincons active will require completing each one, if no wincons are selected "Defeat Shishido" will be enabled.
    """

    display_name = "Enable Defeat Shishido Wincon"
    default = False

class DefeatPocketCircuitOwnerWincon(Toggle):
    """
    Having this option on will require Defeating the Pocket Circuit Owner Rival in a race to be able to goal the game.
    Having multiple wincons active will require completing each one, if no wincons are selected defeat Shishido will be enabled.
    """

    display_name = "Enable Defeat Pocket Circuit Owner Wincon"
    default = False

class ShopKey(Toggle):
    """
    Locks shops down and hides all items until corresponding shop key unlock item is used.
    Shop Key items will appear in your consumable section and need to be activated and consumed to add the items back to the shop.
    """

    display_name = "Enable Shop Keys"
    default = True

class MinigameKey(Toggle):
    """
    Locks Minigame Point shops down and hides all items until corresponding Minigame shop key unlock item is used.
    Minigame Shop Key items will appear in your consumable section and need to be activated and consumed to add the items back to the shop.
    """

    display_name = "Enable Minigame Shop Keys"
    default = True

class Substory(Toggle):
    """
    Adds a check for completing substories.
    This currently adds a single check for each substory, 
    so you will get one for vanquishing the Red Peacocks and one for the Final Showdown with the Red Peacocks.
    """

    display_name = "Enable Substory Checks"
    default = False

class AkameTasks(Toggle):
    """
    Adds checks for each Akame Task, will also add all required items to the Shigano Shop in Sotenbori.
    You can adjust which tasks give a reward in the below Akame Tasks section.
    """

    display_name = "Enable Akame Task Checks"
    default = True

class AkameFetch(Toggle):
    """
    Toggle Akame Fetch Quests giving items, these are the quests where you give an item gift to the person for a reward, Excluding the special 8 progression checks.
    This will not have an effect if Akame Tasks are disabled.
    """

    display_name = "Enable Akame Fetch Tasks"
    default = True

class AkameCombat(Toggle):
    """
    Toggle Akame Combat Quests giving items, these are the quests where you battle a group of enemies for a reward.
    This will not have an effect if Akame Tasks are disabled.
    """

    display_name = "Enable Akame Combat Tasks"
    default = True

class AkameTrial(Toggle):
    """
    Toggle Akame Trial Quests giving items, these are the various quests around Sotenbori that require Kiryu to do various tasks like Pool or Darts.
    This will not have an effect if Akame Tasks are disabled.
    """

    display_name = "Enable Akame Trial Tasks"
    default = True

class AkamePhoto(Toggle):
    """
    Toggle Akame Photo Quests giving items, These quests require Kiryu to take photos of various objects.
    This will not have an effect if Akame Tasks are disabled.
    """

    display_name = "Enable Akame Photo Tasks"
    default = True

class AkameOutfit(Toggle):
    """
    Toggle Akame Outfit Quests giving items, These Quests require specific outfits to be worn, requiring specific outfit items to be in logic.
    This will not have an effect if Akame Tasks are disabled.
    """

    display_name = "Enable Akame Outfit Tasks"
    default = True


class ProgressiveSkills(Toggle):
    """
    Allows certain skill books to progressively get stronger with each additional copy found.
    Disabling this causes imbalance with stats and can have weird effects with some skills gotten out of order.
    """

    display_name = "Enable Progressive Skills"
    default = True

class ProgressiveGrappleItems(Toggle):
    """
    Causes all regional grapple items to be progressive, ie: first Sotenbori grapple item will always come out as grapple_item_1 regardless of which actual grapple was grabbed.
    Amount of relevant grapples can be set below. Good option for newer players learning where grapple points are.
    I recomend not maxing this out as you will not have the standard location hints to guide you to missed points.
    """

    display_name = "Toggle Progressive Grapple Items"
    default = False

class RandomizeEnemyStats(Toggle):
    """
    Randomizes all enemy health and damage stats between 0.5 and 3.0.
    WARNING: This can make the playthrough much harder!
    """

    display_name = "Randomize All Enemy Stats"
    default = False

class IntroSkip(Toggle):
    """
    Sets key fights in the early tutorial section of the game to 1 HP.
    This goes up until the end of the first dungeon before entering sotenbori.
    """

    display_name = "Enable Intro Skip"
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


class MaxGoldenBallCount(Range):
    """
    The maximum number of the game winning item "Golden Ball". 
    This value must be above or equal to the "Required Golden Ball" count.
    """

    display_name = "Max Total Golden Ball Count"

    range_start = 1
    range_end = 30

    # Range options must define an explicit default value.
    default = 10

class RequiredGoldenBallCount(Range):
    """
    The required amount of "Golden Ball"s the player needs to find to trigger thier goal. 
    This number must be below or equal to the "Max Golden Ball" count.
    """

    display_name = "Required Golden Ball Count"

    range_start = 1
    range_end = 30

    # Range options must define an explicit default value.
    default = 7

class PoolModifier(Range):
    """
    A modifier applied to the cost of items purchased with points from the Pool minigame. 
    Keeping this lower is recomended for a more natural point-to-item ratio. consider 100 = 1.0 or no modifier, 200 = 2.0 or 2x points required per item.
    """

    display_name = "Pool Shop cost modifier"

    range_start = 1
    range_end = 300

    # Range options must define an explicit default value.
    default = 20

class GolfModifier(Range):
    """
    A modifier applied to the cost of items purchased with points from the Golf minigame. 
    Keeping this lower is recomended for a more natural point-to-item ratio. consider 100 = 1.0 or no modifier, 200 = 2.0 or 2x points required per item.
    """

    display_name = "Golf Shop cost modifier"

    range_start = 1
    range_end = 300

    # Range options must define an explicit default value.
    default = 25

class CasinoModifier(Range):
    """
    A modifier applied to the cost of items purchased with points from the Casino minigame. 
    Keeping this lower is recomended for a more natural point-to-item ratio. consider 100 = 1.0 or no modifier, 200 = 2.0 or 2x points required per item.
    """

    display_name = "Casino Shop cost modifier"

    range_start = 1
    range_end = 300

    # Range options must define an explicit default value.
    default = 60

class ShogiModifier(Range):
    """
    A modifier applied to the cost of items purchased with points from the Shogi minigame. 
    Keeping this lower is recomended for a more natural point-to-item ratio. consider 100 = 1.0 or no modifier, 200 = 2.0 or 2x points required per item.
    """

    display_name = "Shogi Shop cost modifier"

    range_start = 1
    range_end = 300

    # Range options must define an explicit default value.
    default = 50

class AkameShopModifier(Range):
    """
    A modifier applied to the cost of items purchased with points from the Akame Store. 
    Keeping this lower is recomended for a more natural point-to-item ratio. consider 100 = 1.0 or no modifier, 200 = 2.0 or 2x points required per item.
    """

    display_name = "Akame Shop cost modifier"

    range_start = 1
    range_end = 300

    # Range options must define an explicit default value.
    default = 200

class PocketCircuitModifier(Range):
    """
    A modifier applied to the cost of items purchased with points from the Pocket Circuit minigame. 
    Keeping this lower is recomended for a more natural point-to-item ratio. consider 100 = 1.0 or no modifier, 200 = 2.0 or 2x points required per item.
    """

    display_name = "Pocket Circuit Shop cost modifier"

    range_start = 1
    range_end = 300

    # Range options must define an explicit default value.
    default = 150


# A Range is a numeric option with a min and max value. This will be represented by a slider on the website.
class ItemCostMin(Range):
    """
    Max potential value of how expensive each item can be in stores. 
    note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Item Cost Minimum"

    range_start = 100
    range_end = 3000000

    # Range options must define an explicit default value.
    default = 1000

class ItemCostMax(Range):
    """
    Minimum potential value of how expensive each item can be in stores. 
    note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Item Cost Maximum"

    range_start = 100
    range_end = 3000000

    # Range options must define an explicit default value.
    default = 1000000

class ItemCostPointMin(Range):
    """
    Max potential value of how expensive each item can be in point stores. 
    note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Item Cost Point Minimum"

    range_start = 10
    range_end = 10000

    # Range options must define an explicit default value.
    default = 100

class ItemCostPointMax(Range):
    """
    Minimum potential value of how expensive each item can be in point stores. 
    note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Item Cost Point Maximum"

    range_start = 10
    range_end = 10000

    # Range options must define an explicit default value.
    default = 5000

class SkillMoneyMin(Range):
    """
    The minimum monetary cost each skill can be in the level up tab. 
    note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Skill Cost Minimum"

    range_start = 100
    range_end = 3000000

    # Range options must define an explicit default value.
    default = 1000

class SkillMoneyMax(Range):
    """
    The maximum monetary cost each skill can be in the level up tab. 
    note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.    """

    display_name = "Skill Cost Maximum"

    range_start = 100
    range_end = 3000000

    # Range options must define an explicit default value.
    default = 1000000

class SkillPointMin(Range):
    """
    The minimum point cost each skill can be in the level up tab. 
    note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Skill Point Cost Minimum"

    range_start = 10
    range_end = 10000

    # Range options must define an explicit default value.
    default = 100

class SkillPointMax(Range):
    """
    The maximum point cost each skill can be in the level up tab. 
    note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Skill Point Cost Maximum"

    range_start = 10
    range_end = 10000

    # Range options must define an explicit default value.
    default = 3000

class PartTimeMoneyMin(Range):
    """
    The max amount of monetary reward that Akame tasks can grant. 
    note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Akame Task Monetary Reward Minimum"

    range_start = 100
    range_end = 1000000

    # Range options must define an explicit default value.
    default = 75000

class PartTimeMoneyMax(Range):
    """
    The maximum amount of monetary reward that Akame tasks can grant. 
    note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Akame Task Monetary Reward Maximum"

    range_start = 100
    range_end = 1000000

    # Range options must define an explicit default value.
    default = 500000

class PartTimePointMin(Range):
    """
    The max amount of point reward that Akame tasks can grant. 
    note: this uses a 4 bucket system to try and curve most prices towards the low end, and leave a handfull of high end prices. Use the default as a guide here.
    """

    display_name = "Akame Task Point Reward Minimum"

    range_start = 10
    range_end = 5000

    # Range options must define an explicit default value.
    default = 100

class PartTimePointMax(Range):
    """
    The maximum amount of point reward that Akame tasks can grant. 
    note: Setting this higher can make key items less impactful, adjust if you want to play without waiting on others.
    """

    display_name = "Akame Task Point Reward Maximum"

    range_start = 10
    range_end = 5000

    # Range options must define an explicit default value.
    default = 2000

class AttackDefenseMin(Range):
    """
    The minimum value gear can be given for Attack and Defense.
    note: I recomend allowing negative values as it can force some decision making based on powerful abilities randomized in.
    """

    display_name = "Gear Attack and Defense Minimum"

    range_start = -1000
    range_end = 1000

    # Range options must define an explicit default value.
    default = -200

class AttackDefenseMax(Range):
    """
    The maximum value gear can be given for Attack and Defense.
    note: Most values will fall somewhere in the middle of the two extremes, consider that you can get up to 4 pieces of gear.
    """

    display_name = "Gear Attack and Defense Maximum"


    range_start = -1000
    range_end = 1000

    # Range options must define an explicit default value.
    default = 400

class ResistMin(Range):
    """
    Minimum Value for Resistances on gear. 
    note: These cannot go into the negative, but higher values of resistance reduces damage from that type of attack.
    """

    display_name = "Gear Resistance Minimum"

    range_start = 0
    range_end = 500

    # Range options must define an explicit default value.
    default = 0

class ResistMax(Range):
    """
    Maximum Value for Resistances on gear. 
    note: These cannot go into the negative, but higher values of resistance reduces damage from that type of attack.
    """

    display_name = "Gear Resistance Maximum"

    range_start = 0
    range_end = 500

    # Range options must define an explicit default value.
    default = 150

class EnemyHPMult(Range):
    """
    Determines the multiplier to use for Enemy HP. 
    note: This is overidden by the "Randomize Enemy Stats" option, as this is a single multiplier for all enemies.
    """

    display_name = "Enemy HP Multiplier"

    range_start = 10
    range_end = 300

    # Range options must define an explicit default value.
    default = 100

class EnemyAttackMult(Range):
    """
    Determines the multiplier to use for Enemy Attack. ( 100 = 1.0, 50 = .5) 
    note: This is overidden by the "Randomize Enemy Stats" option, as this is a single multiplier for all enemies.
    """

    display_name = "Enemy Attack Multiplier"

    range_start = 10
    range_end = 300

    # Range options must define an explicit default value.
    default = 100

class ImportantGrappleItemsYokohama(Range):
    """
    The max number of potentially important grapple items within Yokohama. Only in effect if "Progressive Grapple Items" is turned on. 
    note: All grapple items collected after the max set here will be randomized junk items instead.
    """

    display_name = "Important Grapple Item's Yokohama"

    range_start = 1
    range_end = 29

    # Range options must define an explicit default value.
    default = 20

class ImportantGrappleItemsSotenbori(Range):
    """
    The max number of potentially important grapple items within Sotenbori. Only in effect if "Progressive Grapple Items" is turned on. 
    note: All grapple items collected after the max set here will be randomized junk items instead.
    """

    display_name = "Important Grapple Items Sotenbori"

    range_start = 1
    range_end = 39

    # Range options must define an explicit default value.
    default = 30

class ImportantGrappleItemsColosseum(Range):
    """
    The max number of potentially important grapple items within the Colosseum. Only in effect if "Progressive Grapple Items" is turned on. 
    note: All grapple items collected after the max set here will be randomized junk items instead.
    """

    display_name = "Important Grapple Items Colosseum"

    range_start = 1
    range_end = 19

    # Range options must define an explicit default value.
    default = 10

class TrapChance(Range):
    """
    Percent of junk items turned into traps.
    Current traps: Joke healing items
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 10

# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class YakuzaGaidenOptions(PerGameCommonOptions):
    substory: Substory
    akame_tasks: AkameTasks
    shop_key: ShopKey
    minigame_shop_key: MinigameKey
    pocket_circuit: PocketCircuit
    minigames: Minigames
    progressive_skills: ProgressiveSkills
    intro_skip: IntroSkip
    randomize_enemy_stats: RandomizeEnemyStats
    progressive_grapple_items: ProgressiveGrappleItems
    trap_chance: TrapChance
    golden_ball_wincon: GoldenBallWincon
    defeat_shishido_wincon: DefeatShishidoWincon
    defeat_pocket_circuit_owner_wincon: DefeatPocketCircuitOwnerWincon
    required_golden_ball_count: RequiredGoldenBallCount
    max_golden_ball_count: MaxGoldenBallCount
    shops: Shops
    weird_shops: WeirdShops
    consumable_shops: ConsumableShops
    item_cost_min: ItemCostMin
    item_cost_max: ItemCostMax
    darts: Darts
    pool: Pool
    golf: Golf
    casino: Casino
    shogi: Shogi
    item_cost_point_min: ItemCostPointMin
    item_cost_point_max: ItemCostPointMax
    akame_combat: AkameCombat
    akame_fetch: AkameFetch
    akame_photo: AkamePhoto
    akame_trial: AkameTrial
    akame_outfit: AkameOutfit
    skill_money_min: SkillMoneyMin
    skill_money_max: SkillMoneyMax
    skill_point_min: SkillPointMin
    skill_point_max: SkillPointMax
    part_time_money_min: PartTimeMoneyMin
    part_time_money_max: PartTimeMoneyMax
    part_time_point_min: PartTimePointMin
    part_time_point_max: PartTimePointMax
    attack_defense_min: AttackDefenseMin
    attack_defense_max: AttackDefenseMax
    resist_min: ResistMin
    resist_max: ResistMax
    important_grapple_items_yokohama: ImportantGrappleItemsYokohama
    important_grapple_items_sotenbori: ImportantGrappleItemsSotenbori
    important_grapple_items_colosseum: ImportantGrappleItemsColosseum
    enemy_hp_mult: EnemyHPMult
    enemy_attack_mult: EnemyAttackMult
    pool_modifier: PoolModifier
    golf_modifier: GolfModifier
    casino_modifier: CasinoModifier
    shogi_modifier: ShogiModifier
    pocket_circuit_modifier: PocketCircuitModifier
    akame_shop_modifier: AkameShopModifier

# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Primary Settings",
        [Substory, AkameTasks, ShopKey, MinigameKey, PocketCircuit, Minigames, ProgressiveSkills, IntroSkip, RandomizeEnemyStats, ProgressiveGrappleItems, TrapChance],
    ),
    OptionGroup(
        "Win Conditions",
        [GoldenBallWincon, DefeatShishidoWincon, DefeatPocketCircuitOwnerWincon, RequiredGoldenBallCount, MaxGoldenBallCount],
    ),
    OptionGroup(
        "Shops",
        [Shops, WeirdShops, ConsumableShops, ItemCostMin, ItemCostMax],
    ),
    OptionGroup(
        "Minigames",
        [Darts, Pool, Golf, Casino, Shogi, ItemCostPointMin, ItemCostPointMax],
    ),
    OptionGroup(
        "Akame Tasks",
        [AkameCombat, AkameFetch, AkamePhoto, AkameTrial, AkameOutfit],
    ),
    OptionGroup(
        "Skill Options",
        [SkillMoneyMin, SkillMoneyMax, SkillPointMin, SkillPointMax],
    ),
    OptionGroup(
        "Reward Options",
        [PartTimeMoneyMin, PartTimeMoneyMax, PartTimePointMin, PartTimePointMax],
    ),
    OptionGroup(
        "Equipment Options",
        [AttackDefenseMin, AttackDefenseMax, ResistMin, ResistMax],
    ),
    OptionGroup(
        "Grapple Item Options",
        [ImportantGrappleItemsYokohama, ImportantGrappleItemsSotenbori, ImportantGrappleItemsColosseum],
    ),
    OptionGroup(
        "Enemy Options",
        [EnemyHPMult, EnemyAttackMult],
    ),
    OptionGroup(
        "Point Modifiers",
        [PoolModifier, GolfModifier, CasinoModifier, ShogiModifier, PocketCircuitModifier, AkameShopModifier],
    ),
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {

}
