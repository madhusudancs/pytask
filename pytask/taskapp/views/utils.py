"""Module containing taskapp views specific utility functions
"""

__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    ]


def get_intial_tags_for_chapter(textbook):
    """Returns the initial tag set for chapter/module for the textbook.

    Args:
        textbook: textbook entity for which the tags should be built.
    """

    tags = textbook.tags_field.split(',')
    rebuild_tags = []
    for tag in tags:
        tag.strip()
        if 'Textbook' not in tag:
            rebuild_tags.append(tag)

    initial_tags = ', '.join(rebuild_tags + ['Chapter'])

    return initial_tags
