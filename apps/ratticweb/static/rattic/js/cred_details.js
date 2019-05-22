// variables
var credentialPassword = 'all-passwords-are-encrypted';

// get credential ID from page metadata
function getCredentialID() {
  return $("[name='cred-id']").attr("content");
}

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

// get credential password from API and cache it in local JS
function getCredentialPassword() {
  if (credentialPassword == 'all-passwords-are-encrypted') {
    var credentialID = getCredentialID();

    resp = $.parseJSON($.ajax({
      url: '/api/v1/cred/' + credentialID,
      type: 'GET',
      contentType: 'application/json',
      data: undefined,
      async: false
    }).responseText);

    if ('password' in resp) {
      credentialPassword = resp['password']
    }
  }

  return credentialPassword
}

// cred_details.html functions
function showPasswordToggle() {
  var credentialPassword = getCredentialPassword();

  if ($('#password-field').attr('type') == 'password' ) {
    $('#password-field').attr('type', 'text');
    $('#password-field').attr('value', credentialPassword);
  } else {
    $('#password-field').attr('type', 'password');
    $('#password-field').attr('value', 'credentialPassword');
    $('#password-field').attr('value', 'all-passwords-are-encrypted');
  }
};

// copy password throught fake unvisible button
function copyPassword() {
  var credentialPassword = getCredentialPassword();
  var passwordFieldState = $('#password-field').attr('type')
  
  // change field type for clipboard.js plugin
  if (passwordFieldState == 'password') {
    $('#password-field').attr('type', 'text');
    $('#password-field').attr('readonly', 'false');
    $('#password-field').attr('value', credentialPassword);
  }
  // initialize copy password throught fake button
  $('#copy-password-button-hidden').trigger("click");
  
  // revert changes at field type
  if (passwordFieldState == 'password') {
    $('#password-field').attr('readonly', 'true');
    $('#password-field').attr('type', 'password');
    $('#password-field').attr('value', 'all-passwords-are-encrypted');
  }
};

// undelete credentials modal window 
function undeleteCredentialModalToggle() {
  var credentialID = getCredentialID();
  var url = '/cred/undelete/' + credentialID + '/'
  var modalWindow = $('#delete-modal');

  modalWindow.find('.modal-body').text('This credential has been deleted and is in the trash can, click on the undelete button if you want to restore it');
  modalWindow.find('.modal-title').text('Undelete credential');
  modalWindow.find('.btn-danger').text('Undelete');
  $("#delete-modal-form").attr('action', url)

  modalWindow.modal('show')
}

// delete credential modal window toggle 
function deleteCredentialModalToggle() {
  var credentialID = getCredentialID();
  var url = '/cred/delete/' + credentialID + '/'
  var modalWindow = $('#delete-modal');

  modalWindow.find('.modal-body').text('You are about to delete this password. A staff member will be required if you want to undelete it.');
  modalWindow.find('.modal-title').text('Delete credential');
  modalWindow.find('.btn-danger').text('Delete');
  $("#delete-modal-form").attr('action', url)
  
  modalWindow.modal('show')
}

function setFavorite() {
  var CSRF = getCSRFToken();
  var cred_id = $("[name='cred-id']").attr("content");

  $.ajax({
    url: '/cred/favorite/' + cred_id + '/',
    type: 'POST',
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-CSRFToken', CSRF);
    },
    contentType: 'application/json; charset=utf-8',
    success: function () {
      $("#set-favorite-button").toggleClass("btn-warning")
    }
  });
}

$(document).ready(function () {
  // initialize js clipboards and add default unselect actions on it
  var usernameClipboard = new ClipboardJS('#copy-username-button');
  var passwordClipboard = new ClipboardJS('#copy-password-button-hidden');

  usernameClipboard.on('success', function(e) {
    e.clearSelection();
  });

  passwordClipboard.on('success', function (e) {
    e.clearSelection();
  });

  // register - show password toggle button
  $('#show-password-field-button').click(function () {
    showPasswordToggle();
  });

  // register - copy password button
  $('#copy-password-button').click(function () {
    copyPassword();
  });

  // register - undelete button
  $('#undelete-credential-button').click(function () {
    undeleteCredentialModalToggle()
  });

  // register - delete button
  $('#delete-credential-button').click(function () {
    deleteCredentialModalToggle()
  });
  
  // register - set favorite button
  $('#set-favorite-button').click(function () {
    setFavorite();
  });
});

