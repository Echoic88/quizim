from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .formatter import format_answer
import uuid


# Create your models here.
class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_name = models.CharField(max_length=100, blank=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    created_date = models.DateTimeField(auto_now_add=True)
    instances_played = models.IntegerField(null=True, blank=True, default=0)


    def __str__(self):
        return f"{self.id}:{self.quiz_name}"


    def clean(self):
        if self.quiz_name == "" or self.quiz_name is None:
            raise ValidationError("Quiz name is required", code="name_required")
        if len(self.quiz_name) > 100:
            raise ValidationError("Quiz name is too long - 100 characters maximum", code="name_too_long")


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    question = models.CharField(max_length=100, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    correct_answer = models.CharField(max_length=100, blank=True)


    # Overide save method so that CreateQuestionFormset and EditQuestionFormset 
    # rows with no question are not saved these will not be valid entries. 
    # Implemented like this rather than making question field required
    # as there will always be at least one blank row in the formset for 
    # user convenience when creating or editing quizes and, as such, always
    # at least one Question instance submitted that is blank.
    def save(self, *args, **kwargs):
        if self.question != "" and self.correct_answer != "":
            super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.quiz.quiz_name}:{self.question}:{self.id}"


    def clean_question(self):
        if len(self.question) > 100:
            raise ValidationError("Max length is 100 characters", code="max_length_breached")


    def clean_correct_answer(self):
        if len(self.correct_answer) > 100:
            raise ValidationError("Max length is 100 characters", code="max_length_breached")


class PlayerAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="questions")
    player_answer = models.CharField(max_length=100)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    submitted_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submitted_date"]
        get_latest_by = ["submitted_date"]

    def __str__(self):
        return f"{self.id}:{self.question.question}:{self.player_answer}:{self.question.correct_answer}"


    def clean_player_answer(self):
        if len(self.player_answer) > 100:
            raise ValidationError("Max length is 100 characters", code="max_length_breached")    


@receiver(pre_save, sender=PlayerAnswer)
def create_user_profile(sender, instance, *args, **kwargs):
    # use format_answer function to standardise the player answer and correct answer
    # before comparison. If the comparison matches mark the player question as correct
    if format_answer(instance.player_answer) == format_answer(instance.question.correct_answer):
        instance.correct = True
        