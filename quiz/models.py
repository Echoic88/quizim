from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .formatter import format_answer
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


# Create your models here.
class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_name = models.CharField(max_length=100, blank=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    created_date = models.DateTimeField(auto_now_add=True)
    instances_played = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        ordering = ["-created_date"]


    def __str__(self):
        return f"{self.quiz_name}:{self.creator.username}"


    def clean(self):
        if self.quiz_name == "" or self.quiz_name is None:
            raise ValidationError("Quiz name is required", code="name_required")
        if len(self.quiz_name) > 100:
            raise ValidationError("Quiz name is too long - 100 characters maximum", code="name_too_long")
    

class PlayedQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    played_date = models.DateTimeField(auto_now=True)

    def score(self):
        answers = PlayerAnswer.objects.filter(player=self.player).filter(quiz=self.quiz)
        score = round((answers.filter(correct=True).count()/answers.count()),2) 
        return score
    
    def __str__(self):
        return f"{self.quiz}:{self.player}.{self.played_date}"


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
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
        return f"{self.quiz.quiz_name}:{self.quiz.creator.username}:{self.question}"


    def clean_question(self):
        if len(self.question) > 100:
            raise ValidationError("Max length is 100 characters", code="max_length_breached")


    def clean_correct_answer(self):
        if len(self.correct_answer) > 100:
            raise ValidationError("Max length is 100 characters", code="max_length_breached")


class PlayerAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="playeranswers")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    player_answer = models.CharField(max_length=100)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.quiz.quiz_name}:{self.question.question}:{self.player_answer}:{self.question.correct_answer}:{self.player}"

    def clean_player_answer(self):
        if len(self.player_answer) > 100:
            raise ValidationError("Max length is 100 characters", code="max_length_breached")    


class PaidQuiz(models.Model):
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        #set min value to 0.50 - Stripe minimum that can be charged
        validators=[MinValueValidator(0.5)])

    def __str__(self):
        return f"{self.quiz.quiz_name}:{self.price}"


class Order(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    purchase_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quiz.quiz_name}:{self.customer.first_name} {self.customer.last_name}: {self.purchase_date}"

    def played(self):
        played_by_user = PlayedQuiz.objects.filter(player=self.customer)
        for played_quiz in played_by_user:
            if self.quiz == played_quiz.quiz:
                return True
            else:
                return False


@receiver(pre_save, sender=PlayerAnswer)
def compare_answers(sender, instance, *args, **kwargs):
    # use format_answer function to standardise the player answer and correct answer
    # before comparison. If the comparison matches mark the player question as correct
    if format_answer(instance.player_answer) == format_answer(instance.question.correct_answer):
        instance.correct = True


@receiver(post_save, sender=Quiz)
def paid_for_quiz(sender, instance, created, **kwargs):
    """
    when admin creates a quiz this will be a prdouct in the store.
    Extend the base Quiz model to include a price.
    admin can set the price to zero to make the product a free
    purchase.
    """
    admin = User.objects.get(username="admin")
    if instance.creator == admin:
        if created:
            PaidQuiz.objects.create(quiz=instance)
