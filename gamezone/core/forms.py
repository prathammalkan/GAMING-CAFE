from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "score", "body"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "A quick headline for your review"}
            ),
            "score": forms.Select(
                choices=[(5, "5 - Masterpiece"), (4, "4 - Great"), (3, "3 - Good"), (2, "2 - Rough"), (1, "1 - Skip")]
            ),
            "body": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Tell other players what stood out, what hit hard, and what could be better.",
                }
            ),
        }
