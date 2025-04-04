import os
import shutil
import sys
from internal_functions import generate_pages_recursive

def main():
    # Get base_path from CLI argument, default to "/"
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    if not base_path.endswith('/'):
        base_path += '/'

    # Set destination directory to 'docs' for GitHub Pages
    dest_dir = 'docs'

    # Clear the destination directory
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    # Copy static files from 'static' to 'docs'
    shutil.copytree('static', dest_dir)

    # Generate all pages with the base_path
    generate_pages_recursive('content', 'template.html', dest_dir, base_path)

if __name__ == "__main__":
    main()
