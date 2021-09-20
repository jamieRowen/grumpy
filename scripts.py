import subprocess

def test():
    """Test
    
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover -s tests -v -p "*.py"`
    """
    subprocess.run(
        [
            'python', '-u', '-m', 'unittest',
            'discover', '-s', 'tests', '-v', '-p',
            '*.py'
        ]
    )