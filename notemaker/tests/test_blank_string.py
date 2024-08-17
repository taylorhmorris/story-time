from django.test import TestCase

from notemaker.templatetags.notemaker.blank_string import blank_string

class BlankStringTest(TestCase):
    def test_simple_replace(self) -> None:
        phrase = 'word at start'
        blanked = '___ at start'
        self.assertEqual(blank_string(phrase, 'word'), blanked)

    def test_replace_middle(self) -> None:
        phrase = 'a word in middle'
        blanked = 'a ___ in middle'
        self.assertEqual(blank_string(phrase, 'word'), blanked)

    def test_replace_end(self) -> None:
        phrase = 'end word'
        blanked = 'end ___'
        self.assertEqual(blank_string(phrase, 'word'), blanked)

    def test_replace_multiple(self) -> None:
        phrase = 'word a word a word'
        blanked = '___ a ___ a ___'
        self.assertEqual(blank_string(phrase, 'word'), blanked)

    def test_replace_whole(self) -> None:
        phrase = 'word'
        blanked = '___'
        self.assertEqual(blank_string(phrase, 'word'), blanked)

    def test_replace_none(self) -> None:
        phrase = 'word'
        blanked = 'word'
        self.assertEqual(blank_string(phrase, 'not'), blanked)

    def test_replace_empty(self) -> None:
        phrase = ''
        blanked = ''
        self.assertEqual(blank_string(phrase, 'word'), blanked)

    def test_replace_cased_phrase(self) -> None:
        phrase = 'Word'
        blanked = '___'
        self.assertEqual(blank_string(phrase, 'word'), blanked)

    def test_replace_cased_word(self) -> None:
        phrase = 'word'
        blanked = '___'
        self.assertEqual(blank_string(phrase, 'Word'), blanked)