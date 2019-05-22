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
    success: function () {
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