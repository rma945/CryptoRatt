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
  attr_admin_group = confget('saml', 'admin_group', 'Administrators').split(',')

  current_user = User.objects.get(username=saml_data[attr_username][0])

  # create new group and add user on it
  for group_name in saml_data[attr_groups]:
    group, is_created = Group.objects.get_or_create(name=group_name)

    # add user to new groups
    if is_created:
      # add user to already created group
      current_user.groups.add(group)
    else:
      # if group not creared - create it and then add user
      if not current_user.groups.filter(name=group_name).exists():
        current_user.groups.add(group)

    # remove user from old groups
    for g in current_user.groups.all():
      if g.name not in saml_data[attr_groups]:
        g.user_set.remove(current_user)

  # add or remove user from staff role
  for group in current_user.groups.all():
    if group.name in attr_admin_group:
      current_user.is_staff = True
      break
    else:
      current_user.is_staff = False

  # save user
  current_user.save()
  
  return
