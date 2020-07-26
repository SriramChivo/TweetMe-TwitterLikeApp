from django import forms
from .models import Tweet
from django.core.validators import RegexValidator


class TweetForm(forms.ModelForm):
    content = forms.CharField(label="Content", validators=[RegexValidator(r"^[!@#$%^&?{}|<>]*$", "Only Special Characters is Not Allowed", inverse_match=True)],
                              widget=forms.Textarea(attrs={"size": "60", "rows": "4", "cols": "60", "placeholder": "Say Something here!"}))

    class Meta:
        model = Tweet
        exclude = ["parent", "user", "likes", "is_liked", "is_reply"]

    def clean_content(self):
        value = self.cleaned_data.get("content")
        if(len(value) < 5):
            raise forms.ValidationError(
                "Sorry the content is too small to post")
        elif(value == "ABCDEFG"):
            raise forms.ValidationError("Too simple to post")
        return value  # if return is not given then it throws the field cannot be null
