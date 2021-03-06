from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, Form, MultipleChoiceField, ModelMultipleChoiceField, SelectMultiple, CharField, PasswordInput, CheckboxInput, TextInput, FileField, ClearableFileInput

from apps.cred.models import CredAudit

class EditUserForm(ModelForm):
    icon = FileField(widget=ClearableFileInput(
        attrs={'multiple': False, 'style': 'display: none;', 'accept': 'image/*' }), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_active', 'groups', 'icon']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'is_staff': CheckboxInput(attrs={'class': 'custom-control-input'}),
            'is_active': CheckboxInput(attrs={'class': 'custom-control-input'}),
            'groups': SelectMultiple(attrs={'class': 'form-control single-select'}),
        }
        
    def clean(self):
        addvalidator = True

class AuditFilterForm(Form):
    hide = MultipleChoiceField(
      choices=CredAudit.CREDAUDITCHOICES,
      widget=SelectMultiple(attrs={'class': 'selectize-multiple'}),
      initial=[],
    )

class UserForm(ModelForm):
    # We want two password input boxes
    newpass = CharField(
        widget=PasswordInput(attrs={'class': 'btn-password-visibility'}),
        required=False,
        max_length=32,
        min_length=8
    )
    confirmpass = CharField(
        widget=PasswordInput,
        required=False,
        max_length=32,
        min_length=8
    )

    # Define our model
    class Meta:
        model = User
        fields = ('username', 'email', 'is_active', 'is_staff', 'groups')
        widgets = {
            'groups': SelectMultiple(attrs={'class': 'rattic-group-selector'}),
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


class GroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields["users"].initial = (
                self.instance.user_set.all().values_list(
                    'id', flat=True
                )
            )

    users = ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=SelectMultiple(attrs={'class': 'form-control single-select'}),
    )

    class Meta:
        model = Group
        fields = ('name', 'users',)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
        }
        
    def clean(self):
        group = self.instance
        users = self.cleaned_data['users']

        # remove old users
        if group.user_set.all():
            group.user_set.clear()

        # add new users
        for u in users:
            group.user_set.add(u)

        return self.cleaned_data
