from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django import forms
from apps.cred.models import CredAudit


class AuditFilterForm(forms.Form):
    hide = forms.MultipleChoiceField(
        choices=CredAudit.CREDAUDITCHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'selectize-multiple'}),
        initial=[],
    )


class UserForm(forms.ModelForm):
    # We want two password input boxes
    newpass = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'btn-password-visibility'}),
        required=False,
        max_length=32,
        min_length=8
    )
    confirmpass = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        max_length=32,
        min_length=8
    )

    # Define our model
    class Meta:
        model = User
        fields = ('username', 'email', 'is_active', 'is_staff', 'groups')
        widgets = {
            'groups': forms.SelectMultiple(attrs={'class': 'rattic-group-selector'}),
        }

    def clean(self):
        # Check the passwords given match
        cleaned_data = super(UserForm, self).clean()
        newpass = cleaned_data.get("newpass")
        confirmpass = cleaned_data.get("confirmpass")

        if newpass != confirmpass:
            msg = _('Passwords do not match')
            self._errors['confirmpass'] = self.error_class([msg])
            del cleaned_data['newpass']
            del cleaned_data['confirmpass']

        return cleaned_data


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
