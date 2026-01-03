ROMAN_NUMERAL_TO_VALUE = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000
}

ROMAN_NUMERAL_SUBTRACTION_PAIRS = {
    "IV": 4,
    "IX": 9,
    "XL": 40,
    "XC": 90,
    "CD": 400,
    "CM": 900
}



def convert_roman_numeral_to_int_first_pass(roman_numeral: str) -> int:
    value_so_far = 0

    while len(roman_numeral) > 0:
        if len(roman_numeral) >= 2:
            prefix = roman_numeral[0:2]
            if prefix in ROMAN_NUMERAL_SUBTRACTION_PAIRS:
                roman_numeral = roman_numeral[2:]
                value_so_far += ROMAN_NUMERAL_SUBTRACTION_PAIRS[prefix]
                continue
        if roman_numeral[0] not in ROMAN_NUMERAL_TO_VALUE:
            raise ValueError(f"{roman_numeral[0]} in {roman_numeral} is not a roman numeral")
        value_so_far += ROMAN_NUMERAL_TO_VALUE[roman_numeral[0]]
        roman_numeral = roman_numeral[1:]

    return value_so_far


def convert_roman_numeral_to_int(roman_numeral: str) -> int:
    current_value = 0
    prev_value = None
    for char in reversed(roman_numeral):
        if char not in ROMAN_NUMERAL_TO_VALUE:
            raise ValueError(f"{char} in {roman_numeral} is not a roman numeral")
        cur_index_numeral_value = ROMAN_NUMERAL_TO_VALUE[char]
        if prev_value is None or prev_value <= cur_index_numeral_value:
            current_value += cur_index_numeral_value
        else:
            current_value -= cur_index_numeral_value
        prev_value = cur_index_numeral_value
    return current_value



