$(document).ready(function () {
  // initialize tooltips
  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

  // initialize users selectize
  $('#id_credentials').selectize({
    persist: false,
    plugins: ['remove_button'],
  });

  // initialize SimpleMDE
  new SimpleMDE({
    autoDownloadFontAwesome: false,
    spellChecker: false,
    status: false,
    toolbar: [
      'heading-1', 'heading-2', 'heading-3', '|',
      'bold', 'italic', 'strikethrough', '|',
      'code', 'link', 'table', '|',
      'unordered-list', 'ordered-list', 'horizontal-rule', '|',
      'clean-block', 'preview',
    ],
    element: $('#id_description')[0]
  });
});