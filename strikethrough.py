# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from docutils import nodes
from docutils.parsers.rst import roles


def register():
    base_role = roles.generic_custom_role
    role = roles.CustomRole('strike', base_role, {'class': ['strike']}, [])

    roles.register_local_role('strike', role)
