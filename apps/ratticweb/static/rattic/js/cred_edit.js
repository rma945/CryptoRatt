// validatePasswordModal:
// set minimal symbols count for a password modal window
function validatePasswordModal() {
  var setDefault = true

  $("input[type='checkbox']").each(function () {
    if ($(this).prop('checked')) {
      setDefault = false
      return false;
    }
  });
  
  // set default lowerCase letters for password generation
  if (setDefault) {
    $('#lowercase-switch').prop('checked', true);
  }
}

function calculatePasswordStrengthModal() {
  var passwordStrength = 0;
  var passwordLength = $('#password-length-custom-input').val();
  var color = 'danger';

  // generate password
  if ($("#lowercase-switch").prop('checked') ) {
    passwordStrength += 1
  } 
  if ($("#uppercase-switch").prop('checked')) {
    passwordStrength += 1
  }
  if ($("#numbers-switch").prop('checked')) {
    passwordStrength += 1
  }
  if ($("#special-switch").prop('checked')) {
    passwordStrength += 2
  }

  // calculate password length
  switch (true) {
    case (passwordLength <= 6):
      passwordStrength = 1
      break;
    case (passwordLength >= 6 && passwordLength <= 8):
      passwordStrength = 2
      break;
    case (passwordLength >= 8 && passwordLength <= 12):
      passwordStrength += 2
      break;
    case (passwordLength >= 12 && passwordLength <= 16):
      passwordStrength += 3
      break;
    case (passwordLength >= 16 && passwordLength <= 20):
      passwordStrength += 4
      break;
    case (passwordLength >= 20):
      passwordStrength += 5
      break;
  }
  // calculate color-class
  if (passwordStrength <= 4 ) {
    color = 'danger';
  } else if (passwordStrength <= 6) {
    color = 'warning';
  } else {
    color = 'success';
  }

  $('#password-strength-bar').attr('style', 'width:' + passwordStrength * 10 + '%');
  $('#password-strength-bar').attr('class', 'progress-bar progress-bar-striped bg-' + color  )
  $('#generate-password-modal-header').attr('class', 'modal-header text-white bg-' + color)
}

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
  var passwordLength = $('#password-length-custom-input').val();

  // get password length from checkboxex
  $(".form-check-input").each(function () {
    if ($(this).prop('checked')) {
      passwordLength = $(this).val();
      return false;
    }
  });

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

// set added filenames at files upload field
function updateFilesUploadField() {
  var uploadFiles = e.target.files;
  var fileList = '';

  for (var i = 0; i < uploadFiles.length; ++i) {
    fileList = fileList + ' ' + uploadFiles[i].name
  }

  $('#upload-field-label').text(fileList)
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

  // initialize SimpleMDE
  new SimpleMDE({
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
  $('#id_uploads').change(function () {
    updateFilesUploadField();
  });

  // register modal password slider function
  $('#password-length-slider').on('input', function () {
    passwordLength = $(this).val()
    $('#password-length-custom-input').val(passwordLength);
  });

  $('#password-length-slider').change(function () {
    calculatePasswordStrengthModal();
  });

  $('#password-length-custom-input').on('input', function () {
    if ($(this).val() > 128) {
      $(this).val(128)
    }
    if ($(this).val() < 6) {
      $(this).val(6)
    }

    $('#password-length-slider').val($(this).val());
    calculatePasswordStrengthModal();
  });
 
  $("input[type='checkbox']").click(function () {
    validatePasswordModal();
    calculatePasswordStrengthModal();
  });


  // register modal window for icon select
  $('#icon-select-button').click(function () {
    $('#select-icons-modal').modal('show')
  });
  
});