import os
import shutil
from internal_functions import generate_pages_recursive

def main():
    """Generate the static site."""
    # Clear the public directory
    public_dir = 'public'
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    # Copy static files from 'static' to 'public'
    shutil.copytree('static', public_dir)

    # Generate all pages recursively
    generate_pages_recursive('content', 'template.html', public_dir)

if __name__ == "__main__":
    main()
