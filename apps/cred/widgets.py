from django.forms.widgets import ClearableFileInput, HiddenInput
from django.utils.translation import ugettext_lazy as _
from apps.cred.templatetags.credicons import cred_icon
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

class CredIconChooser(HiddenInput):
    button_text = _('Choose')

    def render(self, name, value, attrs=None, renderer=None):
        logo = cred_icon(value, tagid='logodisplay')
        input = super(CredIconChooser, self).render(name, value, attrs, renderer=None)
        button = '<a href="#logoModal" role="button" class="btn" id="choosebutton" data-toggle="modal">%s</a>' % force_text(self.button_text)

        return mark_safe(logo + ' ' + button + input)
