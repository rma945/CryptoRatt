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
  value = document.cookie.match(new RegExp('(^| )' + 'disable_favorites' + '=([^;]+)'));
  if (value) {
    document.cookie = 'disable_favorites=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  } else {
    document.cookie = 'disable_favorites=true; path=/;';
  }
}

$(document).ready(function () {
  // initialize all tooltips
  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

  // open selected favorites item
  $(function () {
    favorites = localStorage.getItem('favorites_item')
    if (favorites) {
      $(favorites).collapse('show')
    }
  })

  // toggle favorites sidebar menu
  $('#favorites-menu-toggle').click(function (e) {
    e.preventDefault();
    $('#content-wrapper').toggleClass('disabled');
    toggleFavoritesMenu()
  });

  // toggle favorites 
  $('.card-header').click(function(e) {
    localStorage.setItem('favorites_item', e.target.parentNode.dataset.target);
  });
 
  // register search form
  $('#search-form').submit(function (form) {
    searchCredentials()
    form.preventDefault();
  });
});

