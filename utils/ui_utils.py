import os

def wrap_filename_with_ellipsis(filename, max_len, max_lines):
    name, ext = os.path.splitext(filename)
    lines = []
    current_line = ""
    for char in name:
        current_line += char
        if len(current_line) >= max_len:
            lines.append(current_line)
            current_line = ""
            if len(lines) >= max_lines:
                break
    if current_line and len(lines) < max_lines:
        lines.append(current_line)
    if len(name) > max_len * max_lines:
        lines[-1] = lines[-1][:max_len-2] + "..."
    lines[-1] += ext
    return "\n".join(lines[:max_lines])