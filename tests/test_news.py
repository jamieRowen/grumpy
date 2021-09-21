from grumpy_checks.checks import CheckResponse
import pyfakefs.fake_filesystem_unittest
from grumpy_checks.news import (
    has_newsfile, newsfile_format,
    news_version_matches_toml
)
from unittest.mock import MagicMock


class TestNewsNoNewsNoToml(pyfakefs.fake_filesystem_unittest.TestCase):
    """Test News No News No Toml

    Test case for both missing NEWS.md and
    missing pyproject.toml
    """

    def setUp(self) -> None:
        self.setUpPyfakefs(allow_root_user=False)

    def test_has_newsfile(self):
        res = has_newsfile()
        self.assertIsInstance(res, CheckResponse)
        self.assertFalse(res.result)
        self.assertEqual(res.info, "Missing NEWS.md")

    def test_newsfile_format(self):
        res = newsfile_format()
        self.assertIsInstance(res, CheckResponse)
        self.assertFalse(res.result)
        self.assertEqual(res.info, "Missing [NEWS.md, pyproject.toml]")

    def test_news_version_matches_toml(self):
        res = news_version_matches_toml()
        self.assertIsInstance(res, CheckResponse)
        self.assertFalse(res.result)
        self.assertEqual(res.info, "Missing [NEWS.md, pyproject.toml]")


class TestNewsNoToml(pyfakefs.fake_filesystem_unittest.TestCase):
    """Test News No Toml

    Test case for news functions when there is a NEWS.md
    but no pyproject.toml
    """

    def setUp(self) -> None:
        self.setUpPyfakefs(allow_root_user=False)
        self.fs.create_file("NEWS.md")

    def test_has_news(self):
        res = has_newsfile()
        self.assertIsInstance(res, CheckResponse)
        self.assertTrue(res.result)
        self.assertFalse(len(res.info))

    def test_newsfile_format(self):
        res = newsfile_format()
        self.assertIsInstance(res, CheckResponse)
        self.assertFalse(res.result)
        self.assertEqual(res.info, "Missing pyproject.toml")

    def test_news_version_matches_toml(self):
        res = news_version_matches_toml()
        self.assertIsInstance(res, CheckResponse)
        self.assertFalse(res.result)
        self.assertEqual(res.info, "Missing pyproject.toml")


class TestNewsNoNews(pyfakefs.fake_filesystem_unittest.TestCase):
    """Test News No Toml

    Test case for news functions when there is a NEWS.md
    but no pyproject.toml
    """

    def setUp(self) -> None:
        self.setUpPyfakefs(allow_root_user=False)
        self.fs.create_file("pyproject.toml")

    def test_has_news(self):
        res = has_newsfile()
        self.assertIsInstance(res, CheckResponse)
        self.assertFalse(res.result)
        self.assertTrue(len(res.info))

    def test_newsfile_format(self):
        res = newsfile_format()
        self.assertIsInstance(res, CheckResponse)
        self.assertFalse(res.result)
        self.assertEqual(res.info, "Missing NEWS.md")

    def test_news_version_matches_toml(self):
        res = news_version_matches_toml()
        self.assertIsInstance(res, CheckResponse)
        self.assertFalse(res.result)
        self.assertEqual(res.info, "Missing NEWS.md")


class TestNewsIssues(pyfakefs.fake_filesystem_unittest.TestCase):

    def setUp(self) -> None:
        self.setUpPyfakefs(allow_root_user=False)
        self.fs.create_file("NEWS.md")
        self.fs.create_file("pyproject.toml")

    def _create_mocks(self):
        mock_news = MagicMock()
        mock_news.return_value = """
##
        """


class TestNewsOK(pyfakefs.fake_filesystem_unittest.TestCase):
    pass
