import os
import re


def get_files_by_extension(working_directory, extension):
    """
    Get files by extension from directory

    Returns a list of FileData objects
    """
    regex = re.compile(r"\d+")
    files = []
    for file in os.listdir(working_directory):
        if file.endswith(f".{extension}") or file.endswith(extension):
            f = FileData(
                os.path.join(working_directory, file),
                int(regex.findall(file)[0]),
            )
            files.append(f)
            continue
    files.sort(key=lambda x: x.path)

    return files


def remove_old_files(path):
    regex = re.compile("^P[a-zA-Z]*[0-9]{5}\\.vtu")
    for file in os.listdir(path):
        if re.match(regex, file):
            os.remove(os.path.join(path, file))


class FileData:
    """
    Simple dataclass to store information about files
    """

    def __init__(self, path, id):
        self.path = path
        self.id = id
