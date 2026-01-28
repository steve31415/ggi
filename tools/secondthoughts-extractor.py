#!/usr/bin/env python3
"""
Command-line utility to extract information from secondthoughts.ai articles
and create corresponding MDX files and directories.
Usage: python extract_article_info.py <URL>
"""

import sys
import os
import re
from urllib.request import urlopen, Request
from urllib.error import URLError
from html.parser import HTMLParser


class ArticleParser(HTMLParser):
    """Custom HTML parser to extract specific article information."""
    
    def __init__(self):
        super().__init__()
        self.title = None
        self.description = None
        self.author = None
        self.in_title = False
        self.current_tag = None
        self.current_attrs = {}
    
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.current_attrs = dict(attrs)

        # Check for title tag with data-rh or data-preact-helmet
        if tag == 'title' and ('data-rh' in dict(attrs) or 'data-preact-helmet' in dict(attrs)):
            self.in_title = True

        # Check for meta tags
        if tag == 'meta':
            attrs_dict = dict(attrs)

            # Description meta tag (with data-rh or data-preact-helmet)
            if (('data-rh' in attrs_dict or 'data-preact-helmet' in attrs_dict) and
                attrs_dict.get('name') == 'description'):
                self.description = attrs_dict.get('content', '')
            
            # Author meta tag
            if attrs_dict.get('name') == 'author':
                self.author = attrs_dict.get('content', '')
    
    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
    
    def handle_endtag(self, tag):
        if tag == 'title' and self.in_title:
            self.in_title = False


def extract_date_published(html_content):
    """Extract the datePublished value from the HTML content."""
    pattern = r'"datePublished":"(\d{4}-\d{2}-\d{2})T[^"]*"'
    match = re.search(pattern, html_content)
    if match:
        return match.group(1)
    return None


def fetch_and_extract(url):
    """Fetch the URL and extract required information."""
    # Validate URL format
    base_url = "https://secondthoughts.ai/p/"
    if not url.startswith(base_url):
        raise ValueError(f"URL must start with {base_url}")
    
    # Extract variable portion
    variable_portion = url[len(base_url):]
    if not variable_portion:
        raise ValueError("URL must include a path after /p/")
    
    # Fetch the webpage
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            html_content = response.read().decode('utf-8')
    except URLError as e:
        raise Exception(f"Failed to fetch URL: {e}")
    
    # Parse HTML
    parser = ArticleParser()
    parser.feed(html_content)
    
    # Extract date published
    date_published = extract_date_published(html_content)
    
    # Return results
    results = {
        'variable_portion': variable_portion,
        'title': parser.title,
        'description': parser.description,
        'author': parser.author,
        'date_published': date_published
    }
    
    return results


def create_mdx_file(slug, title, subtitle, author, date):
    """Create an MDX file with the extracted information."""
    # Verify posts directory exists
    if not os.path.isdir('posts'):
        print("Error: 'posts' directory not found in current directory", file=sys.stderr)
        sys.exit(1)
    
    # Create MDX content
    mdx_content = f'''---
title: "{title or ''}"
subtitle: "{subtitle or ''}"
authors: "{author or ''}"
date: "{date or ''}"
---
'''
    
    # Write MDX file
    mdx_path = os.path.join('posts', f'{slug}.mdx')
    try:
        with open(mdx_path, 'w', encoding='utf-8') as f:
            f.write(mdx_content)
        print(f"Created MDX file: {mdx_path}")
    except IOError as e:
        print(f"Error creating MDX file: {e}", file=sys.stderr)
        sys.exit(1)


def create_image_directory(slug):
    """Create a subdirectory in public/post-images for the article."""
    # Create public/post-images if it doesn't exist
    base_path = os.path.join('public', 'post-images')
    if not os.path.exists(base_path):
        try:
            os.makedirs(base_path)
        except OSError as e:
            print(f"Error creating public/post-images directory: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Create slug subdirectory
    image_dir = os.path.join(base_path, slug)
    if not os.path.exists(image_dir):
        try:
            os.makedirs(image_dir)
            print(f"Created image directory: {image_dir}")
        except OSError as e:
            print(f"Error creating image directory: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Image directory already exists: {image_dir}")


def main():
    """Main function to handle command-line execution."""
    # Check command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python extract_article_info.py <URL>", file=sys.stderr)
        print("Example: python extract_article_info.py https://secondthoughts.ai/p/ai-agent-security", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    
    try:
        # Extract information
        info = fetch_and_extract(url)
        
        # Output results (one per line)
        print(info['variable_portion'] or '')
        print(info['title'] or '')
        print(info['description'] or '')
        print(info['author'] or '')
        print(info['date_published'] or '')
        
        # Create MDX file and image directory
        if info['variable_portion']:
            create_mdx_file(
                info['variable_portion'],
                info['title'],
                info['description'],
                info['author'],
                info['date_published']
            )
            create_image_directory(info['variable_portion'])
        else:
            print("Error: No slug extracted from URL", file=sys.stderr)
            sys.exit(1)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
