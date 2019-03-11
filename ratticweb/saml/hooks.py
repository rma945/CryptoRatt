from ConfigParser import RawConfigParser, NoOptionError
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.models import User, Group

config = RawConfigParser()
config.read(['conf/local.cfg', '/etc/ratticweb.cfg'])

User = get_user_model()

def confget(section, var, default):
  try:
    return config.get(section, var)
  except NoOptionError:
    return default


def sync_user(saml_data):
  # load saml configuration
  attr_username = confget('saml', 'attribute_username', 'username')
  attr_groups = confget('saml', 'attribute_groups', 'usergroups')
  attr_admin_group = confget('saml', 'admin_group', 'devops')

  current_user = User.objects.get(username=saml_data[attr_username][0])

   # create new group and add user on it
  for group_name in saml_data[attr_groups]:
    group, is_created = Group.objects.get_or_create(name=group_name)

    # add user to new groups
    if is_created:
      current_user.groups.add(group)
    else:
      if not current_user.groups.filter(name=group_name).exists():
        current_user.groups.add(group)

    # remove user from old groups
    for group in current_user.groups.all():
      if group.name not in saml_data[attr_groups]:
        group.user_set.remove(current_user)

    # add or remove user from staff role
    if attr_admin_group in saml_data[attr_groups]:
      current_user.is_staff = True
    else:
      current_user.is_staff = False

    # save user
    current_user.save()

  return
