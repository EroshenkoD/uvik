import pytest


@pytest.fixture()
def start_and_end_test_for_check_palindrome_and_symmetrical():
    print('start')
    yield 'amaama'
    print('end')
