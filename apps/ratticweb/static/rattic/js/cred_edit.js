$(document).ready(function () {

  // initialize SimpleMDE only for cred_edit page
  if ($('#id_description').length ) {
    var descriptionMDE = new SimpleMDE({
      autoDownloadFontAwesome: false,
      spellChecker: false,
      toolbar: [ 
        'heading-1','heading-2', 'heading-3', '|',
        'bold', 'italic', 'strikethrough', '|',
        'code', 'link', 'table', '|',
        'unordered-list', 'ordered-list', 'horizontal-rule', '|',
        'clean-block', 'preview',
      ],
      element: $('#id_description')[0]
    });
  }

});

