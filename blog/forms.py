from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'teste mais-um-de-teste', 'placeholder': 'teste@gmail.com'}))
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your comment'}),
        }
