import shutil
import sys
from pathlib import Path
from unidecode import unidecode
import re


def main():
    global TRUE_PATH
    if len(sys.argv) > 1:
        TRUE_PATH = Path(sys.argv[1])
        trash_sorting(sys.argv[1])


def is_dir_empty(path_argv: Path) -> bool:
    for element in path_argv.iterdir():
        return False
    return True


def normalize(path_argv: str) -> str:
    to_check_if_it_file = Path(path_argv)
    if to_check_if_it_file.suffix:
        extension_of_file = to_check_if_it_file.suffix
        path_argv = re.sub(extension_of_file, "", path_argv)
    new_name = unidecode(path_argv)
    new_name = ''.join(
        [item if item.isalnum() else '_' for item in new_name]) + (extension_of_file if to_check_if_it_file.suffix else "")
    return new_name


def trash_sorting(path_argv: str):
    path_argv = Path(path_argv)
    for element in path_argv.iterdir():
        if not element.name in ('video', 'audio', 'images', 'documents', 'archives'):
            if element.is_dir():
                it_dir = element.name
                new_name = normalize(it_dir)
                new_path = element.parent / new_name
                try:
                    element = element.rename(new_path)
                except Exception as e:
                    print(f"exeption - {e}")
                trash_sorting(element)
                if is_dir_empty(element):
                    element.rmdir()
            else:
                it_file = element.name
                new_name = normalize(it_file)
                new_path = element.with_name(new_name)
                element = element.rename(new_path)

                if element.suffix.lower() in ('.jpeg', '.png', '.jpg', '.svg'):
                    destination_dir = TRUE_PATH / 'images'
                    destination_dir.mkdir(exist_ok=True)
                    destination_dir = destination_dir / new_name
                    shutil.move(element, destination_dir)
                elif element.suffix in ('.avi', '.mp4', '.mov', '.mkv'):
                    destination_dir = TRUE_PATH / 'video'
                    destination_dir.mkdir(exist_ok=True)
                    destination_dir = destination_dir / new_name
                    shutil.move(element, destination_dir)
                elif element.suffix in ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'):
                    destination_dir = TRUE_PATH / 'documents'
                    destination_dir.mkdir(exist_ok=True)
                    destination_dir = destination_dir / new_name
                    shutil.move(element, destination_dir)
                elif element.suffix in ('.mp3', '.ogg', '.wav', '.amr'):
                    destination_dir = TRUE_PATH / 'audio'
                    destination_dir.mkdir(exist_ok=True)
                    destination_dir = destination_dir / new_name
                    shutil.move(element, destination_dir)
                elif element.suffix in ('.zip', '.gz', '.tar'):
                    destination_dir = TRUE_PATH / 'archives'
                    destination_dir.mkdir(exist_ok=True)
                    get_suffix = element.suffix
                    get_folder_name = re.sub(
                        get_suffix, "", element.name)
                    destination_dir = destination_dir / get_folder_name
                    destination_dir.mkdir(exist_ok=True)
                    shutil.unpack_archive(element, destination_dir)


if __name__ == "__main__":
    main()
