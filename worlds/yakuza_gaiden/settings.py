from settings import Group, OptionalUserFolderPath


class YakuzaGaidenSettings(Group):
    class RandomizerFolder(OptionalUserFolderPath):
        """Folder where Yakuza Gaiden randomizer files are stored."""
        description = "Yakuza Gaiden randomizer output folder"

    randomizer_folder: RandomizerFolder | None = None