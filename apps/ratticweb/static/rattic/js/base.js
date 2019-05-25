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

function searchCredentials() {
  var searchstr = $("#search-form-input").val();

  if (searchstr.length > 0) {
    baseUrl = window.location.protocol + "//" + window.location.host + "/"
    window.location = baseUrl + "cred/list-by-search/" + searchstr + "/";
  }

  return false
}

function toggleFavoritesMenu() {
  value = document.cookie.match(new RegExp('(^| )' + 'favorites_menu' + '=([^;]+)'));
  
  if (value) {
    if (value[2] == 'false') {
      document.cookie = 'favorites_menu=true; path=/;';
    } else {
      document.cookie = 'favorites_menu=false; path=/;';
    }
  } else {
    document.cookie = 'favorites_menu=false; path=/;';
  }
}

$(document).ready(function () {
  // register favorites menu toggle
  $('#favorites-menu-toggle').click(function (e) {
    e.preventDefault();
    $('#content-wrapper').toggleClass('disabled');
    toggleFavoritesMenu()
  });
 
  // register search form
  $('#search-form').submit(function (form) {
    searchCredentials()
    form.preventDefault();
  });
});

