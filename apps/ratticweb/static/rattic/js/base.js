function searchCredentials() {
  var searchstr = $("#search-form-input").val();

  if (searchstr.length > 0) {
    baseUrl = window.location.protocol + "//" + window.location.host + "/"
    window.location = baseUrl + "cred/list-by-search/" + searchstr + "/";
  }

  return false
}

$(document).ready(function () {
  // register favorites menu toggle
  // register favorites menu toggle
  $('#favorites-menu-toggle').click(function (e) {
    e.preventDefault();
    $('#content-wrapper').toggleClass('disabled');
  });
 
  // register search form
  $('#search-form').submit(function (form) {
    searchCredentials()
    form.preventDefault();
  });
});

