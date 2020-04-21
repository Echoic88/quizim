from django import forms
from django.forms import modelformset_factory, formset_factory
from .models import Question, Quiz, PlayerAnswer

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["quiz_name"]
        

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question", "correct_answer"]
        widgets = {"DELETE":forms.HiddenInput}


CreateQuestionModelFormSet = modelformset_factory(
    Question,
    fields = ["question","correct_answer"],
    extra = 1,
    can_delete = True,
    widgets = {
        "question": forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter question here",
        }),
        "correct_answer": forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter answer here"
        })
    }
)


EditQuestionModelFormSet = modelformset_factory(
    Question,
    fields = ["question","correct_answer"],
    extra = 0,
    can_delete = True,
    widgets = {
        "question": forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter question here"
        }),
        "correct_answer": forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter answer here"
        }),
    }
)


PlayerAnswerModelFormSet = modelformset_factory(
    PlayerAnswer,
    fields=("question","player_answer",),
    extra=0,
    widgets={
        "question": forms.TextInput(attrs={
        "class": "form-control",
        "readonly":True
        }),
        "player_answer": forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter answer here"
        })
    }
)

