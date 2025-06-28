"""
Template tag for extracting and displaying note tags as a string.
"""

from django import template

register = template.Library()


def tags(note_tags):
    """Return a comma-separated string of tag names for a note."""
    return ', '.join([str(name) for name in note_tags.all()])


register.filter('tags', tags)

