from docutils import nodes
from docutils.parsers.rst import directives, Directive, roles

from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension

import xml.etree.ElementTree as etree


class Center(Directive):
    required_arguments = 0
    optional_arguments = 0
    option_spec = {}
    has_content = True

    def run(self):
        # Center the content (and pad it a bit to show that it is centered).
        node = nodes.block_quote(classes=["text-center"])
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


MSC_BASE_URL = "https://github.com/matrix-org/matrix-spec-proposals/pull/%s"


def msc_reference_role(
    role, rawtext, text, lineno, inliner, options=None, content=None
):
    """
    Link to a Matrix Spec Change as: :msc:`1234` or a specific section as :msc:`1234#overview`.
    """
    # See docutils.parsers.rst.roles.rfc_reference_role.
    options = options or {}
    msc_num = nodes.unescape(text)
    try:
        msc_num = int(msc_num)
        if msc_num < 1:
            raise ValueError()
    except ValueError:
        msg = inliner.reporter.error(
            "MSC number must be a number greater than or equal to 1; "
            '"%s" is invalid.' % text,
            line=lineno,
        )
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    ref = MSC_BASE_URL % msc_num
    node = nodes.reference(rawtext, f"MSC{msc_num}", refuri=ref, **options)
    return [node], []


def register():
    # Add a role for a strikethrough on text, can be used like:
    #
    #   :strike:`text to have a strikethrough`
    role = roles.CustomRole(
        "strike", roles.generic_custom_role, {"class": ["strike"]}, []
    )
    roles.register_local_role("strike", role)

    # Add a role for Matrix Spec Changes, can be used like:
    #
    #   :msc:`1234` or :msc:`1234#section`
    roles.register_local_role("msc", msc_reference_role)

    # Add a directive to center content, can be used lke:
    #
    #   .. center::
    #
    #       Some content to center.
    directives.register_directive("center", Center)


class MscInlineProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element("a")
        el.set("href", MSC_BASE_URL % m.group(1))
        el.text = f"MSC{m.group(1)}"
        return el, m.start(0), m.end(0)


class MscExtension(Extension):
    def extendMarkdown(self, md):
        MSC_PATTERN = r"\[MSC(\d+)\]"
        md.inlinePatterns.register(MscInlineProcessor(MSC_PATTERN, md), "msc", 175)
