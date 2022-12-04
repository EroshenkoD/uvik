"""Check if the string is Symmetrical or Palindrome
Given a string. The task is to check if the string is symmetrical or palindrome. A string is said to be symmetrical
if both the halves of the string are the same and a string is said to be a palindrome string if one half of the string
is the reverse of the other half or if a string appears same when read forward or backward.

Input: khokho
Output:
The entered string is symmetrical
The entered string is not palindrome

Input: amaama
Output:
The entered string is symmetrical
The entered string is palindrome
"""


def check_palindrome_and_symmetrical(word: str) -> dict:
    res_dict = {'Symmetrical': False, 'Palindrome': False}
    word_len = len(word)
    if not word_len % 2:
        part_1 = word[: int(word_len/2)]
        part_2 = word[int(word_len/2):]
        if part_1 == part_2:
            res_dict['Symmetrical'] = True
        else:
            res_dict['Symmetrical'] = False
        if part_1 == part_2[::-1]:
            res_dict['Palindrome'] = True
        else:
            res_dict['Palindrome'] = False

    return res_dict


if __name__ == "__main__":
    print(check_palindrome_and_symmetrical('abab'))
