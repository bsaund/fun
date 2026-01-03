from roman_numeral.roman_to_integer import convert_roman_numeral_to_int
import pytest

@pytest.mark.parametrize(
    "roman_numeral, expected_int",
    [("I", 1),
     ("V", 5)]
)
def test_convert_single_numeral_to_int_finds_correct_value(roman_numeral, expected_int):
    assert convert_roman_numeral_to_int(roman_numeral) == expected_int


@pytest.mark.parametrize(
    "roman_numeral, expected_int",
    [("II", 2),
     ("III", 3),
     ("IV", 4),
     ("VI", 6),
     ("LVIII", 58),
     ("MCMXCIV", 1994)]
)
def test_convert_roman_numeral_to_int_finds_correct_value(roman_numeral, expected_int):
    assert convert_roman_numeral_to_int(roman_numeral) == expected_int

@pytest.mark.parametrize(
    "roman_numeral",
    [
        "A"
    ]
)
def test_convert_roman_numeral_to_int_raises_when_invalid_character(roman_numeral):
    with pytest.raises(ValueError):
        convert_roman_numeral_to_int(roman_numeral)