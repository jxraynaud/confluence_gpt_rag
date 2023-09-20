import re

def split_markdown_document(content: str, depth: int = 3) -> list[str]:
    """
    Split a Markdown document into an array of strings using titles and subtitles.

    Args:
        content (str): The content of the Markdown document.
        depth (int, optional): The depth at which to split the content. Defaults to 3.

    Returns:
        list[str]: The array of strings split by titles and subtitles.
    """

    title_pattern = r'^#{1,' + str(depth) + '} '

    split_by_title = []
    acc = ''
    current_titles = []
    previous_was_title = False

    for line in content.splitlines():
        if re.match(title_pattern, line):
            if previous_was_title is not True and acc:
                # add the previous acc as we are in a new section
                split_by_title.append(acc.strip())
                # reset the acc
                acc = ''
            # it's a title, add it to the list of current titles
            nbr_of_hash = len(line) - len(line.lstrip("#"))
            # remove the titles that aren't relevant anymore
            current_titles = current_titles[:(nbr_of_hash - 1)]
            current_titles.append(line)
            previous_was_title = True
        else:
            if previous_was_title:
                # add the titles
                acc += '\n'.join(current_titles) + '\n'
                # reset the current titles
                current_titles = current_titles[:-1]
            previous_was_title = False
            acc += line + '\n'

    # Append the last accumulated content
    if acc:
        split_by_title.append(acc.strip())

    return split_by_title
