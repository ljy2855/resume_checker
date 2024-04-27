from django import forms
from django.forms import ModelForm
from django.forms import (
    inlineformset_factory,
    ModelChoiceField,
    ModelMultipleChoiceField,
)
from .models import Resume, QuestionAnswer, Technology, JobField

from .models import Technology


class TechnologyField(forms.ModelMultipleChoiceField):
    def clean(self, value):
        # 입력된 모든 값에 대해 처리
        def get_or_create_tech(name):
            tech, _ = Technology.objects.get_or_create(name=name.strip())
            return tech

        # 입력된 기술을 검사하고, 없으면 생성
        return [get_or_create_tech(name) for name in value]


class ResumeForm(ModelForm):
    technology_stack = TechnologyField(
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
