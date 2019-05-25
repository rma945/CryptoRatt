
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
