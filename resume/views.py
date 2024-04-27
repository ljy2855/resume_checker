from django.shortcuts import render, redirect
from .forms import ResumeForm, QuestionAnswerFormSet


def submit_resume(request):
    if request.method == "POST":
        resume_form = ResumeForm(request.POST)
        if resume_form.is_valid():
            resume = resume_form.save()
            formset = QuestionAnswerFormSet(request.POST, instance=resume)
            if formset.is_valid():
                formset.save()
                return redirect("/")  # 'success' URL을 설정해주세요.
    else:
        resume_form = ResumeForm()
        formset = QuestionAnswerFormSet()
    return render(
        request,
        "resume/submit_form.html",
        {"resume_form": resume_form, "formset": formset},
    )
