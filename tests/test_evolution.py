"""
test_evolution.py

@author Elliot Penson
"""

from pytest import approx

from embark.evolution import normalize


def test_normalize():
    assert normalize({}) == {}
    assert normalize({"key": 1}) == {"key": 1}
    assert normalize({"key1": 0.5, "key2": 0.5}) == approx({"key1": 0.5, "key2": 0.5})
    assert normalize({"key1": 1, "key2": 1}) == approx({"key1": 0.5, "key2": 0.5})
    assert normalize({"key1": 1, "key2": 0.5}) == approx({"key1": 2/3, "key2": 1/3})
