from django import forms


class TodoForm(forms.Form):
    title = forms.CharField(max_length=200, label='title')
    description = forms.CharField(widget=forms.Textarea, required=False, label='description')
    due_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='due_date')
    priority = forms.ChoiceField(choices=[
        ('low', 'Düşük'),
        ('medium', 'Orta'),
        ('high', 'Yüksek'),
    ], initial='medium', label='priority')