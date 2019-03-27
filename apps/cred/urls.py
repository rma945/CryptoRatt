from django.urls import include, path, re_path
from django.conf import settings
from apps.cred.views import *

app_name = "cred"

urlpatterns = [    
    # projects
    path("project/", project_list, name="project_list"),
    path("project/page-<int:page>/", project_list, name="project_list"),
    path("project/add/", project_add, name="project_add"),
    path("project/edit/<int:project_id>/", project_edit, name="project_edit"),
    path("project/detail/<int:project_id>)/", project_detail, name="project_detail"),
    path("project/delete/<int:project_id>)/", project_delete, name="project_delete"),

    # credentials list
    path("list/", list, name="cred_list"),
    re_path(r"^list-by-(?P<cfilter>\w+)/(?P<value>[^/]*)/$", list, name="cred_list" ),
    re_path(r"^list-by-(?P<cfilter>\w+)/(?P<value>[^/]*)/sort-(?P<sortdir>ascending|descending)-by-(?P<sort>\w+)/$", list, name="cred_list"),
    re_path(r"^list-by-(?P<cfilter>\w+)/(?P<value>[^/]*)/sort-(?P<sortdir>ascending|descending)-by-(?P<sort>\w+)/page-(?P<page>\d+)/$", list, name="cred_list"),

    # Search dialog for mobile
    path("search/", search, name="search"),

    # Single cred views
    path("detail/<int:cred_id>/", detail, name="cred_detail"),
    path("detail/<int:cred_id>/fingerprint/", ssh_key_fingerprint, name="ssh_key_fingerprint"),
    path("detail/<int:cred_id>/download/", downloadattachment, name="download_attachment"),
    path("detail/<int:cred_id>/ssh_key/", downloadsshkey, name="download_sshkey"),
    path("edit/<int:cred_id>/", edit, name="cred_edit"),
    path("delete/<int:cred_id>/", delete, name="cred_delete"),
    path("add/", add, name="cred_add"),

    # Adding to the change queue
    path("addtoqueue/<int:cred_id>/", addtoqueue, name="cred_add_to_queue"),

    # Bulk views (for buttons on list page)
    path("addtoqueue/bulk/", bulkaddtoqueue, name="cred_bulk_add_to_queue"),
    path("delete/bulk/", bulkdelete, name="cred_bulk_delete"),
    path("undelete/bulk/", bulkundelete, name="cred_bulk_undelete"),
    path("addtag/bulk/", bulktagcred, name="cred_bulk_tag_cred"),

    # Tags
    path("tag/", tags, name="tags"),
    path("tag/add/", tagadd, name="tagadd"),
    path("tag/edit/<int:tag_id>/", tagedit, name="tag_edit"),
    path("tag/delete/<int:tag_id>/", tagdelete, name="tag_delete"),
]

if not settings.RATTIC_DISABLE_EXPORT:
    urlpatterns += [
        cred.views,
        # Export views
        path(r"^export.kdb$", download, name="download"),
        re_path(r"^export-by-(?P<cfilter>\w+)/(?P<value>[^/]*).kdb$", download),
    ]
