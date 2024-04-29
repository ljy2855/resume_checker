from django.db import models


class JobField(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Resume(models.Model):
    job_field = models.ForeignKey(
        JobField, on_delete=models.CASCADE, verbose_name="Job Field"
    )
    technology_stack = models.ManyToManyField(
        Technology, verbose_name="Technology Stack"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Resume {self.id} created at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
        )


class Analysis(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    content = models.TextField(blank=True)


class QuestionAnswer(models.Model):
    resume = models.ForeignKey(
        Resume, related_name="questions", on_delete=models.CASCADE
    )
    question = models.TextField(blank=True, verbose_name="Question")
    answer = models.TextField(blank=True, verbose_name="Answer")

    def __str__(self):
        return f"Question for Resume {self.resume.id}"
