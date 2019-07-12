function deleteProject() {
  var CSRF = getCSRFToken();
  var project_id = $("[name='project-id']").attr("content");

  $.ajax({
    url: '/cred/project/delete/' + project_id + '/',
    type: 'POST',
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-CSRFToken', CSRF);
    },
    contentType: 'application/json; charset=utf-8',
    success: function () {
      window.location.href = '/cred/project';
    }
  });
}

function setFavorite() {
  var CSRF = getCSRFToken();
  var project_id = $("[name='project-id']").attr("content");

  $.ajax({
    url: '/cred/project/favorite/' + project_id + '/',
    type: 'POST',
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-CSRFToken', CSRF);
    },
    contentType: 'application/json; charset=utf-8',
    success: function (data) {
      if (data.action == 'added') {
        $("#projects-favorites-list").append(
          "<li data-id='" + project_id + "'>\
          <a href='" + window.location.href + "'>\
          <i class='fas fa-minus'>\
          </i> " + $('#project-title').text() + "</a>\
          </li>"
        );
      } else {
        $("#projects-favorites-list").find("[data-id='" + project_id + "']").remove()
      }
      $("#set-farovire-button").toggleClass("btn-warning")
    }
  });
}


$(document).ready(function () {
  // register delete project button
  $("#delete-project-button").click(function () {
    $("#delete-project-modal").modal("show")
    $("#delete-project-modal-button").click(function () {
      deleteProject();
    });
  });

  // register set favorite project button
  $("#set-farovire-button").click(function () {
    setFavorite();
  });
});