from unittest.mock import MagicMock, patch
from grumpy_checks.lint import has_flake8, run_flake8
from grumpy_checks.checks import CheckResponse
import pyfakefs.fake_filesystem_unittest


class TestLintNoFlake8(pyfakefs.fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs(allow_root_user=False)

    def test_has_flake8(self):
        """Test has_flake8() -> CheckResponse"""
        res = has_flake8()
        # assert return type
        self.assertIsInstance(res, CheckResponse)
        self.assertFalse(res.result)

    @patch("grumpy_checks.lint._flake8_process")
    def test_run_flake8(self, mock_run):
        mock = MagicMock()
        mock.configure_mock(
            **{
                "stdout.decode.return_value":
                    "./scripts.py:3:1: E302 expected 2 blank lines, found 1",
                "stderr.decode.return_value":
                    "./scripts.py:3:1: E302 expected 2 blank lines, found 1",
                "returncode": 1
            }
        )
        mock_run.return_value = mock

        res = run_flake8()
        self.assertIsInstance(res, CheckResponse)
        self.assertFalse(res.result)
        # check that the mocked function was not actually called
        # and gave an early exit
        self.assertFalse(mock_run.called)
        self.assertEqual(res.info, "No flake 8 file")


class TestLintIssues(pyfakefs.fake_filesystem_unittest.TestCase):

    def setUp(self) -> None:
        self.setUpPyfakefs(allow_root_user=False)
        self.fs.create_file(".flake8")

    def test_has_flake8(self):
        res = has_flake8()
        self.assertIsInstance(res, CheckResponse)
        self.assertTrue(res.result)
        self.assertFalse(len(res.info))

    @patch("grumpy_checks.lint._flake8_process")
    def test_run_flake8(self, mock_run):
        mock = MagicMock()
        mock.configure_mock(
            **{
                "stdout.decode.return_value":
                    "./scripts.py:3:1: E302 expected 2 blank lines, found 1",
                "stderr.decode.return_value": "",
                "returncode": 1
            }
        )
        mock_run.return_value = mock
        res = run_flake8()
        self.assertIsInstance(res, CheckResponse)
        self.assertFalse(res.result)
        self.assertTrue(len(res.info))


class TestLintOK(pyfakefs.fake_filesystem_unittest.TestCase):

    def setUp(self) -> None:
        self.setUpPyfakefs(allow_root_user=False)
        self.fs.create_file(".flake8")

    def test_has_flake8(self):
        res = has_flake8()
        self.assertIsInstance(res, CheckResponse)
        self.assertTrue(res.result)
        self.assertFalse(len(res.info))

    @patch("grumpy_checks.lint._flake8_process")
    def test_run_flake8(self, mock_run):
        mock = MagicMock()
        mock.configure_mock(
            **{
                "stdout.decode.return_value": "",
                "stderr.decode.return_value": "",
                "returncode": 0
            }
        )
        mock_run.return_value = mock
        res = run_flake8()
        self.assertIsInstance(res, CheckResponse)
        self.assertTrue(res.result)
        self.assertFalse(len(res.info))
