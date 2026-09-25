from worlds.LauncherComponents import Component, Type, components, launch as launch_component

from .output import generate_output
from .world import YakuzaGaiden as YakuzaGaiden


def launch_client():
    from .Client import launch
    launch_component(launch, name="YakuzaGaidenClient")

components.append(
    Component(
        "Yakuza Gaiden Client",
        func=launch_client,
        component_type=Type.CLIENT,
    )
)