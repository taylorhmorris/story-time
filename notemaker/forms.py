from django import forms

from notemaker.models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            "word",
            "ipa",
            "grammar",
            "definition",
            "example",
            "expression",
            "expression_meaning",
            "image",
            "owner"
        ]
