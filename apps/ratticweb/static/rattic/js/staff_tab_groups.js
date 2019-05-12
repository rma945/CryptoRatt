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

function deleteGroup(button) {
  var CSRF = getCSRFToken();

  $.ajax({
    url: '/staff/delete/group/' + button.data('groupid') + '/',
    type: 'POST',
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-CSRFToken', CSRF);
    },
    contentType: 'application/json; charset=utf-8',
    success: function () {
      button.closest(".group-tab").remove();
      $("#delete-group-modal").modal("hide")
    }
  });
}


$(document).ready(function () {
  // initialize deactivate user button throught modal window
  $(".delete-group-button").click(function (e) {
    var dropdownButton = $(this)
    $("#delete-group-modal").modal("show")
    $("#delete-group-modal-button").click(function () {
      deleteGroup($(dropdownButton))
    });
  });

});
