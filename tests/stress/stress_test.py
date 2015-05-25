import os


def test_stress():
    INPUT = os.environ['INPUT']
    assert INPUT is not '', 'Must specify INPUT directory.'
