from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import YakuzaGaiden


def create_and_connect_regions(world: YakuzaGaiden) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: YakuzaGaiden) -> None:

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

    regions = [yokohama, sotenbori_1, sotenbori_2, sotenbori_3, sotenbori_4, colosseum_1, colosseum_2, colosseum_3, colosseum_4, pocket_circuit_1, pocket_circuit_2, pocket_circuit_3, pocket_circuit_4]

    world.multiworld.regions += regions


def connect_regions(world: YakuzaGaiden) -> None:

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
