function ProfileSubmitForm() {

}


$(document).ready(function () {
  // initialize users selectize
  $('#id_favourite_tags').selectize({
    persist: false,
    plugins: ['remove_button'],
  });

  // initialize submit form
  $("#profile-submit-button").click(function () {
    console.log("submit")
    $("#profile-submit-form").submit();
  });

});

