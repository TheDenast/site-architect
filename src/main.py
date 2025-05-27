import shutil
from pathlib import Path
from src.html_generation import generate_pages_recursive


def copy_files_recursive(src: Path, dst: Path) -> None:
    """Recursive copy with verbose logging for each file"""
    if not src.exists():
        return

    dst.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        src_item = src / item.name
        dst_item = dst / item.name

        if src_item.is_dir():
            print(f"Creating directory: {dst_item}")
            copy_files_recursive(src_item, dst_item)
        else:
            print(f"Copying: {src_item} -> {dst_item}")
            _ = shutil.copy2(src_item, dst_item)


def deploy_static_to_public() -> None:
    # Get absolute path of the script's directory (project root)
    script_dir = Path(__file__).parent.parent  # Go up from src/ to project root
    static_path = script_dir / "static"
    public_path = script_dir / "public"

    print(f"Static source: {static_path}")
    print(f"Public target: {public_path}")

    # Safety check - ensure we're in the right directory
    if not static_path.exists():
        raise FileNotFoundError(f"Static directory not found at {static_path}")

    # Clear public directory first
    if public_path.exists():
        print(f"Removing existing public directory: {public_path}")
        shutil.rmtree(public_path)

    print("Starting recursive copy...")
    copy_files_recursive(static_path, public_path)


def main() -> None:
    print("Starting static deployment...")
    deploy_static_to_public()
    print("Static files deployed to public/")

    generate_pages_recursive(
        "content/",
        "template.html",
        "public/",
    )


if __name__ == "__main__":
    main()
