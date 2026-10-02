from pathlib import Path
import shutil
import threading
import importlib
import importlib.resources
import importlib.util
import json
import Utils


WORLD_DIR = Path(__file__).resolve().parent
ARCHIPELAGO_JSON = WORLD_DIR / "archipelago.json"
VERSION_FILE = ".yakuza_gaiden_version"

SOURCE_GAMEDATA = WORLD_DIR / "GameData"
SOURCE_ASSETS = WORLD_DIR / "Assets"

CONFIG_PATH = Path(
    Utils.user_path("YakuzaGaiden", "config.json")
)

def world_resource(name):
    package = importlib.import_module(__package__)

    return importlib.resources.files(package) / name

def get_randomizer_version():
    resource = world_resource("archipelago.json")

    with resource.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    return manifest["world_version"]

def get_folder_version(folder):
    version_path = Path(folder) / VERSION_FILE

    if not version_path.exists():
        return None

    try:
        return version_path.read_text(encoding="utf-8").strip()
    except Exception:
        return None

def save_folder_version(folder):
    version_path = Path(folder) / VERSION_FILE

    version_path.write_text(
        get_randomizer_version(),
        encoding="utf-8",
    )


def folder_is_valid(folder):
    folder = Path(folder)

    if not folder.exists():
        return False

    required_folders = [
        folder / "GameData",
        folder / "Assets",
        folder / "AP_PATCH",
    ]

    if not all(path.is_dir() for path in required_folders):
        return False

    return get_folder_version(folder) == get_randomizer_version()

def load_saved_folder():
    if not CONFIG_PATH.exists():
        return None

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)

        folder = config.get("randomizer_folder")

        if folder:
            return Path(folder)

    except Exception:
        pass

    return None


def save_folder(folder):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {"randomizer_folder": str(folder)},
            f,
            indent=4,
        )


def select_folder(log):
    import Utils
    
    folder = Utils.open_directory(
        "Select Yakuza Gaiden Randomizer Folder",
        "~",
    )

    if not folder:
        log("Folder selection cancelled.")
        return None

    folder = Path(folder)

    save_folder(folder)

    log(f"Randomizer folder selected: {folder}")

    return folder



def create_folder_layout(log, output_dir):
    output_dir = Path(output_dir)

    log("Creating randomizer folder layout...")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_gamedata = output_dir / "GameData"
    output_assets = output_dir / "Assets"
    output_ap_patch = output_dir / "AP_PATCH"

    log("Copying GameData...")

    if output_gamedata.exists():
        shutil.rmtree(output_gamedata)

    with importlib.resources.as_file(
        world_resource("GameData")
    ) as source_gamedata:
        shutil.copytree(
            source_gamedata,
            output_gamedata,
        )

    log("GameData copied.")

    log("Copying Assets...")

    if output_assets.exists():
        shutil.rmtree(output_assets)

    with importlib.resources.as_file(
        world_resource("Assets")
    ) as source_assets:
        shutil.copytree(
            source_assets,
            output_assets,
        )

    log("Assets copied.")

    log("Creating AP_PATCH folder...")

    output_ap_patch.mkdir(
        parents=True,
        exist_ok=True,
    )

    save_folder_version(output_dir)

    log("Randomizer folder ready.")

def run_randomizer(log, output_dir):
    output_dir = Path(output_dir)

    if not output_dir.exists():
        log("Randomizer folder does not exist.")
        log("Create the randomizer folder first.")
        return

    def task():
        try:
            log("Starting randomizer...")

            def load_script(name):
                resource = world_resource(
                    f"scripts/{name}.py"
                )

                with importlib.resources.as_file(resource) as script_path:
                    spec = importlib.util.spec_from_file_location(
                        name,
                        script_path,
                    )

                    module = importlib.util.module_from_spec(spec)
                    module.world_resource = world_resource
                    spec.loader.exec_module(module)

                    return module


            archipelago_item_creation = load_script(
                "archipelago_item_creation"
            )

            replace_items = load_script(
                "replace_items"
            )

            convert = load_script(
                "convert"
            )

            pipeline = [
                (
                    archipelago_item_creation.main,
                    "Generating Archipelago items",
                ),
                (
                    replace_items.main,
                    "Replacing game items",
                ),
                (
                    convert.main,
                    "Converting files",
                ),
            ]

            for func, description in pipeline:
                log(f"{description}...")

                func(output_dir)

                log(f"{description} complete.")

            log("Randomizer finished!")
            log("Enjoy the Rando!")

        except Exception as e:
            log(f"Randomizer failed: {e}")

            import logging
            logging.getLogger("Client").exception(
                "Randomizer error"
            )

    threading.Thread(
        target=task,
        daemon=True,
    ).start()