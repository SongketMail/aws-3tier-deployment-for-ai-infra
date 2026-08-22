#!/usr/bin/env python3
"""
Script Name: parse_llms.py
Description: Parses the project's llms.txt index file and compiles the referenced
             Markdown documentation into structured XML and aggregated plain text files.
             Provides a CLI and Python API for deep LLM-friendly content curation.
Usage:        python scripts/parse_llms.py
Author:       Harisfazillah Jamel (LinuxMalaysia)
"""

import os
import sys
import re
import html
import argparse

def parse_llms_file(text):
    """
    Parses the contents of an llms.txt file into a structured dictionary.

    Parameters:
    text (str): The raw text contents of the llms.txt file.

    Returns:
    dict: A dictionary containing title, summary, info, and sections of links.
    """
    sections_raw = re.split(r'^##\s*(.*?)$', text, flags=re.MULTILINE)
    header_raw = sections_raw[0].strip()

    title_match = re.search(r'^#\s*(.*?)$', header_raw, flags=re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""

    summary_match = re.search(r'^>\s*(.*?)$', header_raw, flags=re.MULTILINE)
    summary = summary_match.group(1).strip() if summary_match else ""

    info_lines = []
    for line in header_raw.split('\n'):
        if line.startswith('#') or line.startswith('>'):
            continue
        info_lines.append(line)
    info = "\n".join(info_lines).strip()

    sections = {}
    if len(sections_raw) > 1:
        for i in range(1, len(sections_raw), 2):
            sec_title = sections_raw[i].strip()
            sec_content = sections_raw[i+1].strip()

            links = []
            for line in sec_content.split('\n'):
                line = line.strip()
                if not line.startswith('-'):
                    continue
                match = re.match(r'^-\s*\[([^\]]+)\]\(([^)]+)\)(?:\s*:\s*(.*))?$', line)
                if match:
                    t = match.group(1).strip()
                    u = match.group(2).strip()
                    d = match.group(3).strip() if match.group(3) else ""
                    links.append({"title": t, "url": u, "desc": d})
            sections[sec_title] = links

    return {
        "title": title,
        "summary": summary,
        "info": info,
        "sections": sections
    }

def get_doc_content(filepath):
    """
    Reads the content of a local Markdown file, stripping Jekyll front matter blocks.

    Parameters:
    filepath (str): The relative path to the Markdown file.

    Returns:
    str: The file contents or an error message if the file is missing.
    """
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.strip().startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    return parts[2].strip()
            return content.strip()
    return f"[Error: File not found at {filepath}]"

def escape_xml(val):
    """
    Escapes special XML characters in a string value.

    Parameters:
    val (str): The raw string.

    Returns:
    str: The XML-escaped string.
    """
    if val is None:
        return ""
    return html.escape(str(val))

def create_ctx(text, optional=False):
    """
    Generates a structured XML context representation of the llms.txt resources.

    Parameters:
    text (str): The raw text of the llms.txt file.
    optional (bool): Whether to include sections designated as 'optional'.

    Returns:
    str: The fully formatted XML context file.
    """
    parsed = parse_llms_file(text)

    xml = []
    xml.append("<project>")
    xml.append(f"  <title>{escape_xml(parsed['title'])}</title>")
    xml.append(f"  <summary>{escape_xml(parsed['summary'])}</summary>")
    xml.append(f"  <info>{escape_xml(parsed['info'])}</info>")

    for sec_name, links in parsed["sections"].items():
        if sec_name.lower() == "optional" and not optional:
            continue
        xml.append(f'  <section name="{escape_xml(sec_name)}">')
        for link in links:
            url = link["url"]
            title = link["title"]
            desc = link["desc"]

            # Prefix relative skills/... paths with .agents/ so links resolve from the workspace root
            res_url = f".agents/{url}" if url.startswith("skills/") else url
            content = get_doc_content(res_url)

            xml.append(f'    <doc title="{escape_xml(title)}" url="{escape_xml(res_url)}" desc="{escape_xml(desc)}">')
            indented_content = "\n".join([f"      {line}" for line in content.split("\n")])
            xml.append(indented_content)
            xml.append("    </doc>")
        xml.append("  </section>")
    xml.append("</project>")

    return "\n".join(xml)

def create_llms_full(text):
    """
    Compiles all Markdown resources from the parsed llms.txt into a single text file.

    Parameters:
    text (str): The raw text of the llms.txt file.

    Returns:
    str: The concatenated full documentation file.
    """
    parsed = parse_llms_file(text)
    full_content = []

    full_content.append(f"# {parsed['title']} - Full Documentation")
    full_content.append("")
    full_content.append(parsed['summary'])
    full_content.append("")
    full_content.append(parsed['info'])
    full_content.append("")

    for sec_name, links in parsed["sections"].items():
        full_content.append(f"## {sec_name}")
        full_content.append("")
        for link in links:
            url = link["url"]
            title = link["title"]
            desc = link["desc"]

            # Prefix relative skills/... paths with .agents/ so links resolve from the workspace root
            res_url = f".agents/{url}" if url.startswith("skills/") else url

            full_content.append(f"### {title} ({res_url})")
            if desc:
                full_content.append(f"*{desc}*")
                full_content.append("")

            content = get_doc_content(res_url)
            full_content.append(content)
            full_content.append("")
            full_content.append("---")
            full_content.append("")

    return "\n".join(full_content)

def main():
    """
    CLI entry point to execute parsing of llms.txt and output context files.
    """
    parser = argparse.ArgumentParser(description="Parse llms.txt to XML context & consolidated text.")
    parser.add_argument("-i", "--input", default="llms.txt", help="Input llms.txt path (default: llms.txt)")
    parser.add_argument("-o", "--xml-output", default="llms.xml", help="Output XML path (default: llms.xml)")
    parser.add_argument("-f", "--full-output", default="llms-full.txt", help="Consolidated output path (default: llms-full.txt)")
    parser.add_argument("--optional", action="store_true", help="Include optional sections")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(args.input, 'r', encoding='utf-8') as file_in:
        text = file_in.read()

    # Generate XML context
    print(f"Generating XML context file at: {args.xml_output}")
    xml_content = create_ctx(text, optional=args.optional)
    with open(args.xml_output, 'w', encoding='utf-8') as file_xml:
        file_xml.write(xml_content)

    # Generate full documentation text
    print(f"Generating full consolidated documentation file at: {args.full_output}")
    full_text = create_llms_full(text)
    with open(args.full_output, 'w', encoding='utf-8') as file_full:
        file_full.write(full_text)

    print("Success: Curation files successfully generated.")

if __name__ == "__main__":
    main()
