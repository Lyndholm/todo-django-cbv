from django import forms

from .models import Task


class TaskPositionForm(forms.Form):
    position = forms.CharField()


class DateInput(forms.DateInput):
    input_type = 'date'
    attrs = {
        'class': 'form-control',
        'placeholder': 'Select a date',
        'type': 'date',
    }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'deadline',
            'complete',
        )
        widgets = {
            'deadline': DateInput,
        }
