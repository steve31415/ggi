#!/usr/bin/env python3
"""
Automates adding a blog post to the GGI website.

Usage:
    python tools/add-post.py <post-url> <header-image>

Examples:
    python tools/add-post.py https://secondthoughts.ai/p/some-article ./image.jpg
    python tools/add-post.py https://secondthoughts.ai/p/some-article https://example.com/image.jpg
"""

import sys
import os
import subprocess
import tempfile
import re
from urllib.request import urlopen, Request
from urllib.error import URLError

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    sys.exit(1)


def run_git_pull():
    """Run git pull to ensure we have the latest code."""
    print("Running git pull...")
    result = subprocess.run(
        ["git", "pull"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Warning: git pull failed: {result.stderr}", file=sys.stderr)
    else:
        print("Git pull complete.")


def run_extractor(post_url):
    """Run the extractor script and return the slug."""
    print(f"Running extractor for {post_url}...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    extractor_path = os.path.join(script_dir, "secondthoughts-extractor.py")

    result = subprocess.run(
        [sys.executable, extractor_path, post_url],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error running extractor: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    # First line of output is the slug
    lines = result.stdout.strip().split('\n')
    if not lines:
        print("Error: Extractor produced no output", file=sys.stderr)
        sys.exit(1)

    slug = lines[0]
    print(f"Extractor complete. Slug: {slug}")

    # Print the rest of the extractor output
    for line in lines[1:]:
        print(f"  {line}")

    return slug


def download_image(url):
    """Download an image from a URL and return the path to a temp file."""
    print(f"Downloading image from {url}...")

    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            # Determine extension from content-type or URL
            content_type = response.headers.get('Content-Type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            elif 'webp' in content_type:
                ext = '.webp'
            else:
                # Try to get extension from URL
                ext = os.path.splitext(url.split('?')[0])[1] or '.jpg'

            # Create temp file
            fd, temp_path = tempfile.mkstemp(suffix=ext)
            with os.fdopen(fd, 'wb') as f:
                f.write(response.read())

            print(f"Downloaded to temp file: {temp_path}")
            return temp_path
    except URLError as e:
        print(f"Error downloading image: {e}", file=sys.stderr)
        sys.exit(1)


def process_image(image_path, output_path):
    """
    Process an image: crop to 4:3 aspect ratio and save as PNG.

    4:3 means width:height = 4:3, so height = width * 3/4.
    Center crop to achieve this ratio.
    """
    print(f"Processing image: {image_path}")

    try:
        img = Image.open(image_path)

        # Convert to RGB if necessary (removes alpha channel)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create white background for images with transparency
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        width, height = img.size
        target_ratio = 4 / 3  # width / height
        current_ratio = width / height

        if current_ratio > target_ratio:
            # Image is too wide, crop horizontally
            new_width = int(height * target_ratio)
            left = (width - new_width) // 2
            img = img.crop((left, 0, left + new_width, height))
            print(f"  Cropped horizontally: {width}x{height} -> {new_width}x{height}")
        elif current_ratio < target_ratio:
            # Image is too tall, crop vertically
            new_height = int(width / target_ratio)
            top = (height - new_height) // 2
            img = img.crop((0, top, width, top + new_height))
            print(f"  Cropped vertically: {width}x{height} -> {width}x{new_height}")
        else:
            print(f"  Image already 4:3 ratio: {width}x{height}")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save as PNG
        img.save(output_path, 'PNG')
        print(f"  Saved to: {output_path}")

    except Exception as e:
        print(f"Error processing image: {e}", file=sys.stderr)
        sys.exit(1)


def update_writing_spotlight(slug):
    """Update writing-spotlight.tsx to add the new slug at the beginning of the array."""
    print("Updating writing-spotlight.tsx...")

    file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "app", "(main)", "writing-spotlight.tsx"
    )

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the postSlugs array and add the new slug at the beginning
        # Pattern matches: const postSlugs = [
        #   "slug1",
        #   ...
        # ];
        pattern = r'(const postSlugs = \[\s*\n)(\s*)'
        match = re.search(pattern, content)

        if not match:
            print("Error: Could not find postSlugs array in writing-spotlight.tsx", file=sys.stderr)
            sys.exit(1)

        # Insert the new slug at the beginning of the array
        indent = match.group(2)
        new_entry = f'{indent}"{slug}",\n'
        new_content = content[:match.end(1)] + new_entry + content[match.end(1):]

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  Added '{slug}' to postSlugs array")

    except Exception as e:
        print(f"Error updating writing-spotlight.tsx: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("Usage: python tools/add-post.py <post-url> <header-image>", file=sys.stderr)
        print("", file=sys.stderr)
        print("Examples:", file=sys.stderr)
        print("  python tools/add-post.py https://secondthoughts.ai/p/article ./image.jpg", file=sys.stderr)
        print("  python tools/add-post.py https://secondthoughts.ai/p/article https://example.com/image.jpg", file=sys.stderr)
        sys.exit(1)

    post_url = sys.argv[1]
    image_source = sys.argv[2]

    # Change to repo root directory
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_root)
    print(f"Working directory: {repo_root}")

    # Step 1: Git pull
    run_git_pull()

    # Step 2: Run extractor
    slug = run_extractor(post_url)

    # Step 3: Process header image
    # Determine if image_source is a URL or local path
    if image_source.startswith('http://') or image_source.startswith('https://'):
        temp_image = download_image(image_source)
        image_path = temp_image
    else:
        if not os.path.exists(image_source):
            print(f"Error: Image file not found: {image_source}", file=sys.stderr)
            sys.exit(1)
        image_path = image_source
        temp_image = None

    output_path = os.path.join("public", "post-images", slug, "header.png")
    process_image(image_path, output_path)

    # Clean up temp file if we downloaded
    if temp_image and os.path.exists(temp_image):
        os.remove(temp_image)

    # Step 4: Update writing-spotlight.tsx
    update_writing_spotlight(slug)

    # Done
    print("")
    print("=" * 50)
    print(f"Successfully added post: {slug}")
    print("")
    print("Files created/modified:")
    print(f"  - posts/{slug}.mdx")
    print(f"  - public/post-images/{slug}/header.png")
    print(f"  - app/(main)/writing-spotlight.tsx")
    print("")
    print("Next steps:")
    print("  1. Review the changes")
    print("  2. Run 'npm run dev' to verify the post appears correctly")
    print("  3. Commit when satisfied")


if __name__ == "__main__":
    main()
