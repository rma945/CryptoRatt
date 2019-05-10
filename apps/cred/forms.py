from django.utils.translation import ugettext_lazy as _
from django.forms import Form, ModelForm, SelectMultiple, Select, PasswordInput, CharField, TextInput, ClearableFileInput, FileField, Textarea

from apps.cred.models import Project, Cred, Tag, Group

class ExportForm(Form):
    password = CharField(widget=PasswordInput(
        attrs={'class': 'btn-password-visibility'}
    ))


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

class ProjectForm(ModelForm):
    def __init__(self, requser, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['title'].label = _('Project title')
        self.fields['url'].label = _('Project URL')
        self.fields['description'].label = _('Project description')

        # Make the URL invalid message a bit more clear
        self.fields['url'].error_messages['invalid'] = _("Please enter a valid HTTP/HTTPS URL")

    class Meta:
        model = Project
        fields = '__all__'
        # These field are not user configurable
        widgets = {
            'title': TextInput(attrs={'autocomplete': ''}),
        }


class CredForm(ModelForm):
    
    # fake uploads field for attachments
    uploads = FileField(widget=ClearableFileInput(
        attrs={'multiple': True, 'class': 'custom-file-input'}), required=False)

    iconname = CharField(required=False)

    def __init__(self, requser, *args, **kwargs):
        super(CredForm, self).__init__(*args, **kwargs)

        # Limit the group options to groups that the user is in, for non staff users
        if not requser.is_staff:
            self.fields['group'].queryset = Group.objects.filter(user=requser)

        self.fields['group'].label = _('Owner Group')
        self.fields['groups'].label = _('Viewers Groups')
        self.fields['users'].label = _('Viewers Users')
        self.fields['uploads'].label = _('Upload files')

        # Make the URL invalid message a bit more clear
        self.fields['url'].error_messages['invalid'] = _("Please enter a valid HTTP/HTTPS URL")

    class Meta:
        model = Cred
        # These field are not user configurable
        exclude = Cred.APP_SET
        widgets = {
            # Use chosen for the tag field
            'project': Select(attrs={'class': 'custom-select'}),
            'title': TextInput(attrs={'class': 'form-control'}),
            'url': TextInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'autocomplete': 'off', 'class': 'form-control'}),
            'password': PasswordInput(render_value=True, attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'description': Textarea(attrs={'autocomplete': 'off'}),
            'tags':  SelectMultiple(attrs={'class': 'form-control single-select'}),
            'group': Select(attrs={'class': 'form-control single-select'}),
            'groups': SelectMultiple(attrs={'class': 'form-control single-select'}),
            'users': SelectMultiple(attrs={'class': 'form-control single-select'}),
        }
