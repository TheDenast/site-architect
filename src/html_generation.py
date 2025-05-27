from pathlib import Path
from src.md import extract_title
from src.conversions import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    # Get project root (assuming this file is in src/)
    project_root = Path(__file__).parent.parent

    # Convert to absolute paths
    from_abs = project_root / from_path
    template_abs = project_root / template_path
    dest_abs = project_root / dest_path

    print(f"Generating page from {from_abs} to {dest_abs} using {template_abs}")

    # Read markdown file
    markdown_content = Path(from_abs).read_text(encoding="utf-8")

    # Read template file
    template_content = Path(template_abs).read_text(encoding="utf-8")

    # Convert markdown to HTML (placeholder for your function)
    html_content = markdown_to_html_node(markdown_content).to_html()

    # Extract title from markdown
    title = extract_title(markdown_content)

    # Replace placeholders in template
    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    # Create destination directory if it doesn't exist
    dest_file = Path(dest_abs)
    dest_file.parent.mkdir(parents=True, exist_ok=True)

    # Write the generated HTML to destination
    _ = dest_file.write_text(full_html, encoding="utf-8")


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    # Get project root (assuming this file is in src/)
    project_root = Path(__file__).parent.parent

    # Convert to absolute paths
    content_dir = project_root / dir_path_content
    dest_dir = project_root / dest_dir_path

    if not content_dir.exists():
        raise FileNotFoundError(f"Content directory not found: {content_dir}")

    # Recursively process all .md files
    for item in content_dir.rglob("*.md"):
        # Calculate relative path from content dir
        rel_path = item.relative_to(content_dir)

        # Change extension from .md to .html
        html_rel_path = rel_path.with_suffix(".html")

        # Build destination path
        dest_file_path = dest_dir / html_rel_path

        # Convert back to relative paths for generate_page
        from_path_rel = str(item.relative_to(project_root))
        dest_path_rel = str(dest_file_path.relative_to(project_root))

        # Generate the page
        generate_page(from_path_rel, template_path, dest_path_rel)
