import unittest
from unittest.mock import MagicMock, PropertyMock, patch
from grumpy_checks.lint import has_flake8, run_flake8
from grumpy_checks.checks import CheckResponse
from pyfakefs.fake_filesystem_unittest import patchfs
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
                "stdout.decode.return_value" : "./scripts.py:3:1: E302 expected 2 blank lines, found 1",
                "stderr.decode.return_value" : "./scripts.py:3:1: E302 expected 2 blank lines, found 1",
                "returncode": 1
            }
        )
        mock_run.return_value = mock


        res = run_flake8()
        self.assertIsInstance(res, CheckResponse)
        self.assertFalse(res.result)
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
                "stdout.decode.return_value" : "./scripts.py:3:1: E302 expected 2 blank lines, found 1",
                "stderr.decode.return_value" : "",
                "returncode": 1
            }
        )
        mock_run.return_value = mock
        res = run_flake8()
        self.assertIsInstance(res, CheckResponse)
        self.assertFalse(res.result)
        self.assertTrue(len(res.info))

# class TestLintChecks(unittest.TestCase):

#     @patchfs
#     def test_has_flake8_return(self, fs):
#         """Test has_flake8() -> CheckResponse"""
#         res = has_flake8()
#         # assert return type
#         self.assertIsInstance(res, CheckResponse)
#         fs.create_file(".flake8")
#         res = has_flake8()
#         self.assertIsInstance(res, CheckResponse)
#         self.assertTrue(res.result)
    
#     @patchfs
#     def test_has_flake8(self, fs):
#         """Test has_flake8() gives correct .result"""
#         res = has_flake8()
#         # should give .result == False, when no .flake8 file
#         self.assertFalse(res.result)
#         fs.create_file(".flake8")
#         res = has_flake8()
#         # should give .result == True, when is .flake8 file
#         self.assertTrue(res.result)
    
#     @patchfs
#     def test_run_flake8_earlyexit(self, fs):
#         """Test run_flake8 no .flake8"""
#         res = run_flake8()
#         self.assertIsInstance(res, CheckResponse)
#         self.assertFalse(res.result)
#         self.assertEqual(res.info == "No flake 8 file")
    
#     @patchfs
#     def test_run_flake8_issues(self, fs):
#         """Test run flake 8 with lint issues"""
#         fs.create_file(".flake8")
#         fs.create_file("test.py", contents="""
# def f( x):
#     return x+1
#         """)
#         res = run_flake8()
#         self.assertIsInstance(res, CheckResponse)
#         self.assertFalse(res.result)
#         self.assertTrue(len(res.info))
    
#     @patchfs
#     def test_run_flake8_ok(self, fs):
#         """Test run flake 8 without lint issues"""
#         fs.create_file(".flake8")
#         fs.create_file("test.py", contents="""
# def f(x):
#     return x + 1
# """)
#         res = run_flake8()
#         self.assertIsInstance(res, CheckResponse)
#         self.assertTrue(res.result)
#         self.assertFalse(len(res.info))
    