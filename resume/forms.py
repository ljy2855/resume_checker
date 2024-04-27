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
        tech_objects = []
        for item in value:
            if item.isdigit():  # 입력값이 숫자인 경우, 기존 기술의 ID로 간주
                try:
                    tech = Technology.objects.get(id=int(item))
                    tech_objects.append(tech)
                except Technology.DoesNotExist:
                    raise forms.ValidationError(
                        "Technology with id {} does not exist.".format(item)
                    )
            else:  # 입력값이 숫자가 아닌 경우, 새로운 기술의 이름으로 간주
                tech, created = Technology.objects.get_or_create(name=item.strip())
                tech_objects.append(tech)
        return tech_objects


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
