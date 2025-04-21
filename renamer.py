import os
import re
import argparse
from ebooklib import epub


def sanitize_filename(name):
    """
    Removes invalid characters, dots, commas, and replaces spaces with underscores.
    """
    name = re.sub(r'[\\/*?:"<>|.,]', "", name)
    return name.replace(" ", "_")


def rename_epub_files(folder_path, recursive=False):
    """
    Renames epub files in the given folder.

    Args:
        folder_path (str): The path to the folder containing epub files.
        recursive (bool, optional): If True, renames files in subfolders as
        well. Defaults to False.
    """
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith(".epub"):
                file_path = os.path.join(root, filename)
                try:
                    book = epub.read_epub(file_path)

                    # Get author and title
                    title = book.get_metadata("DC", "title")
                    creator = book.get_metadata("DC", "creator")

                    title_text = (
                        sanitize_filename(title[0][0].strip()) if title else None
                    )
                    author_text = (
                        sanitize_filename(creator[0][0].strip()) if creator else None
                    )

                    if not title_text:
                        print(f"⚠️ Skipped (title not found): {filename}")
                        continue

                    if author_text and author_text != "Unknown":
                        new_filename = f"{author_text}__{title_text}.epub"
                    else:
                        new_filename = f"{title_text}.epub"

                    new_file_path = os.path.join(root, new_filename)

                    # Avoid overwriting
                    if os.path.exists(new_file_path):
                        print(f"❌ File already exists: {new_filename}")
                        continue

                    os.rename(file_path, new_file_path)
                    print(f"✅ Renamed: {filename} → {new_filename}")

                except Exception as e:
                    print(f"❌ Error processing {filename}: {e}")
        if not recursive:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename epub files based on metadata.")
    parser.add_argument("folder", help="Path to the folder containing epub files.")
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Rename files in subfolders as well.",
    )

    args = parser.parse_args()

    rename_epub_files(args.folder, args.recursive)
