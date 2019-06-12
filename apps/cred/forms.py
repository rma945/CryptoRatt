from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm, SelectMultiple, Select, PasswordInput, CharField, TextInput, ClearableFileInput, FileField, Textarea, ModelMultipleChoiceField

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
    icon = FileField(widget=ClearableFileInput(
        attrs={'multiple': False, 'style': 'display: none;', 'accept': 'image/*' }), required=False)

    credentials = ModelMultipleChoiceField(
        queryset=Cred.objects.filter(is_deleted=False, latest=None),
        widget=SelectMultiple(attrs={'class': 'form-control single-select'}),
    )

    def __init__(self, requser, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
               
        self.fields['title'].label = _('Project title')
        self.fields['url'].label = _('Project URL')
        self.fields['description'].label = _('Project description')
        self.fields['credentials'].required = False

        if self.instance:
            self.fields["credentials"].initial = (
                self.instance.cred_set.all().values_list('id', flat=True)
        )

        self.fields['url'].error_messages['invalid'] = _("Please enter a valid HTTP/HTTPS URL")

    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'url': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        project = self.instance
        credentials = self.cleaned_data['credentials']

        if project.cred_set.all():
            project.cred_set.clear()
        
        # TODO: fix project creating
        if Project.objects.filter(title = self.cleaned_data['title']).exists():
            for c in credentials:
                project.cred_set.add(c)
        
        if Project.objects.filter(title = self.cleaned_data['title']).exists():
            raise ValidationError({'title': ['Project with same name already exists',]})

        return self.cleaned_data


class CredForm(ModelForm):
    
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
        
        # requre owners group
        self.fields['group'].required = True

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
