"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from feedreader.models import Post


class PostContentTest(TestCase):
    def test_relative_url(self):
        """
        Tests that relative URLs are replaced by absolute URLs.
        """
        post = Post()
        post.link = "https://example.org"
        post.content = """<a href="/url">url</a>"""

        self.assertEqual(post.processed_content, """<a href="https://example.org/url">url</a>""")

    def test_iframe_replacement(self):
        """
        Tests that iframes are replaced by a link to the source.
        """
        post = Post()
        post.content = """<iframe src="https://example.org"></iframe>"""

        self.assertEqual(post.processed_content, """<a href="https://example.org">iframe</a>""")

    def test_iframe_no_src(self):
        """
        Tests that iframes with no src attribute get removed.
        """
        post = Post()
        post.content = """<iframe></iframe>"""

        self.assertEqual(post.processed_content, "")

    def test_iframe_removes_script(self):
        """
        Tests that scripts are removed from content.
        """
        post = Post()
        post.content = """<script src="https://example.org/script.js"></script>"""

        self.assertEqual(post.processed_content, "")
