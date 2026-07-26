from pathlib import Path


IGNORE_CONTENTS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "country_highlights",
    "country_shapes",
    "country_flags",
    "country_coa",
    "*.egg-info",
    "OLD",
}


def matches_ignore(path: Path) -> bool:
    """
    Check whether a directory's contents should not be printed.
    """
    return any(path.match(pattern) for pattern in IGNORE_CONTENTS)


def print_tree(path: Path, prefix: str = ""):
    """
    Print a directory tree recursively.
    """
    items = sorted(
        path.iterdir(),
        key=lambda x: (x.is_file(), x.name.lower())
    )

    for index, item in enumerate(items):
        is_last = index == len(items) - 1

        connector = "└── " if is_last else "├── "

        print(prefix + connector + item.name)

        # Show folder, but do not show its contents
        if item.is_dir() and not matches_ignore(item):
            extension = "    " if is_last else "│   "
            print_tree(item, prefix + extension)


def main():
    root = Path.cwd()

    print(root.name)
    print_tree(root)


if __name__ == "__main__":
    main()