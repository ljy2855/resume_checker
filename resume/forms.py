from django import forms
from django.forms import (
    inlineformset_factory,
    ModelChoiceField,
    ModelMultipleChoiceField,
)
from .models import Resume, QuestionAnswer, Technology, JobField


class ResumeForm(forms.ModelForm):
    technology_stack = forms.ModelMultipleChoiceField(
        queryset=Technology.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "select2-multiple"}),
        required=False,
    )

    class Meta:
        model = Resume
        fields = ["job_field", "technology_stack"]


class QuestionAnswerForm(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        fields = ["question", "answer"]


QuestionAnswerFormSet = inlineformset_factory(
    Resume, QuestionAnswer, form=QuestionAnswerForm, extra=1, can_delete=False
)
