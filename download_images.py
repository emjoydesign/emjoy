#!/usr/bin/env python3
"""Download all Squarespace CDN images and update HTML references."""

import os
import re
import urllib.parse
import urllib.request
import ssl
import json

PROJECT_DIR = "/Users/emilythomas/projects/emjoy"
IMAGES_DIR = os.path.join(PROJECT_DIR, "images")

# Find all HTML files and extract image URLs
html_files = [f for f in os.listdir(PROJECT_DIR) if f.endswith(".html")]

# Build mapping: (html_file, full_url) -> local_path
url_pattern = re.compile(r'https://images\.squarespace-cdn\.com/[^"]+')

replacements = []  # list of (html_file, old_url, new_local_path)
seen = {}  # track (project, filename) -> count for collision handling

for html_file in sorted(html_files):
    filepath = os.path.join(PROJECT_DIR, html_file)
    with open(filepath, "r") as f:
        content = f.read()

    project = html_file.replace(".html", "")
    project_dir = os.path.join(IMAGES_DIR, project)
    os.makedirs(project_dir, exist_ok=True)

    for url in url_pattern.findall(content):
        # Strip query string for download, but keep full URL for replacement
        clean_url = url.split("?")[0]

        # Extract filename
        raw_filename = clean_url.rsplit("/", 1)[-1]
        filename = urllib.parse.unquote(raw_filename)

        # Extract Squarespace unique ID (path segment before filename)
        parts = clean_url.split("/")
        sq_id = parts[-2] if len(parts) >= 2 else "unknown"

        # Handle collisions (same filename, different image)
        key = (project, filename)
        if key in seen and seen[key] != clean_url:
            # Different image with same name — add ID prefix
            ext = filename.rsplit(".", 1)[-1] if "." in filename else ""
            base = filename.rsplit(".", 1)[0] if "." in filename else filename
            short_id = sq_id[:8]
            filename = f"{base}-{short_id}.{ext}"
            key = (project, filename)

        seen[key] = clean_url

        local_path = os.path.join(project_dir, filename)
        relative_path = f"images/{project}/{filename}"

        replacements.append((html_file, url, relative_path, clean_url, local_path))

# Deduplicate downloads (same URL may appear in multiple files)
downloads = {}
for html_file, url, rel_path, clean_url, local_path in replacements:
    downloads[clean_url] = (local_path, url)

# Download images
ctx = ssl.create_default_context()
total = len(downloads)
print(f"Downloading {total} unique images...")

failed = []
for i, (clean_url, (local_path, original_url)) in enumerate(downloads.items(), 1):
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        print(f"  [{i}/{total}] Already exists: {os.path.basename(local_path)}")
        continue

    # Use the URL with format parameter for best quality
    download_url = original_url if "?" in original_url else clean_url
    print(f"  [{i}/{total}] Downloading: {os.path.basename(local_path)}")
    try:
        req = urllib.request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            with open(local_path, "wb") as out:
                out.write(resp.read())
    except Exception as e:
        print(f"    FAILED: {e}")
        failed.append((clean_url, str(e)))

# Update HTML files
print("\nUpdating HTML files...")
for html_file in sorted(html_files):
    filepath = os.path.join(PROJECT_DIR, html_file)
    with open(filepath, "r") as f:
        content = f.read()

    original = content
    for hf, url, rel_path, clean_url, local_path in replacements:
        if hf == html_file:
            content = content.replace(url, rel_path)

    if content != original:
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  Updated: {html_file}")

print(f"\nDone! {total} images downloaded, {len(failed)} failed.")
if failed:
    print("Failed downloads:")
    for url, err in failed:
        print(f"  {url}: {err}")
