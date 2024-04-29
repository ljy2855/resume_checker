from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import ResumeForm, QuestionAnswerFormSet
from clients.openai_client import OpenAIClient
from clients.llama_client import OllamaClient
from .models import Resume, QuestionAnswer, Analysis
from django.shortcuts import render, get_object_or_404


def view_resume(request, resume_id):
    # get_object_or_404는 주어진 파라미터에 맞는 객체를 반환하거나, 객체가 없을 경우 404 에러를 발생시킵니다.
    resume = get_object_or_404(Resume, id=resume_id)
    # 연결된 질문과 답변을 가져옵니다.
    questions_answers = QuestionAnswer.objects.filter(resume=resume)

    return render(
        request,
        "resume/view_resume.html",
        {"resume": resume, "questions_answers": questions_answers},
    )


def submit_resume(request):
    if request.method == "POST":
        resume_form = ResumeForm(request.POST)
        if resume_form.is_valid():
            resume = resume_form.save()
            # POST 데이터와 함께 formset 인스턴스화
            formset = QuestionAnswerFormSet(request.POST, instance=resume)
            if formset.is_valid():
                formset.save()
                return redirect(f"/resume/{resume.id}")  # 성공적인 제출 후 리디렉트
        else:
            # 폼 검증 실패 시, 같은 formset 인스턴스를 유지
            formset = QuestionAnswerFormSet(request.POST)
    else:
        resume_form = ResumeForm()
        # GET 요청시 비어있는 formset 인스턴스화
        formset = QuestionAnswerFormSet()

    return render(
        request,
        "resume/submit_form.html",
        {"resume_form": resume_form, "formset": formset},
    )


def evaluate_resume(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
        questions = QuestionAnswer.objects.filter(resume=resume)
        # 이력서 정보를 문자열로 변환하는 로직 구현 필요
        resume_details = [
            f"Job Field: {resume.job_field.name}",
            f"Technology Stack: {', '.join([tech.name for tech in resume.technology_stack.all()])}",
        ]

        # 질문과 답변을 문자열 리스트에 추가
        for question in questions:
            resume_details.append(
                f"Question: {question.question} Answer: {question.answer}"
            )

        # 모든 정보를 하나의 문자열로 합치기
        resume_text = ". ".join(resume_details) + "."

        analysis, created = Analysis.objects.get_or_create(resume=resume)
        if created:

            client = OllamaClient()
            result = client.evaluate_text(resume_text)
            analysis.content = result
            analysis.save()
        else:
            result = analysis.content
        #         result = """**Resume Rating:** 2/5 (Needs improvement)

        # **Corrected Problems:**

        # 1. **Job-specific keywords**: The resume lacks relevant keywords from the job field and technology stack. Adding terms like "DevOps", "Django", "containerization", and "cloud" can help the resume pass through applicant tracking systems (ATS) and catch the eye of the hiring manager.
        # 2. **Clear structure**: The resume lacks a clear structure, making it hard to follow the developer's experience and skills. I'll provide a suggested outline:
        #         * Summary/Objective
        #         * Education
        #         * Technical Skills
        #         * Projects/Experience
        # 3. **Specific examples**: The answer to the question about describing efforts for the job is vague. I'll suggest rewriting it to include specific examples of how the developer applied their DevOps knowledge while studying.
        # 4. **Grammar and punctuation**: The resume contains errors in grammar, punctuation, and sentence structure. A review of the application's writing style will help improve its overall clarity.

        # **Rewritten Resume:**

        # **Summary/Objective**
        # Highly motivated DevOps enthusiast with a strong foundation in containerization using Docker and Django development experience. Proficient in leveraging cloud technologies to streamline workflows.

        # **Education**
        # Bachelor's Degree in Computer Science, XYZ University (20XX-20XX)

        # **Technical Skills**
        # * Programming languages: Python
        # * Frameworks: Django
        # * Containerization: Docker
        # * Cloud platforms: AWS, Azure
        # * Operating Systems: Linux, Windows

        # **Projects/Experience**

        # While studying DevOps at XYZ University, I successfully implemented a Dockerized environment for a team project. This allowed us to:
        #         + Rapidly deploy and scale applications using Docker containers.
        #         + Simplify the development process by leveraging containerization's isolation features.

        # To further enhance my skills, I worked on a personal project, building a Django-based web application and deploying it on AWS Elastic Beanstalk. This experience taught me the importance of:
        #         + Continuous Integration/Continuous Deployment (CI/CD) pipelines.
        #         + Monitoring application performance using CloudWatch metrics.

        # **Question Answer:**
        # During my studies, I made significant efforts to develop my DevOps skills by focusing on Docker containerization and Django development. One notable project was a team effort where we built a web application using Django and deployed it on AWS Elastic Beanstalk. By leveraging Docker containers, we streamlined our deployment process and ensured scalability. This experience not only honed my technical skills but also taught me the value of collaboration in DevOps.

        # **Rating after corrections:** 4/5 (Good)

        # Remember to proofread your resume multiple times for errors in grammar, punctuation, and sentence structure. Highlighting specific examples and emphasizing relevant technical skills can significantly improve the effectiveness of your application.

        #             """
        print(result)
        return JsonResponse({"result": result})
    except Resume.DoesNotExist:
        return JsonResponse({"error": "Resume not found"}, status=404)
