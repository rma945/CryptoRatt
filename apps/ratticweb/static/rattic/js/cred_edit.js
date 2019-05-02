// variables

function generateRandomPassword(lower=true, upper=true, numbers=true, special=false, length=16) {
  var generatedPassword = '';
  var symbolArray = [];
  var lowerList = "abcdefghijklmnopqrstuvwxyz"
  var upperList = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  var numbersList = "0123456789";
  var specialList = "!@#$%^&*()_-+=:;',.<>?/"

  // actualize symbols dict
  if (lower) { symbolArray.push(lowerList);}
  if (upper) { symbolArray.push(upperList);}
  if (numbers) { symbolArray.push(numbersList);}
  if (special) { symbolArray.push(specialList);}
  
  // generate password strings
  for (var i = 0; i < length; i++) {
    randomKey = Math.floor(Math.random() * (symbolArray.length))
    generatedPassword += symbolArray[randomKey].charAt(Math.floor(Math.random() * symbolArray[randomKey].length));
  }

  return generatedPassword
}

function setRandomPassword() {
  var passwordLength = 24;

  // get password length from checkboxex
  $(".form-check-input").each(function () {
    if ($(this).prop('checked')) {
      passwordLength = $(this).val();
      return false;
    }
  });

  // set custom password length if need
  if ($("#lengthCustom").val()) {
    passwordLength = $("#lengthCustom").val();
  }

  // generate password
  password = generateRandomPassword(
    lower = $("#lowercase-switch").prop('checked'),
    upper = $("#uppercase-switch").prop('checked'),
    numbers = $("#numbers-switch").prop('checked'),
    special = $("#special-switch").prop('checked'),
    length = passwordLength
  )

  // set password
  $("#id_password").attr('value', password)
}

function showPassword() {
  if ($('#id_password').attr('type') == 'password') {
    $('#id_password').attr('type', 'text');
  } else {
    $('#id_password').attr('type', 'password');
  }
}

$(document).ready(function () {

  // initialize passwordGenerate button
  $('#set-password-button').click(function () {
    setRandomPassword();
    $('#generate-password-modal').modal('hide')
  });

  // initialize show password button
  $("#show-password-button").click(function () {
    showPassword();
  });

  // initialize SimpleMDE only for cred_edit page
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

  // add upload filenames at upload files panel
  $('#id_uploads').change(function (e) {
    var uploadFiles = e.target.files;
    var fileList = '';

    for (var i = 0; i < uploadFiles.length; ++i ) {
      fileList = fileList + ' ' + uploadFiles[i].name
    }

    $('#upload-field-label').text(fileList)
  });
});

