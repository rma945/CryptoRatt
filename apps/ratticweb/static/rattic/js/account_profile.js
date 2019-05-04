// TODO: MOVE TO API
// Post data to django view for create new API key
function createAPIKey() {
  var formData = new FormData();
  var apiKeyName =  $("#new-apikey-input").val()
  var csrfToken = $("[name='csrfmiddlewaretoken']").val()

  if (apiKeyName.length > 0 ) {
    formData.append('name', apiKeyName);
    formData.append('csrfmiddlewaretoken', csrfToken)

    $.ajax({
      url: 'newapikey/',
      data: formData,
      processData: false,
      contentType: false,
      type: 'POST',
    });
  }
  
  // TODO: MOVE TO API
  location.reload();
}

function deleteAPIKey(button) {
  var formData = new FormData();
  var apiKeyId = button.data('keyid')
  var csrfToken = $("[name='csrfmiddlewaretoken']").val();
  
  if (apiKeyId > 0) {
    formData.append('csrfmiddlewaretoken', csrfToken)

    $.ajax({
      url: 'deleteapikey/' + apiKeyId + '/',
      data: formData,
      processData: false,
      contentType: false,
      type: 'POST',
    });
    
    // hide modal
    $("#delete-apikey-modal").modal('hide');
    
    // remove parent row with api key
    $(button).parents("tr").remove(); 
  }
}

function deleteSession(button) {
  var formData = new FormData();
  var sessionId = button.data('sesionid')
  var csrfToken = $("[name='csrfmiddlewaretoken']").val();
  
  if (sessionId.length > 0) {
    formData.append('csrfmiddlewaretoken', csrfToken)

    $.ajax({
      url: 'killsession/' + sessionId + '/',
      data: formData,
      processData: false,
      contentType: false,
      type: 'POST',
    });

    // hide modal
    $("#delete-session-modal").modal('hide');

    // remove parent row with api key
    $(button).parents("tr").remove();
  }
}

$(document).ready(function () {
  // initialize users selectize
  $('#id_favourite_tags').selectize({
    persist: false,
    plugins: ['remove_button'],
  });

  // initialize submit form
  $("#profile-submit-button").click(function () {
    $("#profile-submit-form").submit();
  });

  // initialize apikey create button
  $("#create-apikey-button").click(function () {
    createAPIKey();
  });
  
  // TODO: MOVE TO API
  // // initialize apikey delete buttons
  $(".delete-apikey-button").click(function () {
    var button = $(this)
    
    $("#delete-apikey-modal").modal('show');
    
    // set delete function with element ID on modal button
    $("#delete-apikey-button").click(function () {
      deleteAPIKey(button);
    });
  });

  // TODO: MOVE TO API
  // // initialize session delete buttons
  $(".delete-session-button").click(function () {
    var button = $(this)

    $("#delete-session-modal").modal('show');

    // set delete function with element ID on modal button
    $("#delete-session-modal-button").click(function () {
      deleteSession(button);
    });
  });

});
