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
            "image"
        ]
    # word = forms.CharField(label="Word")
    # ipa = forms.CharField(label="ipa")
    # grammar = forms.CharField(label="grammar", max_length=50)
    # definition = forms.CharField(label="definition", max_length=200)
    # example = forms.CharField(label="example", max_length=200)
    # expression = forms.CharField(label="expression", max_length=200)
    # expression_meaning = forms.CharField(label="expression meaning", max_length=200)
    # image = forms.CharField(label="image")
