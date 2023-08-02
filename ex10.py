import pytest


def test_phrase_length():
    correct_phrase_length = 15
    phrase = input("Set a correct phrase: ")
    assert len(phrase) < correct_phrase_length, f"The phrase must be shorter than {correct_phrase_length} symbols"
