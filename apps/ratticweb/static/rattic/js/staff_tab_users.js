// TODO move to API - VERY BAAD 
function deactivateUser(button) {
  var CSRF = getCSRFToken();
  var isActive = null
  var buttonText = 'unset'

  if (button.data('isactive') === 'True') {
    isActive = false
    buttonText = 'Activate'
  } else {
    isActive = true
    buttonText = 'Deactivate'
  }

  var jsonData = {
    user_id: button.data('userid'),
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
      button.closest(".users-tab").toggleClass("bg-light");
      button.data('isactive', isActive)
      button.text(buttonText);
    }
  });
}

function deleteUser(button) {
  var CSRF = getCSRFToken();

  $.ajax({
    url: '/staff/delete/user/' + button.data('userid') + '/',
    type: 'POST',
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-CSRFToken', CSRF);
    },
    contentType: 'application/json; charset=utf-8',
    success: function () {
      button.closest(".users-tab").remove();
      $("#delete-user-modal").modal("hide")
    }
  });
}


$(document).ready(function () {
  // add selection highlight throught JS for a correct colors in all boostrap themes
  $(".users-tab").hover(function () {
    $(this).toggleClass("bg-light");
  }, function () {
      $(this).toggleClass("bg-light");
  });

  // initialize deactivate user buttons
  $(".deactivate-user-button").click(function () {
    deactivateUser($(this))
  });

  // initialize deactivate user button throught modal window
  $(".delete-user-button").click(function () {
    var dropdownButton = $(this)
    $("#delete-user-modal").modal("show")
    $("#delete-user-modal-button").click(function () {
      deleteUser($(dropdownButton))
    });
  });

});
