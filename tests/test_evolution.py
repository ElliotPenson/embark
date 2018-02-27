"""
test_evolution.py

@author Elliot Penson
"""

from embark.evolution import normalize


def test_normalize():
    assert normalize({}) == {}
    assert {"key": 1} == normalize({"key": 1})
    assert {"key1": 0.5, "key2": 0.5} == normalize({"key1": 0.5, "key2": 0.5})
    assert {"key1": 0.5, "key2": 0.5} == normalize({"key1": 1, "key2": 1})
