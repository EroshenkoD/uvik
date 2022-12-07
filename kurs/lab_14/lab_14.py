"""Testing
In this task you need to cover with tests all tasks from the lab1.

Use pytest.

Create fixtures, use parametrize, mocks and marks.

Note: try to cover the code with no less than 5 tests each task

python -m pytest kurs/lab_14/lab_14.py
coverage run -m pytest kurs/lab_14/lab_14.py
coverage report -m
"""
import pytest

from kurs.lab_14.from_lab_1_task_1 import check_palindrome_and_symmetrical
from kurs.lab_14.from_lab_1_task_2 import multiply_without_multiply
from kurs.lab_14.from_lab_1_task_3 import check_balanced


def test_palindrome_and_symmetrical(start_and_end_test_for_check_palindrome_and_symmetrical):
    assert check_palindrome_and_symmetrical(start_and_end_test_for_check_palindrome_and_symmetrical) == {
        'Symmetrical': True, 'Palindrome': True
    }, "Error symmetrical and palindrome"


def test_not_palindrome_and_not_symmetrical():
    assert check_palindrome_and_symmetrical('some word') == {
        'Symmetrical': False, 'Palindrome': False
    }, "Error not symmetrical and not palindrome"


@pytest.mark.parametrize("input_data, expected_result", [
    ("", {'Symmetrical': True, 'Palindrome': True}),
    ("khokho", {'Symmetrical': True, 'Palindrome': False}),
    ("Bobb", {'Symmetrical': False, 'Palindrome': False}),
    ("Never odd or even", {'Symmetrical': False, 'Palindrome': False}),
    ("Do geese see God?", {'Symmetrical': False, 'Palindrome': False}),
    ("abc", {'Symmetrical': False, 'Palindrome': False}),
    ("abab", {'Symmetrical': True, 'Palindrome': False}),
    ])
def test_diff_input_palindrome_and_symmetrical(input_data, expected_result):
    assert check_palindrome_and_symmetrical(input_data) == expected_result, "Error not symmetrical and palindrome"


@pytest.mark.parametrize("first_num, second_num, expected_result", [
    (2, 2, 4),
    (3, 6, 18),
    (5.6, 1, 5.6),
    (1.0, 5.0, 5),
    (25, 10, 250),
    ])
def test_multiply_without_multiply(first_num, second_num, expected_result):
    assert multiply_without_multiply(first_num, second_num) == expected_result, \
        "Error at multiply_without_multiply()"


@pytest.mark.xfail
def test_multiply_without_multiply_fail():
    assert multiply_without_multiply('a', 'b') == 'aXb', "Must error"


@pytest.mark.xfail
def test_multiply_without_multiply_without_fail():
    assert multiply_without_multiply(1, 1) == 1, "Must not error"


@pytest.mark.skip(reason="this functionality does not work")
def test_multiply_without_multiply_skip():
    assert multiply_without_multiply('a', 'b') == 'b**Xa**', "Must error"


@pytest.mark.parametrize("input_data, expected_result", [
    ('{[]{()}}', 'Balanced'),
    ('[{}{}(]', 'Unbalanced'),
    ('{][{()}}', 'Unbalanced'),
    ('{][{()}}$$', 'Unbalanced'),
    ('{][{(%)}}', 'Unbalanced'),
    ('{', 'Unbalanced'),
    ])
def test_check_balanced(input_data, expected_result, mocker):
    mocker.patch('from_lab_1_task_3.time.sleep', return_value=None)
    assert check_balanced(input_data) == expected_result, "Value should be mocked"

