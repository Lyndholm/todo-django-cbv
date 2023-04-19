from django import forms


class TaskPositionForm(forms.Form):
    position = forms.CharField()
