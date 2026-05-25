from pathlib import Path


def generate_project_tree():
    current_script = Path(__file__).resolve()
    project_root = current_script.parent.parent
    output_file = project_root / "tools" / "project_tree.txt"


    exclude_dirs = {
        ".git", "__pycache__", ".venv", "venv",
        ".idea", ".vscode", "build", "dist",
        ".pytest_cache"
    }

    def build_tree(path: Path, prefix=""):
        lines = []
        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))

        for i, item in enumerate(items):
            if item.name in exclude_dirs:
                continue

            connector = "└── " if i == len(items) - 1 else "├── "
            lines.append(prefix + connector + item.name)

            if item.is_dir():
                extension = "    " if i == len(items) - 1 else "│   "
                lines.extend(build_tree(item, prefix + extension))

        return lines

    try:
        tree_lines = [project_root.name]
        tree_lines.extend(build_tree(project_root))

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(tree_lines))

        print(f"✅ Дерево проекта сохранено: {output_file}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    generate_project_tree()