from django import forms

class SolutionForm(forms.Form):
    solution = forms.ImageField(label='Upload your solution')
