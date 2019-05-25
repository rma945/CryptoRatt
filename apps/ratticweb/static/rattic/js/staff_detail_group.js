// TODO move to API
function deleteUser() {
  var CSRF = getCSRFToken();
  var group_id = $("[name='group-id']").attr("content");

  $.ajax({
    url: '/staff/delete/group/' + group_id + '/',
    type: 'POST',
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-CSRFToken', CSRF);
    },
    contentType: 'application/json; charset=utf-8',
    success: function () {
      window.location.href = '/staff/groups';
    }
  });
}

$(document).ready(function () {
  // register delete user handler
  $("#delete-group-modal-button").click(function (e) {
    deleteUser()
  });

});

