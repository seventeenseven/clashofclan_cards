from django import forms


class ThreadForm(forms.Form):
    subject = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter the subject of your thread",
            })
        )


class CommentForm(forms.Form):
    comment = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your comment",
            })
        )
