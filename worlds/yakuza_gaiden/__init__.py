from worlds.LauncherComponents import Component, Type, components, icon_paths, launch as launch_component

from .output import generate_output
from .world import YakuzaGaiden as YakuzaGaiden
from .settings import YakuzaGaidenSettings


def launch_client():
    from .Client import launch
    launch_component(launch, name="YakuzaGaidenClient")

icon_paths['yakuza_gaiden_icon'] = f"ap:{__name__}/Assets/icon.png"

components.append(
    Component(
        "Yakuza Gaiden Client",
        func=launch_client,
        component_type=Type.CLIENT,
        icon='yakuza_gaiden_icon',
    )
)