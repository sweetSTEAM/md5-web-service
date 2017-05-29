function error(info) {
    var err_p = $('#error');
    console.log(info);
    err_p.html('<h1>' + info + '</h1>');
    err_p.show();
    $('.w3-section').show();
    $('#header').text('Input url of a file');
    $("#butt").show();
}

function checkStatus(guid) {
    $.ajax({

        dataType: "json",
        url: '/api/get_status/' + guid,
        statusCode: {
            409: function(data) {
                console.log(data['responseJSON']['info']);
                $('#header').text('Progress: ' + data['responseJSON']['info'] + '%');
            }
        },
        success: function (data) {
            clearInterval(checker);
            console.log(data['info']);
            $('#header').text('Success');
            $('#md5').text(data['info']);
            $('#md5wrap').show();
        },
        error: function (data) {
            if (data['status'] != 409) {
                console.log(data['responseJSON']['info']);
                clearInterval(checker);
                error(data['responseJSON']['info']);
            }
        }
    })
}


$("#butt").click(function() {
    var url = $('#url').val();
    console.log(url);
    $.ajax({
        type: "POST",
        dataType: "json",
        url: '/api/post_link/',
        data: {'url': url},
        success: function (data) {
            $('.w3-section').hide();
            $('#error').hide();
            $('#header').text('Processing');
            $("#butt").hide();
            var guid = data['guid'];
            console.log(guid);
            checker = setInterval(checkStatus, 1000, guid);
        },
        error: function (data) {
            console.log(data);
            error(data['responseJSON']['message']);
        }
    });
});