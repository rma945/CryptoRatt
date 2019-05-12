function getCSRFToken() {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, 'csrftoken'.length + 1) === ('csrftoken' + '=')) {
        cookieValue = decodeURIComponent(cookie.substring('csrftoken'.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

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

