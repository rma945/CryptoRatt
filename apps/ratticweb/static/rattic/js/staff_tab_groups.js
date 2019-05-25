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
