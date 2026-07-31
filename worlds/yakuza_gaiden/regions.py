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
    sotenbori_1 = Region("Sotenbori 1", world.player, world.multiworld)
    sotenbori_2 = Region("Sotenbori 2", world.player, world.multiworld)
    sotenbori_3 = Region("Sotenbori 3", world.player, world.multiworld)
    sotenbori_4 = Region("Sotenbori 4", world.player, world.multiworld)
    colosseum_1 = Region("Colosseum 1", world.player, world.multiworld)
    colosseum_2 = Region("Colosseum 2", world.player, world.multiworld)
    colosseum_3 = Region("Colosseum 3", world.player, world.multiworld)
    colosseum_4 = Region("Colosseum 4", world.player, world.multiworld)
    pocket_circuit_1 = Region("Pocket Circuit 1", world.player, world.multiworld)
    pocket_circuit_2 = Region("Pocket Circuit 2", world.player, world.multiworld)
    pocket_circuit_3 = Region("Pocket Circuit 3", world.player, world.multiworld)
    pocket_circuit_4 = Region("Pocket Circuit 4", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [yokohama, sotenbori_1, sotenbori_2, sotenbori_3, sotenbori_4, colosseum_1, colosseum_2, colosseum_3, colosseum_4, pocket_circuit_1, pocket_circuit_2, pocket_circuit_3, pocket_circuit_4]

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

    # Okay, now we can get connecting. For this, we need to create Entrances.
    # Entrances are inherently one-way, but crucially, AP assumes you can always return to the origin region.
    # One way to create an Entrance is by calling the Entrance constructor.
    #yokohama_to_sotenbori = Entrance(world.player, "Yokohama to Sotenbori", parent=yokohama)
    #yokohama.exits.append(yokohama_to_sotenbori)
    # You can then connect the Entrance to the target region.
    #yokohama_to_sotenbori.connect(sotenbori)

    # An even easier way is to use the region.connect helper.
    yokohama.connect(sotenbori_1, "Yokohama to Sotenbori 1")
    sotenbori_1.connect(sotenbori_2, "Sotenbori 1 to Sotenbori 2")
    sotenbori_2.connect(colosseum_1, "Sotenbori 2 to Colosseum 1")
    sotenbori_3.connect(colosseum_3, "Sotenbori 3 to Colosseum 3")
    sotenbori_3.connect(sotenbori_4, "Sotenbori 3 to Sotenbori 4")
    sotenbori_4.connect(colosseum_4, "Sotenbori 4 to Colosseum 4")
    colosseum_1.connect(pocket_circuit_1, "Colosseum 1 to Pocket Circuit 1")
    colosseum_1.connect(colosseum_2, "Colosseum 1 to Colosseum 2")
    colosseum_1.connect(sotenbori_3, "Colosseum 1 to Sotenbori 3")
    colosseum_2.connect(pocket_circuit_2, "Colosseum 2 to Pocket Circuit 2")
    colosseum_3.connect(pocket_circuit_3, "Colosseum 3 to Pocket Circuit 3")
    colosseum_4.connect(pocket_circuit_4, "Colosseum 4 to Pocket Circuit 4")
    
    # The region.connect helper even allows adding a rule immediately.
    # We'll talk more about rule creation in the set_all_rules() function in rules.py.
    #sotenbori_akame_3.connect(colosseum_bottom, "Sotenbori Akame 3 to Colosseum", lambda state: state.has("Key", world.player))

    # Some Entrances may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # In this case, we previously created an extra "Top Middle Room" region that we now need to connect to Overworld.
    #if world.options.hammer:
    #    pocket_circuit = world.get_region("Pocket Circuit")
    #    colosseum_bottom.connect(pocket_circuit, "Colosseum to Pocket Circuit")
