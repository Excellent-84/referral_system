import re

from django import forms


class BaseForm(forms.Form):

    def add_placeholder(self, field_name, placeholder):
        field = self.fields.get(field_name)
        if field:
            field.widget.attrs.update({'placeholder': placeholder})


class PhoneForm(BaseForm):
    phone = forms.CharField(
        max_length=12,
        required=True,
        label='Номер телефона',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholder('phone', 'Например +79001234567')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone_pattern = re.compile(r"^\+7\d{10}$")
        if not phone_pattern.match(phone):
            raise forms.ValidationError(
                'Номер телефона в формате +7XXXXXXXXXX'
            )
        return phone


class CodeForm(BaseForm):
    code = forms.CharField(
        max_length=4,
        required=True,
        label='Код подтверждения',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholder('code', 'Введите код из СМС')


class InviteCodeForm(BaseForm):
    invite_code = forms.CharField(
        max_length=12,
        required=True,
        label='Инвайт-код',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholder('invite_code', 'Введите инвайт-код')
