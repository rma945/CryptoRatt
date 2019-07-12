// TODO move to API
function deactivateUser() {
  var CSRF = getCSRFToken();
  var isActive = null

  if ($("#deactivate-user-button").data("isactive") == 'True') {
    isActive = false
  } else {
    isActive = true
  }

  var jsonData = {
    user_id: $("[name='user-id']").attr("content"),
    is_active: isActive,
  };

  $.ajax({
    url: '/staff/deactivate/user/',
    type: 'POST',
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-CSRFToken', CSRF);
    },
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(jsonData),
    dataType: 'json',
    success: function () {
      location.reload();
    }
  });
}

// TODO move to API
function deleteUser() {
  var CSRF = getCSRFToken();
  var user_id = $("[name='user-id']").attr("content");

  $.ajax({
    url: '/staff/delete/user/' + user_id + '/',
    type: 'POST',
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-CSRFToken', CSRF);
    },
    contentType: 'application/json; charset=utf-8',
    success: function () {
      window.location.href = '/staff/users';
    }
  });
}

$(document).ready(function () {
  // register deactivate user handler
  $("#deactivate-user-button").click(function (e) {
    deactivateUser()
  });

  // register delete user handler
  $("#delete-user-modal-button").click(function (e) {
    deleteUser()
  });

});

