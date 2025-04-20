import re


class LexicalHelpers:
    @staticmethod
    def get_readable_file_size_unit(size_value: int):
        units = ["B", "KB", "MB", "GB"]
        no_of_units = len(units)
        for level, unit in enumerate(units):
            if size_value < 1024 ** (level + 1) or (level + 1) == no_of_units:
                return f"{round(size_value / (1024 ** level), 2)}{unit}"

    @staticmethod
    def to_alphanumeric(value):
        return re.sub(r'[^a-zA-Z0-9]', '', value)
