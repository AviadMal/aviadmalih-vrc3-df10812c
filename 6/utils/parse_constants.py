import re
import os



# דפוס למציאת שורות constant
CONST_PATTERN = re.compile(r"^\s*constant\s+(\w+)\s*:\s*([\w_\(\)\s]+)\s*:=\s*(.*?);(?:\s*--(.*))?\s*$")

def parse_constants(filename):
    constants = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            match = CONST_PATTERN.match(line)
            if match:
                name = match.group(1)
                type_ = match.group(2).strip()
                value = match.group(3).strip()
                comment = match.group(4).strip() if match.group(4) else ''
                constants.append({'name': name, 'type': type_, 'value': value, 'comment': comment})
    return constants

# --- new function ---
def update_constants_in_vhdl(vhdl_path, updates):
    """
    updates: dict {constant_name: new_value}
    Updates only the value of the constant, preserves type, comments, and all other code.
    Returns True if any change was made, False otherwise.
    """
    # Case-insensitive mapping
    updates_ci = {k.lower(): v for k, v in updates.items()}
    changed = False
    lines = []
    with open(vhdl_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = CONST_PATTERN.match(line)
            if match:
                name = match.group(1)
                type_ = match.group(2)
                value = match.group(3)
                comment = match.group(4) if match.group(4) else ''
                if name.lower() in updates_ci:
                    new_value = str(updates_ci[name.lower()])
                    if value.strip() != new_value:
                        # שמור רווחים כמו במקור
                        prefix = line[:match.start(3)]
                        suffix = line[match.end(3):]
                        line = f"{prefix}{new_value}{suffix}"
                        changed = True
            lines.append(line)
    if changed:
        with open(vhdl_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    return changed


def update_all_vhdl_from_config(config):
    """
    For a configparser.ConfigParser object, update all VHDL files according to the [CONSTANT] section.
    Returns a dict {path: changed} for each file updated.
    """
    if not config.has_section('CONSTANT'):
        return {}
    items = list(config.items('CONSTANT'))
    vhdl_updates = {}  # {abs_path: {const_name: value}}
    base_dir = os.getcwd()
    current_path = None
    for key, value in items:
        if key.startswith('path'):
            rel_path = value
            abs_path = os.path.abspath(os.path.join(base_dir, rel_path))
            current_path = abs_path
            if current_path not in vhdl_updates:
                vhdl_updates[current_path] = {}
        else:
            if current_path:
                vhdl_updates[current_path][key] = value
    results = {}
    for path, updates in vhdl_updates.items():
        results[path] = update_constants_in_vhdl(path, updates)
    return results


def main():
    VHDL_FILE = 'KOKO.vhd'
    constants = parse_constants(VHDL_FILE)
    for c in constants:
        print(f"{c['name']} ({c['type']}): {c['value']} {c['comment']}")

if __name__ == '__main__':
    main() 
