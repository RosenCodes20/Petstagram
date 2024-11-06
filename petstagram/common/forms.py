from django.forms import ModelForm, TextInput, Textarea, Form, CharField

from petstagram.common.models import Comment


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ["comment_text"]

        widgets = {
            "comment_text": Textarea(attrs={"placeholder": "Add comment..."})
        }


class SearchBarForm(Form):

    pet_name = CharField(
        widget=TextInput(
            attrs={
                "placeholder": "Search by pet name..."
            }
        ),
        required=False
    )