import importlib.resources
import importlib.util
import time
import shutil
from pathlib import Path


def main(base_dir=None):
    BASE_DIR = Path(base_dir) if base_dir is not None else Path.cwd()

    ROOT = BASE_DIR / "GameData_Output"
    ASSETS = BASE_DIR / "Assets"
    BIN_OUTPUT = BASE_DIR / "Gaiden_Rando"

    BIN_OUTPUT.mkdir(parents=True, exist_ok=True)

    rearmp_resource = world_resource("scripts/reARMP.py")

    with importlib.resources.as_file(rearmp_resource) as rearmp_path:
        spec = importlib.util.spec_from_file_location(
            "reARMP",
            rearmp_path,
        )

        reARMP = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(reARMP)

    for json_file in ROOT.rglob("*.bin.json"):
        print(f"Processing: {json_file}")

        reARMP.main(json_file, ROOT)

        # reARMP output no longer lands in root now!
        output_file = ROOT / (json_file.name + ".bin")

        timeout = 1
        start = time.time()

        while not output_file.exists():
            if time.time() - start > timeout:
                print(f"Timed out waiting for {output_file}")
                break
            time.sleep(0.25)

        if output_file.exists():
            
            relative_path = json_file.relative_to(ROOT)
            final_file = BIN_OUTPUT / relative_path.with_suffix("")

            final_file.parent.mkdir(parents=True, exist_ok=True)

            if final_file.exists():
                final_file.unlink()

            output_file.rename(final_file)

            print(f"Moved to: {final_file}")

    print("Done!")

    print("Creating zip archive...")

    # Copy metadata 
    shutil.copy2(ASSETS / "mod-image.ico", BIN_OUTPUT / "mod-image.ico")
    shutil.copy2(ASSETS / "mod-meta.yaml", BIN_OUTPUT / "mod-meta.yaml")
    shutil.copy2(ASSETS / "libcrypto-3-x64.dll", BIN_OUTPUT / "libcrypto-3-x64.dll")
    shutil.copy2(ASSETS / "libssl-3-x64.dll", BIN_OUTPUT / "libssl-3-x64.dll")
    shutil.copy2(ASSETS / "gaiden_hook_fresh.asi", BIN_OUTPUT / "gaiden_hook_fresh.asi")
    shutil.copy2(ASSETS / "item_mapping.csv", BIN_OUTPUT / "item_mapping.csv")
    shutil.copy2(ASSETS / "event_list.csv", BIN_OUTPUT / "event_list.csv")
    shutil.copy2(ASSETS / "progressive_items.json", BIN_OUTPUT / "progressive_items.json")
    shutil.copy2(ASSETS / "items.json", BIN_OUTPUT / "items.json")
    shutil.copy2(ASSETS / "locations.json", BIN_OUTPUT / "locations.json")
    shutil.copy2(ASSETS / "options.json", BIN_OUTPUT / "options.json")
    

    zip_path = shutil.make_archive( base_name=str(BIN_OUTPUT), format="zip", root_dir=BIN_OUTPUT.parent, base_dir=BIN_OUTPUT.name, )

    print(f"Created archive: {zip_path}")

    # Cleanup (delete folder after completion)

    if Path(zip_path).exists():
        print("Deleting output folder...")
        shutil.rmtree(BIN_OUTPUT)
        print(f"Deleted folder: {BIN_OUTPUT}")
    else:
        print("Zip failed — folder not deleted.")


if __name__ == "__main__":
    main()