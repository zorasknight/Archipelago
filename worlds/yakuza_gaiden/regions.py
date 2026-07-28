from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import YakuzaGaiden

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: YakuzaGaiden) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: YakuzaGaiden) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    yokohama = Region("Yokohama", world.player, world.multiworld)
    sotenbori = Region("Sotenbori", world.player, world.multiworld)
    sotenbori_akame_3 = Region("Sotenbori Post Akame 3", world.player, world.multiworld)
    colosseum_bottom = Region("Colosseum Entrance", world.player, world.multiworld)
    colosseum_silver = Region("Colosseum Silver", world.player, world.multiworld)
    colosseum_gold = Region("Colosseum Gold", world.player, world.multiworld)
    pocket_circuit = Region("Pocket Circuit", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [yokohama, sotenbori, sotenbori_akame_3, colosseum_bottom, colosseum_silver, colosseum_gold, pocket_circuit]

    # Some regions may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    #if world.options.pocket_circuit:
        #pocket_circuit = Region("Pocket Circuit", world.player, world.multiworld)
        #regions.append(pocket_circuit)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: YakuzaGaiden) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    yokohama = world.get_region("Yokohama")
    sotenbori = world.get_region("Sotenbori")
    sotenbori_akame_3 = world.get_region("Sotenbori Post Akame 3")
    colosseum_bottom = world.get_region("Colosseum Entrance")
    colosseum_silver = world.get_region("Colosseum Silver")
    colosseum_gold = world.get_region("Colosseum Gold")
    pocket_circuit = world.get_region("Pocket Circuit")

    # Okay, now we can get connecting. For this, we need to create Entrances.
    # Entrances are inherently one-way, but crucially, AP assumes you can always return to the origin region.
    # One way to create an Entrance is by calling the Entrance constructor.
    #yokohama_to_sotenbori = Entrance(world.player, "Yokohama to Sotenbori", parent=yokohama)
    #yokohama.exits.append(yokohama_to_sotenbori)
    # You can then connect the Entrance to the target region.
    #yokohama_to_sotenbori.connect(sotenbori)

    # An even easier way is to use the region.connect helper.
    yokohama.connect(sotenbori, "Yokohama to Sotenbori")
    sotenbori.connect(sotenbori_akame_3, "Sotenbori to Sotenbori Akame 3")
    colosseum_bottom.connect(pocket_circuit, "Colosseum to Pocket Circuit")
    sotenbori_akame_3.connect(colosseum_bottom, "Sotenbori Akame 3 to Colosseum")
    colosseum_bottom.connect(colosseum_silver, "Colosseum to Colosseum Silver Rank")
    colosseum_silver.connect(colosseum_gold, "Colosseum Silver Rank to Colosseum Gold Rank")
    
    
    # The region.connect helper even allows adding a rule immediately.
    # We'll talk more about rule creation in the set_all_rules() function in rules.py.
    #sotenbori_akame_3.connect(colosseum_bottom, "Sotenbori Akame 3 to Colosseum", lambda state: state.has("Key", world.player))

    # Some Entrances may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # In this case, we previously created an extra "Top Middle Room" region that we now need to connect to Overworld.
    #if world.options.hammer:
    #    pocket_circuit = world.get_region("Pocket Circuit")
    #    colosseum_bottom.connect(pocket_circuit, "Colosseum to Pocket Circuit")
