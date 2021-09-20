import unittest

from grumpy_checks.lint import has_flake8
from grumpy_checks.checks import CheckResponse
from pyfakefs.fake_filesystem_unittest import patchfs


class TestLintChecks(unittest.TestCase):

    @patchfs
    def test_has_flake8_return(self, fs):
        """Test has_flake8() -> CheckResponse"""
        res = has_flake8()
        # assert return type
        self.assertIsInstance(res, CheckResponse)
        fs.create_file(".flake8")
        res = has_flake8()
        self.assertIsInstance(res, CheckResponse)
        self.assertTrue(res.result)
    
    @patchfs
    def test_has_flake8(self, fs):
        """Test has_flake8() gives correct .result"""
        res = has_flake8()
        # should give .result == False, when no .flake8 file
        self.assertFalse(res.result)
        fs.create_file(".flake8")
        res = has_flake8()
        # should give .result == True, when is .flake8 file
        self.assertTrue(res.result)
