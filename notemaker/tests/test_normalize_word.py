from django.test import TestCase

from notemaker.utils.normalize_word import normalize_word

# Create your tests here.
class NormalizeWordTest(TestCase):
    def test_lowercase_unchanged(self) -> None:
        word = 'manger'
        self.assertEqual(normalize_word(word), word)

    def test_uppercase_changed(self) -> None:
        word = 'MaNger'
        self.assertEqual(normalize_word(word), 'manger')

    def test_numbers(self) -> None:
        word = '12411'
        self.assertEqual(normalize_word(word), '')

    def test_alphanumeric(self) -> None:
        word = 'aa12b411c'
        self.assertEqual(normalize_word(word), 'aabc')

    def test_special_chars(self) -> None:
        word = 'abCd%&^*$#@(!)((())+=-_,./;l;\'\'[]{e}{}f'
        self.assertEqual(normalize_word(word), 'abcdlef')

    def test_accented_chars(self) -> None:
        word = 'mangé et èαá'
        self.assertEqual(normalize_word(word), 'mangéetèαá')

    def test_empty(self) -> None:
        word = ''
        self.assertEqual(normalize_word(word), '')

    def test_None(self) -> None:
        word = None
        self.assertEqual(normalize_word(word), '')
