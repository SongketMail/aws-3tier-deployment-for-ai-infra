#!/usr/bin/env python3
import os
import re
import datetime

def parse_yaml(front_matter_str):
    lines = front_matter_str.strip().split('\n')
    data = {}
    current_key = None
    for line in lines:
        if not line.strip():
            continue

        # Check for list items
        if line.strip().startswith('-') and current_key:
            val = line.strip()[1:].strip().strip('"\'')
            if isinstance(data[current_key], list):
                data[current_key].append(val)
            else:
                data[current_key] = [val]
            continue

        match = re.match(r'^([a-zA-Z0-9_\-]+)\s*:\s*(.*)$', line)
        if match:
            key = match.group(1).strip()
            val = match.group(2).strip()
            current_key = key
            # Check if it's an inline list like [a, b, c]
            if val.startswith('[') and val.endswith(']'):
                items = [i.strip().strip('"\'') for i in val[1:-1].split(',') if i.strip()]
                data[key] = items
            elif val.startswith('{') and val.endswith('}'):
                data[key] = val
            elif val == '':
                data[key] = []
            else:
                data[key] = val.strip('"\'')
    return data

def serialize_yaml(data):
    lines = []
    # Core OKF and Jekyll keys in consistent order
    keys_order = ['layout', 'okf_version', 'type', 'title', 'timestamp', 'topics']
    for k in keys_order:
        if k in data:
            val = data[k]
            if isinstance(val, list):
                list_str = ", ".join([f'"{x}"' for x in val])
                lines.append(f'{k}: [{list_str}]')
            else:
                if isinstance(val, str) and (':' in val or '#' in val or val.startswith('"') or val.startswith('{')):
                    lines.append(f'{k}: {val}')
                else:
                    lines.append(f'{k}: "{val}"')

    for k, val in sorted(data.items()):
        if k not in keys_order:
            if isinstance(val, list):
                list_str = ", ".join([f'"{x}"' for x in val])
                lines.append(f'{k}: [{list_str}]')
            else:
                if isinstance(val, str) and (':' in val or '#' in val or val.startswith('"') or val.startswith('{')):
                    lines.append(f'{k}: {val}')
                else:
                    lines.append(f'{k}: "{val}"')
    return "\n".join(lines)

def process_markdown_file(filepath, workspace_root):
    rel_path = os.path.relpath(filepath, workspace_root)
    print(f"Processing: {rel_path}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine if file has front matter
    has_front_matter = False
    stripped_content = content.lstrip()
    if stripped_content.startswith('---'):
        has_front_matter = True

    data = {}
    body_content = content

    if has_front_matter:
        parts = stripped_content.split('---', 2)
        if len(parts) >= 3:
            fm_str = parts[1]
            body_content = parts[2].lstrip('\n')
            data = parse_yaml(fm_str)
        else:
            # Malformed frontmatter
            body_content = content

    # 1. layout
    if 'layout' not in data:
        data['layout'] = 'default'

    # 2. okf_version
    data['okf_version'] = '0.1'

    # 3. title
    if 'title' not in data:
        title = None
        heading_match = re.search(r'^\s*#+\s+(.+)$', body_content, re.MULTILINE)
        if heading_match:
            title = heading_match.group(1).strip().strip('"\'')
        else:
            filename = os.path.basename(filepath)
            name_without_ext, _ = os.path.splitext(filename)
            title = name_without_ext.replace('_', ' ').replace('-', ' ').title()
        data['title'] = title

    # 4. type
    if 'type' not in data:
        filename = os.path.basename(filepath)
        if 'modules/' in filepath.replace('\\', '/'):
            data['type'] = 'Module Documentation'
        elif filename == 'AGENTS.md':
            data['type'] = 'Agent Operating Instructions'
        elif filename == 'README.md':
            data['type'] = 'Portal'
        elif filename == 'CHANGELOG.md':
            data['type'] = 'Changelog'
        elif filename == 'HISTORY.md':
            data['type'] = 'History'
        elif filename == 'SKILL.md':
            data['type'] = 'Skill'
        elif 'docs/' in filepath.replace('\\', '/'):
            data['type'] = 'Guide'
        else:
            data['type'] = 'Documentation'

    # 5. timestamp
    if 'timestamp' not in data:
        mtime = os.path.getmtime(filepath)
        try:
            from datetime import timezone
            dt = datetime.datetime.fromtimestamp(mtime, timezone.utc)
        except ImportError:
            dt = datetime.datetime.utcfromtimestamp(mtime)
        data['timestamp'] = dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    # 6. topics
    if 'topics' not in data:
        # If tags are already defined, use them as topics
        if 'tags' in data:
            if isinstance(data['tags'], list):
                data['topics'] = data['tags']
            else:
                data['topics'] = [x.strip() for x in data['tags'].strip('[]').split(',') if x.strip()]
        else:
            # Dynamic topic generation based on content and filename
            filename = os.path.basename(filepath)
            topics = ["aws", "cloud", "architecture"]
            filename_clean = os.path.splitext(filename)[0].lower()
            if filename_clean in ['readme', 'agents', 'changelog', 'history', 'skill']:
                topics.append(filename_clean)

            content_lower = body_content.lower()
            keywords = ["vpc", "alb", "asg", "rds", "waf", "elasticache", "valkey", "jumphost", "bastion", "route53", "dns", "ssl", "acm", "dr", "disaster-recovery", "gitlab", "ci-cd", "efs", "postgre", "gpu", "ragflow", "langfuse", "antigravity", "skills", "sovereignty", "compliance", "costing"]
            for kw in keywords:
                if kw in content_lower:
                    if kw == "postgre":
                        topics.append("postgresql")
                    elif kw == "dr":
                        topics.append("disaster-recovery")
                    elif kw == "ci-cd":
                        topics.append("cicd")
                    else:
                        topics.append(kw)
            data['topics'] = list(dict.fromkeys(topics))

    # Serialize and update
    new_fm_str = serialize_yaml(data)
    new_content = f"---\n{new_fm_str}\n---\n{body_content}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  -> Successfully updated with OKF v0.1 metadata")

def should_process_dir(dirpath):
    parts = dirpath.split(os.sep)
    for part in parts:
        if part.startswith('.') and part not in ['.agents']:
            return False
    return True

def main():
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print(f"Scanning markdown files under workspace: {workspace_root}")

    for root, _, files in os.walk(workspace_root):
        if not should_process_dir(root):
            continue
        for file in files:
            if file.endswith('.md'):
                process_markdown_file(os.path.join(root, file), workspace_root)

if __name__ == '__main__':
    main()
