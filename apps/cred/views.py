from base64 import b64encode

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _

from apps.cred.models import Project, Cred, Attachment, CredAudit, Tag, CredChangeQ, CredentialIcon
from apps.cred.search import cred_search
from apps.cred.forms import ExportForm, ProjectForm, CredForm, TagForm

from django.contrib.auth.models import Group

def list(request, cfilter='special', value='all', sortdir='ascending', sort='title', page=1):
    # Setup basic stuff
    viewdict = {
        'credtitle': _('All passwords'),
        'alerts': [],
        'filter': str(cfilter).lower(),
        'value': str(value).lower(),
        'sort': str(sort).lower(),
        'sortdir': str(sortdir).lower(),
        'page': str(page).lower(),
        'groups': request.user.groups,

        # Default buttons
        'buttons': {
            'add': True,
            'delete': True,
            'changeq': True,
            'tagger': True,
            'export': False,
        }
    }

    # Get groups if required
    get_groups = request.GET.getlist('group')

    if len(get_groups) > 0:
        groups = Group.objects.filter(id__in=get_groups)
    else:
        groups = Group.objects.all()

    # Perform the search
    (search_object, cred_list) = cred_search(request.user, cfilter, value, sortdir, sort, groups)

    # Apply the filters
    if cfilter == 'tag':
        viewdict['credtitle'] = _('Passwords tagged with %(tagname)s') % {'tagname': search_object.name, }
        viewdict['buttons']['export'] = True

    elif cfilter == 'group':
        viewdict['credtitle'] = _('Passwords in group %(groupname)s') % {'groupname': search_object.name, }
        viewdict['buttons']['export'] = True

    elif cfilter == 'search':
        viewdict['credtitle'] = _('Passwords for search "%(searchstring)s"') % {'searchstring': search_object, }
        viewdict['buttons']['export'] = True

    elif cfilter == 'history':
        viewdict['credtitle'] = _('Versions of: "%(credtitle)s"') % {'credtitle': search_object.title, }
        viewdict['buttons']['add'] = False
        viewdict['buttons']['delete'] = False
        viewdict['buttons']['changeq'] = False
        viewdict['buttons']['tagger'] = False

    elif cfilter == 'changeadvice':
        alert = {}
        alert['message'] = _("That user is now disabled. Here is a list of passwords that they have viewed that have not since been changed. You probably want to add them all to the change queue.")
        alert['type'] = 'info'

        viewdict['credtitle'] = _('Changes required for "%(username)s"') % {'username': search_object.username}
        viewdict['buttons']['add'] = False
        viewdict['buttons']['delete'] = True
        viewdict['buttons']['changeq'] = True
        viewdict['buttons']['tagger'] = False
        viewdict['alerts'].append(alert)

    elif cfilter == 'special' and value == 'all':
        viewdict['buttons']['export'] = True

    elif cfilter == 'special' and value == 'trash':
        viewdict['credtitle'] = _('Passwords in the trash')
        viewdict['buttons']['add'] = False
        viewdict['buttons']['undelete'] = True
        viewdict['buttons']['changeq'] = False
        viewdict['buttons']['tagger'] = False
        viewdict['buttons']['export'] = True

    elif cfilter == 'special' and value == 'changeq':
        viewdict['credtitle'] = _('Passwords on the Change Queue')
        viewdict['buttons']['add'] = False
        viewdict['buttons']['delete'] = False
        viewdict['buttons']['changeq'] = False
        viewdict['buttons']['tagger'] = False

    else:
        raise Http404

    # Apply the sorting rules
    if sortdir == 'ascending':
        viewdict['revsortdir'] = 'descending'
    elif sortdir == 'descending':
        viewdict['revsortdir'] = 'ascending'
    else:
        raise Http404

    # Get the page
    paginator = Paginator(cred_list, request.user.profile.items_per_page)
    try:
        cred = paginator.page(page)
    except PageNotAnInteger:
        cred = paginator.page(1)
    except EmptyPage:
        cred = paginator.page(paginator.num_pages)

    # Get variables to give the template
    viewdict['credlist'] = cred

    # Create the form for exporting
    # viewdict['exportform'] = ExportForm()

    return render(request, 'cred_list.html', viewdict)

@login_required
def projects(request):
    paginator = Paginator(
        Project.objects.all().order_by('title'),
        request.user.profile.items_per_page
    )
    
    page = request.GET.get('page')
    projects = paginator.get_page(page)

    return render(request, 'project_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):

    project = get_object_or_404(Project, pk=project_id)

    paginator = Paginator(
        Cred.objects.filter(project=project,is_deleted=False, latest=None).order_by('title'),
        request.user.profile.items_per_page
    )
    
    page = request.GET.get('page')
    credentials = paginator.get_page(page)

    return render(request, 'project_detail.html', {'project': project, 'credentials': credentials})

@login_required
def project_add(request):
    # Restrict project add only to staff members
    if not request.user.is_staff:
        raise Http404

    if request.method == 'POST':
        form = ProjectForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("cred:projects"))
    else:
        form = ProjectForm(request.user)

    return render(request, 'project_edit.html', {'form': form, 'action':reverse("cred:project_add")})

@login_required
def project_edit(request, project_id):
    if not request.user.is_staff:
        raise Http404

    project = get_object_or_404(Project, pk=project_id)
    next = request.GET.get('next', None)

    if request.method == 'POST':
        form = ProjectForm(request.user, request.POST, request.FILES, instance=project)
        
        if form.is_valid():
            saved_form = form.save()

            if request.FILES.getlist('icon'):
                f = request.FILES.getlist('icon')[0]
                saved_form.icon = b64encode(f.file.read())
                saved_form.save()

        if next is None:
            return HttpResponseRedirect(reverse("cred:project_detail", args=(project.id,)))
        else:
            return HttpResponseRedirect(next)

    else:
        form = ProjectForm(request.user, instance=project)

    return render(
        request, 'project_edit.html',
        {
            'form': form,
            'action': reverse('cred:project_edit', args=(project.id,)),
            'next': next,
            'project': project,
        }
    )

@login_required
def project_delete(request, project_id):
    if not request.user.is_staff:
        raise Http404

    if request.method == 'POST':
        project = get_object_or_404(Project, pk=project_id)
        project.delete()

    return HttpResponseRedirect(reverse("cred:projects"))

# TODO: MOVE TO API
@login_required
def set_favorite_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        if project in request.user.profile.favourite_projects.all():
            request.user.profile.favourite_projects.remove(project)
        else:
            request.user.profile.favourite_projects.add(project)
        
    return HttpResponseRedirect(reverse('cred:projects'))


@login_required
def tags(request):
    tags = {}
    for t in Tag.objects.all():
        tags[t] = t.visible_count(request.user)
    return render(request, 'cred_tags.html', {'tags': tags})


@login_required
def detail(request, cred_id):
    cred = get_object_or_404(Cred, pk=cred_id)
    attachments = Attachment.objects.filter(credential=cred)

    # Check user has perms as owner or viewer
    if not cred.is_visible_by(request.user):
        raise Http404

    CredAudit(audittype=CredAudit.CREDVIEW, cred=cred, user=request.user).save()

    if request.user.is_staff:
        credlogs = cred.logs.all()[:5]
        morelink = reverse("staff:audit", args=('cred', cred.id))
    else:
        credlogs = None
        morelink = None

    # User is not in the password owner group, show a read-only UI
    if cred.group in request.user.groups.all():
        readonly = False
    elif request.user.is_staff:
        readonly = False
    else:
        readonly = True

    return render(request, 'cred_detail.html', {
        'cred': cred,
        'attachments': attachments,
        'credlogs': credlogs,
        'morelink': morelink,
        'readonly': readonly,
        'groups': request.user.groups,
    })


@login_required
def download_attachment(request, attachment_id):
    # get attachment
    attachment = get_object_or_404(Attachment, pk=attachment_id)

    # check that user has access to credentials 
    if not attachment.credential.is_visible_by(request.user):
        raise Http404

    # Write the audit that attachment was downloaded
    CredAudit(
        audittype=CredAudit.CREDATTACHVIEW,
        cred=attachment.credential,
        user=request.user
    ).save()

    # download attachment
    response = HttpResponse(attachment.content, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(attachment.filename)
    response['Content-Length'] = response.tell()

    return response

@login_required
def delete_attachment(request, attachment_id):
    # get attachment
    attachment = get_object_or_404(Attachment, pk=attachment_id)

    # check that user has access to credentials
    if not attachment.credential.is_visible_by(request.user):
        raise Http404

    # write the audit that attachment was deleted
    CredAudit(
        audittype=CredAudit.CREDATTACHDELETED,
        cred=attachment.credential,
        user=request.user
    ).save()
    
    # delete attachment
    attachment.delete()

    return HttpResponseRedirect(reverse('cred:cred_edit', args=(attachment.credential.id,)))


@login_required
def add(request):
    if request.method == 'POST':
        form = CredForm(request.user, request.POST)

        if form.is_valid():
            saved_form = form.save()
            
            # save attachments
            files = request.FILES.getlist('uploads')
            for f in files:
                if f.size <= settings.RATTIC_MAX_ATTACHMENT_SIZE:
                    a = Attachment(
                        credential=saved_form,
                        filename=f._name,
                        mime=f.content_type,
                        content=f.file.read(),
                    ).save()
            
            CredAudit(audittype=CredAudit.CREDADD, cred=form.instance, user=request.user).save()
            return HttpResponseRedirect(reverse('cred:cred_detail', args=(saved_form.id,)))
    else:
        form = CredForm(request.user)

    return render(
        request, 'cred_edit.html',
        {
            'form': form,
            'action':reverse('cred:cred_add'),
        }
    )

@login_required
def edit(request, cred_id):
    cred = get_object_or_404(Cred, pk=cred_id)

    if cred.latest is not None:
        raise Http404

    next = request.GET.get('next', None)

    # Check user has perms
    if not cred.is_visible_by(request.user):
        raise Http404

    if request.method == 'POST':
        form = CredForm(request.user, request.POST, instance=cred)

        # Password change possible only for owner group
        if form.is_valid():
            if cred.group in request.user.groups.all() or request.user.is_staff:
                
                # Assume metedata change
                chgtype = CredAudit.CREDMETACHANGE

                # Unless something thats not metadata changes
                for c in form.changed_data:
                    if c not in Cred.METADATA:
                        chgtype = CredAudit.CREDCHANGE

                # Clear pre-existing change queue items
                if chgtype == CredAudit.CREDCHANGE:
                    CredChangeQ.objects.filter(cred=cred).delete()

                # Create audit log
                CredAudit(audittype=chgtype, cred=cred, user=request.user).save()
                saved_form = form.save()

                # save attachments
                files = request.FILES.getlist('uploads')
                for f in files:
                    if f.size <= settings.RATTIC_MAX_ATTACHMENT_SIZE:
                        a = Attachment(
                            credential=saved_form,
                            filename=f._name,
                            mime=f.content_type,
                            content=f.file.read(),
                        ).save()

                # If we dont have anywhere to go, go to the details page
                if next is None:
                    return HttpResponseRedirect(reverse('cred:cred_detail', args=(cred.id,)))
                else:
                    return HttpResponseRedirect(next)
    else:
        form = CredForm(request.user, instance=cred)
        CredAudit(audittype=CredAudit.CREDPASSVIEW, cred=cred, user=request.user).save()

    # get all attachments
    attachments = Attachment.objects.filter(credential=cred)
    icons = CredentialIcon.objects.all().order_by('name')
    
    return render(
        request, 'cred_edit.html',
        {
            'form': form,
            'action': reverse('cred:cred_edit', args=(cred.id,)),
            'next': next,
            'cred': cred,
            'attachments': attachments,
            'icons': icons,
        }
    )


@login_required
def delete(request, cred_id):
    cred = get_object_or_404(Cred, pk=cred_id)

    if cred.latest is not None:
        raise Http404

    try:
        lastchange = CredAudit.objects.filter(
            cred=cred,
            audittype__in=[CredAudit.CREDCHANGE, CredAudit.CREDADD],
        ).latest().time
    except CredAudit.DoesNotExist:
        lastchange = _("Unknown (Logs deleted)")

    # Check user has perms (user must be member of the password owner group)
    if cred.is_owned_by(request.user) or request.user.is_staff:
        if request.method == 'POST':
            CredAudit(audittype=CredAudit.CREDDELETE, cred=cred, user=request.user).save()
            cred.delete()
            return HttpResponseRedirect(reverse('cred:cred_list'))
    else:
        raise Http404

    CredAudit(audittype=CredAudit.CREDVIEW, cred=cred, user=request.user).save()

    return render(
        request, 'cred_detail.html',
        {
            'cred': cred,
            'lastchange': lastchange,
            'action': reverse('cred:cred_edit', args=(cred_id,)),
        }
    )

# TODO: MOVE TO API
@login_required
def set_favorite_credential(request, cred_id):
    credential = get_object_or_404(Cred, pk=cred_id)
    
    if request.method == 'POST':
        if credential in request.user.profile.favourite_credentials.all():
            request.user.profile.favourite_credentials.remove(credential)
        else:
            request.user.profile.favourite_credentials.add(credential)

    return HttpResponseRedirect(reverse('cred:cred_list'))


@login_required
def cred_undelete(request, cred_id):
    if request.method == 'POST':
        if request.user.is_staff:
            cred = get_object_or_404(Cred, pk=cred_id)

            if cred.latest is not None:
                raise Http404

            cred.is_deleted = False
            cred.save()

            CredAudit(audittype=CredAudit.CREDUNDELETE,
                      cred=cred, user=request.user).save()
            CredAudit(audittype=CredAudit.CREDVIEW,
                      cred=cred, user=request.user).save()
        return HttpResponseRedirect(reverse('cred:cred_detail', args=(cred_id,)))

    return HttpResponseRedirect(reverse('cred:cred_list'))

@login_required
def tagadd(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cred:cred_list'))
    else:
        form = TagForm()

    return render(request, 'cred_tagedit.html', {'form': form})


@login_required
def tagedit(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cred:cred_list'))
    else:
        form = TagForm(instance=tag)

    return render(request, 'cred_tagedit.html', {'form': form})


@login_required
def tagdelete(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    if request.method == 'POST':
        tag.delete()
        return HttpResponseRedirect(reverse('tags'))
    return render(request, 'cred_tagdelete.html', {'t': tag})


@login_required
def addtoqueue(request, cred_id):
    cred = get_object_or_404(Cred, pk=cred_id)
    # Check user has perms (user must be member of the password owner group)
    if not cred.is_owned_by(request.user):
        raise Http404
    CredChangeQ.objects.add_to_changeq(cred)
    CredAudit(audittype=CredAudit.CREDSCHEDCHANGE, cred=cred, user=request.user).save()
    return HttpResponseRedirect(reverse('cred:cred_list', args=('special', 'changeq')))
