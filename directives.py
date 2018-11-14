# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from docutils import nodes
from docutils.parsers.rst import directives, Directive, roles


class Center(Directive):
    required_arguments = 0
    optional_arguments = 0
    option_spec = {}
    has_content = True

    def run(self):
        # Center the content (and pad it a bit to show that it is centered).
        node = nodes.block_quote(classes=['text-center'])
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def register():
    # Add a role for a strikethrough on text, can be used like:
    #
    #   :strike:`text to have a strikethrough`
    role = roles.CustomRole('strike', roles.generic_custom_role, {'class': ['strike']}, [])
    roles.register_local_role('strike', role)

    # Add a directive to center content, can be used lke:
    #
    #   .. center::
    #
    #       Some content to center.
    directives.register_directive('center', Center)
