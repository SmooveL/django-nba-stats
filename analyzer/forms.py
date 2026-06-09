from django import forms

class PlayerSearchForm(forms.Form):
    query = forms.CharField(
        label='Поиск игрока',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя или фамилию...'})
    )

    def clean_query(self):
        data = self.cleaned_data.get('query')
        if data:
            data = data.strip()
            if len(data) < 2:
                raise forms.ValidationError("Минимальная длина запроса — 2 символа.")
        return data