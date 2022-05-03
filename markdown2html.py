#!/usr/bin/python3
"""This module converts a Markdown file to HTML given certain specifications.
"""
import sys
import re
import hashlib

symbols = {
    "h": "#",
    "ul": "-",
    "ol": "*"
}

regex_hash = {
    "b": r"\*{2}([^\*]*)\*{2}",
    "em": r"_{2}([^_]*)_{2}",
    "no_c": r"\({2}([^\(\)]*)\){2}",
    "md5": r"\[{2}([^\[\]]*)\]{2}",
}


def replacement(match_grp, tag):
    """Returns a string replacement given a certain tag
    Args:
        match_grp (str): The match group to be replaced.
        tag (str): The tag to operate the replacement.
    Returns:
        str: The replaced string.
    """
    if match_grp is not None:
        if tag in ["b", "em"]:
            return f"<{tag}>{match_grp.group()[2:-2]}</{tag}>"
        if tag == "no_c":
            return match_grp.group()[2:-2].replace("c", "").replace("C", "")
        if tag == "md5":
            return hashlib.md5(match_grp.group()[2:-2].encode()).hexdigest()


def format_text(content):
    """Returns a formatted string depending on certain tags using regex.
    Args:
        content (str): The content to be formatted.
    Returns:
        str: The formatted content.
    """
    for tag, regex in regex_hash.items():
        content = re.sub(regex_hash[tag],
                         lambda match_grp: replacement(match_grp, tag),
                         content)
    return content


def tag_parse(option, **kwargs):
    """Parses a string depending on the option passed as argument and calls
    the corresponding function.
    Args:
        option (str): The function to call.
        **kwargs: Keyword arguments to be passed to the functions.
    Returns:
        str: The parsed content.
    """
    tag_dict = {
        "#": h,
        "-": ul,
        "*": ol
    }
    return tag_dict.get(option)(**kwargs)


def h(symbol, content, output, tag_stack=None):
    """Formats a string with the h tag.
    Args:
        symbol (str): The original markdown symbol
        content (str): The content to be formatted.
        output (:obj:`list` of :obj:`str`): The final output list to be
                                            written to file.
        tag_stack (:obj:`list` of :obj:`str`, optional): The tag stack
    Returns:
        str: The line formatted with its h tag.
    """
    tag = f"h{len(symbol)}"
    output.append(f"<{tag}>{content}</{tag}>")


def ul(content, output, tag_stack, symbol=None):
    """Formats a string with the ul - li tags.
    Args:
        content (str): The content to be formatted.
        output (:obj:`list` of :obj:`str`): The final output list to be
                                            written to file.
        tag_stack (:obj:`list` of :obj:`str`): The tag stack
        symbol (str, optional): The original markdown symbol
    Returns:
        str: The line formatted with its ul tag.
    """
    if "ul" not in tag_stack:
        tag_stack.append("ul")
        output.append("<ul>")
    output.append(f"  <li>{content}</li>")


def ol(content, output, tag_stack, symbol=None):
    """Formats a string with the ol - li tags.
    Args:
        content (str): The content to be formatted.
        output (:obj:`list` of :obj:`str`): The final output list to be
                                            written to file.
        tag_stack (:obj:`list` of :obj:`str`): The tag stack
        symbol (str, optional): The original markdown symbol
    Returns:
        str: The line formatted with its ol tag.
    """
    if "ol" not in tag_stack:
        tag_stack.append("ol")
        output.append("<ol>")
    output.append(f"  <li>{content}</li>")


def parse(content):
    """The main parsing function. Converts Markdown content to HTML formatting.
    Args:
        content (str): The content to be formatted.
    Returns:
        :obj:`list` of :obj:`str`: The list of formatted strings to be written.
    """
    tag_stack = []
    parsed_html = []

    for line in content:
        line = line.strip("\n")

        if len(line) == 0:
            if "p" in tag_stack:
                parsed_html.append("</p>")
                tag_stack.pop()
            continue

        line = line.split(" ")
        symbol = line[0]
        symbol_first_char = symbol[0]
        symbol_size = len(symbol)

        if len(tag_stack) != 0 \
                and tag_stack[-1] != "p" \
                and symbols[tag_stack[-1]] != symbol_first_char:
            parsed_html.append(f"</{tag_stack[-1]}>")
            tag_stack.pop()

        line_content = format_text(" ".join(line[1:])) \
            if len(line[1:]) > 0 else ""
        kwargs = {
            "symbol": symbol,
            "content": line_content,
            "output": parsed_html,
            "tag_stack": tag_stack
        }
        if symbol_first_char == "#" and 1 <= symbol_size <= 6:
            tag_parse(symbol_first_char, **kwargs)
        elif symbol_first_char in ["*", "-"] and symbol_size == 1:
            tag_parse(symbol_first_char, **kwargs)
        else:
            if "p" not in tag_stack:
                tag_stack.append("p")
                parsed_html.append("<p>")
            else:
                parsed_html.append("    <br />")
            line_content = format_text(" ".join(line))
            parsed_html.append(f"  {line_content}")

    if len(tag_stack) != 0:
        parsed_html.append(f"</{tag_stack[-1]}>")
        tag_stack.pop()

    return "\n".join(parsed_html) + "\n"


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)
    try:
        src_filename = args[0]
        dest_filename = args[1]
        with open(src_filename, 'r') as src_file:
            src_content = src_file.readlines()
    except FileNotFoundError:
        sys.stderr.write(f"Missing {src_filename}\n")
        sys.exit(1)
    else:
        with open(dest_filename, 'w') as dest_file:
            dest_file.write(parse(src_content))
        sys.exit(0)
