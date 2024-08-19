"""
Create redirects from old URLs to the currently hosted URLs.

This is vaguely based on https://github.com/getpelican/pelican-plugins/blob/master/permalinks/
"""
import logging

from pelican import signals
from pelican.generators import Generator

logger = logging.getLogger(__name__)


class RedirectGenerator(Generator):
    """
    Creates redirects based on the extra-slug metadata of articles.

    This is due to having articles which changed their slug over time.

    See (bad) commit cb6df6fc3420c474bd95cd03bbd1d8197682e405.
    """

    def generate_output(self, writer):
        """Generate redirect files"""
        logger.info("Generating redirect files")

        # Write it to each redirect path.
        redirect_save_as = self.settings.get("ARTICLE_SAVE_AS", "{slug}.html")

        for article in self.context["articles"]:
            if "extra-slug" not in article.metadata:
                continue

            # Make a copy of the metadata, replacing the slug with the redirect slug..
            url_format = article.url_format
            url_format["slug"] = article.metadata["extra-slug"]

            # Generate the output path.
            redirect_path = redirect_save_as.format(**url_format)

            # Similar to pelican.generators.ArticlesGenerator.generate_articles,
            # but uses the redirect path & redirect template.
            writer.write_file(
                redirect_path,
                self.get_template("article_redirect"),
                self.context,
                article=article,
                category=article.category,
                override_output=False,
                url=article.url,
                blog=True,
                relative_urls=self.settings["RELATIVE_URLS"],
            )


def get_generators(pelican_object):
    return [RedirectGenerator]


def register():
    signals.get_generators.connect(get_generators)
