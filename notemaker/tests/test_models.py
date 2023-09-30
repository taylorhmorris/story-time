from django.test import TestCase

from notemaker.models import Note

# Create your tests here.
class NoteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Note.objects.create(word='Blank Word')

    def setUp(self) -> None:
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_word_label(self) -> None:
        note = Note.objects.get(id=1)
        field_label = note._meta.get_field('word').verbose_name
        self.assertEqual(field_label, 'word')

