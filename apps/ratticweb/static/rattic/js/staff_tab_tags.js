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
    url: '/staff/delete/tag/' + button.data('tagid') + '/',
    type: 'POST',
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-CSRFToken', CSRF);
    },
    contentType: 'application/json; charset=utf-8',
    success: function () {
      button.closest(".tag-tab").remove();
      $("#delete-tag-modal").modal("hide")
    }
  });
}


$(document).ready(function () {
  // initialize deactivate user button throught modal window
  $(".delete-tag-button").click(function (e) {
    var dropdownButton = $(this)
    $("#delete-tag-modal").modal("show")
    $("#delete-tag-modal-button").click(function () {
      deleteGroup($(dropdownButton))
    });
  });

});
