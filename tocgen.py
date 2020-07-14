"""Some basic ToC generation and sanitation helpers"""

import re
import glob
from os import path
import requests


def set_toc_titles():
    """
    Set texts for ToC links in top-level README.md from page headings

    ToC lines are expected to start with an asterisk.
    Pages are expected to have a first-level-heading as first line.
    """
    with open("README.md") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("*"):
            # search for linked document path
            match = re.search(r"(?<!\\)\((.*\.md)(?<!\\)\)", line)
            if match:
                fn = match.group(1)
                if not path.exists(fn):
                    raise ValueError(f"Linked document not found: {fn}")

                # retrieve and copy in the document title
                with open(fn) as f:
                    title = f.readline()[1:].strip()
                    if re.search(r'(?<!\\)[()]', title):
                        raise ValueError("Title may not contain un-escaped parentheses!")
                    line = re.sub(r"\[.*\]", f"[{title}]", line)

        new_lines.append(line)

    with open("README.md", "w") as f:
        f.write("".join(new_lines))


def add_toc_links():
    """
    Adds a link back to README.md for all sub-pages (in case it is not yet there)
    """
    md_files = glob.glob(path.join("pages", "*.md"))

    for md_file in md_files:
        with open(md_file) as f:
            lines = f.readlines()

        if "README.md" not in lines[-1]:
            lines.append("\n\n")
            lines.append("<<< Go back to the [table of contents](../README.md) "
                         "|| Opinions are mine, not necessarily those of [Vebeto GmbH](https://www.vebeto.de)")

        with open(md_file, "w") as f:
            f.write("".join(lines))


def check_links():
    """
    Check if all links in all markdown documents are alive.

    Only checks links formatted like [link text](link target).
    """
    md_files = glob.glob(path.join("pages", "*.md")) + ["README.md"]

    for md_file in md_files:
        with open(md_file) as f:
            lines = f.readlines()

        for line in lines:
            # search for link
            match = re.search(r"\]\((.*?)\)", line)
            if match:
                link = match.group(1)
                if len(link) == 0:
                    print(f"{md_file}: Empty URL found")

                if link.startswith("http"):
                    try:
                        requests.get(link)
                    except requests.HTTPError:
                        print(f"{md_file}: Linked URL not found: {link}")
                else:
                    link = path.join(path.dirname(md_file), link)
                    if not path.exists(link):
                        print(f"{md_file}: Linked file not found: {link}")


if __name__ == "__main__":
    set_toc_titles()
    add_toc_links()
    check_links()
