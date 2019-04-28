$(document).ready(function () {

  // initialize SimpleMDE only for cred_edit page
  if ($('#id_description').length ) {
    var descriptionMDE = new SimpleMDE({
      autoDownloadFontAwesome: false,
      spellChecker: false,
      status: false,
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

  // initialize groups selectize
  $('#id_groups').selectize({
    persist: false,
    plugins: ['remove_button'],
  });
  
  // initialize users selectize
  $('#id_users').selectize({
    persist: false,
    plugins: ['remove_button'],
  });

  // initialize tags selectize
  $('#id_tags').selectize({
    persist: false,
    maxItems: 10,
    plugins: ['remove_button'],
  });


  $('#id_uploads').change(function (e) {
    var uploadFiles = e.target.files;
    var fileList = '';

    for (var i = 0; i < uploadFiles.length; ++i ) {
      fileList = fileList + ' ' + uploadFiles[i].name
    }

    $('#upload-field-label').text(fileList)
  });
});

