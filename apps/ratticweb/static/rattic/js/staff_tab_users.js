$(document).ready(function () {
  
  // add selection highlight throught JS for a correct colors in all boostrap themes
  $(".users-tab").hover(function () {
    $(this).toggleClass("bg-light");
  }, function () {
      $(this).toggleClass("bg-light");
  });
});