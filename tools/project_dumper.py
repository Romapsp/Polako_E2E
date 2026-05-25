import os

EXCLUDE_DIRS = {
    '.venv',
    'env',
    '.env',
    '__pycache__',
    '.git',
    '.pytest_cache',
    '.idea',
    '.vscode',
    'artifacts'
}

EXCLUDE_FILES = {
    '.env',
    'project_dump.txt',
    'full_project_dump.txt'
}


EXCLUDE_EXTENSIONS = {
    '.pyc', '.pyo', '.pyd', '.db', '.png', '.jpg', '.jpeg', '.bin', '.exe', '.zip'
}

OUTPUT_FILE = "full_project_dump.txt"


def generate_project_dump():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    output_path = os.path.join(current_dir, OUTPUT_FILE)

    with open(output_path, 'w', encoding='utf-8') as f_out:
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                if file in EXCLUDE_FILES or file == os.path.basename(__file__):
                    continue

                if any(file.endswith(ext) for ext in EXCLUDE_EXTENSIONS):
                    continue

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_root)

                f_out.write("=" * 60 + "\n")
                f_out.write(f"FILE: {relative_path}\n")
                f_out.write("=" * 60 + "\n\n")

                try:
                    with open(file_path, 'r', encoding='utf-8') as f_in:
                        f_out.write(f_in.read())
                except Exception as e:
                    f_out.write(f"[ОШИБКА ЧТЕНИЯ ФАЙЛА: {e}]\n")

                f_out.write("\n\n")

    print(f"✅ Готово! Секреты и виртуальное окружение пропущены.")
    print(f"📍 Файл: {output_path}")


if __name__ == "__main__":
    generate_project_dump()