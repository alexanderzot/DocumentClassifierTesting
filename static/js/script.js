// setting for django POST ajax enable
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; ++i) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// Sign Out
$('#singOut').click(function(e){
    e.preventDefault()

    $.ajax({
        type: "POST",
        url: "/api/user/sign_out/",
        success: function (data){
            location.reload();
        },
        error: function(request, status, errorT) {
             alert('Произошел сбой. Запрос не может быть выполнен. Повторите попытку.');
        }
    });
});

// Sign In
$('#formSignIn').submit(function(e){
    e.preventDefault()

    var sendData = {
        'email': $('#inputSignInEmail').val(),
        'password': $('#inputSignInPassword').val(),
    };

    $.ajax({
        type: "POST",
        url: "/api/user/sign_in/",
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(sendData),
        success: function (data, textStatus) {
            if (textStatus === 'success') {
                location.reload();
            }
            else {
                $('#inputSignInPassword').val('');
                $('#alertSignIn').text('Неправильно указан логин и/или пароль!').collapse("show");
            }
        },
        error: function (request, status, errorT) {
            alert('Произошел сбой. Запрос не может быть выполнен. Повторите попытку.');
        }
    });
});

$('#modalSignIn').on('hidden.bs.modal', function () {
    $('#inputSignInEmail').val('');
    $('#inputSignInPassword').val('');
    $('#alertSignIn').collapse("hide");
});


// Sign Up
$('#formSignUp').submit(function(e){
    e.preventDefault();

    var email =  $('#inputSignUpEmail').val();
    var pass1 =  $('#inputSignUpPassword').val();
    var pass2 =  $('#inputSignUpPassword2').val();

    var sendData = {
        'email': email,
        'password1': pass1,
        'password2': pass2
    };

    $.ajax({
        type: "POST",
        url: "/api/user/sign_up/",
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(sendData),
        success: function (data, textStatus) {
            var alert = $('#alertSignUp');
            if (data['status'] === 'OK') {
                // show success message
                alert.addClass('alert-success').removeClass('alert-danger');
                alert.text(data['msg']);

                // login to system
                $.ajax({
                        type: "POST",
                        url: "/api/user/sign_in/",
                        dataType: 'json',
                        contentType: 'application/json; charset=utf-8',
                        data: JSON.stringify({
                            'email':    email,
                            'password': pass1
                        }),
                        success: function (data, textStatus) {
                            if (data['status'] === 'OK') {
                                location.reload();
                            }
                        },
                        error: function (request, status, errorT) {
                            alert('Произошел сбой. Запрос не может быть выполнен. Повторите попытку.');
                        }
                });
            }
            else {
                // show error message
                alert.removeClass('alert-success').addClass('alert-danger');
                alert.text(data['msg']);
            }
            alert.collapse("show");
        },
        error: function (request, status, errorT) {
            alert('Произошел сбой. Запрос не может быть выполнен. Повторите попытку.');
        }
    });
});

$('#modalSignUp').on('hidden.bs.modal', function () {
    $('#inputSignUpEmail').val('');
    $('#inputSignUpPassword').val('');
    $('#inputSignUpPassword2').val('');
    $('#alertSignUp').collapse("hide");
});

/* File upload */
var fileInput = $('#inputFile');
fileInput = document.getElementById('inputFile');
fileInput.addEventListener('change', function (event) {
//fileInput.on('change', function (event) {
    var files = fileInput.files;
    var fileCount = files.length;

    var fileName = files[0].name;

    console.log(fileName);

    //if (fileName.length > 15)
    //    document.getElementById('id_file_input_label').innerHTML = fileName.substr(1, 15) + '...';
    //else
    //    document.getElementById('id_file_input_label').innerHTML = fileName;
    document.getElementById('id_file_input_label').innerHTML = 'Файл готов к загрузке   ';
    document.getElementById('id_file_name').value = fileName;

    //var count = fileInput.length;
    //console.log(fileInput[0].files[0].name);
    // type size
    //var count = files.length;

    //alert(files[0].name);
}, false);