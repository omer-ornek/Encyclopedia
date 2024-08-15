def md_to_html(cont):
    html = ""
    lines = cont.split("\n")
    inside_paragraph = False
    inside_list = None  # Track if we're inside a list (None, 'ul', or 'ol')

    for i, line in enumerate(lines):
        line = line.rstrip()  # Remove trailing whitespace
        if not line:
            if inside_paragraph:
                html += "</p>\n"
                inside_paragraph = False
            if inside_list:
                html += f"</{inside_list}>\n"
                inside_list = None
            continue
        elif line[0] == "#":  # Check for header
            if inside_paragraph:
                html += "</p>\n"
                inside_paragraph = False
            if inside_list:
                html += f"</{inside_list}>\n"
                inside_list = None
            html += header(line)
        elif line[0] in "-+":  # Check for unordered list
            if inside_paragraph:
                html += "</p>\n"
                inside_paragraph = False
            if len(line) >= 2 and line[1] == " ":
                if inside_list != "ul":
                    if inside_list:
                        html += f"</{inside_list}>\n"
                    html += "<ul>\n"
                    inside_list = "ul"
                html += f"<li>{content(line[2:])}</li>\n"
        elif line[0].isdigit() and len(line) > 1 and line[1] == "." and len(line) > 2 and line[2] == " ":
            if inside_paragraph:
                html += "</p>\n"
                inside_paragraph = False
            if inside_list != "ol":
                if inside_list:
                    html += f"</{inside_list}>\n"
                html += "<ol>\n"
                inside_list = "ol"
            html += f"<li>{content(line[3:])}</li>\n"
        elif line[0] == "*":
            if inside_paragraph:
                html += "</p>\n"
                inside_paragraph = False
            if len(line) >= 2 and line[1] == " ":
                if inside_list != "ul":
                    if inside_list:
                        html += f"</{inside_list}>\n"
                    html += "<ul>\n"
                    inside_list = "ul"
                html += f"<li>{content(line[2:])}</li>\n"
            else:
                html += content(line)
        else:
            if inside_list:
                html += f"</{inside_list}>\n"
                inside_list = None
            if not inside_paragraph:
                html += "<p>\n"
                inside_paragraph = True
            html += content(line)
        
    if inside_paragraph:
        html += "</p>\n"

    if inside_list:
        html += f"</{inside_list}>\n"

    return html

def header(line):
    level = line.count("#")
    return f"<h{level}>{line[level:].strip()}</h{level}>\n"

def content(line):
    stack = []
    text = ""
    n = len(line)
    index = 0

    while index < n:
        if line[index] in "*_":
            symbol = line[index]
            count = 0
            start_index = index

            # Count the number of consecutive '*' or '_'
            while index < n and line[index] == symbol:
                count += 1
                index += 1

            # Handling bold (**) or italic (*)
            if count >= 2:  # Consider '**' at the start of a line
                if stack and stack[-1] == symbol:
                    text += "</b>"
                    stack.pop()
                else:
                    text += "<b>"
                    stack.append(symbol)
                continue
            elif count == 1:
                if stack and stack[-1] == symbol:
                    text += "</i>"
                    stack.pop()
                else:
                    text += "<i>"
                    stack.append(symbol)
                continue
        elif line[index] == "~":
            if stack and stack[-1] == "~":
                text += "</s>"
                stack.pop()
            else:
                text += "<s>"
                stack.append("~")
            continue
        elif line[index] == "[":
            index += 1
            start_index = index
            while index < n and line[index] != "]":
                index += 1
            end_index = index
            index += 2
            start_link = index
            while index < n and line[index] != ")":
                index += 1
            end_link = index
            text += f'<a href="{line[start_link:end_link]}">{line[start_index:end_index]}</a>'
            index += 1
            continue
        else:
            text += line[index]
        
        index += 1

    while stack:
        unmatched = stack.pop()
        if unmatched == "*":
            text += "*"
        elif unmatched == "_":
            text += "_"
        elif unmatched == "~":
            text += "~"

    return text
