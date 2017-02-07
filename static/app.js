class Yui2 {
    constructor () {
        this.bindEvents();
    }

    setPhoto (base64img) {
        var $photo = $('#photo');
        $photo.attr('data-photo', base64img);
        var $img = $(`<img src="${base64img}" class="user-photo">`);
        $photo[0].innerHTML = '';
        $photo.append($img);
        setBgColor('#78909C');
    }

    post () {
        var $photo = $('#photo');
        var base64img = $photo.attr('data-photo');
        if ($('#fg').length > 0) return;

        $.ajax({
            url: '/api/v0/detect',
            data: JSON.stringify({
                image: base64img.replace(/^data:image\/(.+);base64,/, '')
            }),
            type: "POST",
            contentType:'application/json',
            success: function (response) {
                $('#res-img').attr('src', response.base64image);
                $('#res-e').html(response.description);
            },
            error: function (response) {
                console.info(response);
            }
        });

    }

    bindEvents () {
        var self = this;

        var setDragDesign = function () {
            $('#photo').css({
                'background-color': '#FFE082'
            });
        };

        var resetDragDesign = function () {
            $('#photo').css({
                'background-color': '#e9e7e4'
            });
        };

        $('#btn-gyazo').on('click', function () {
            var $img = $('#res-img');
            var imageUrl = $img.attr('src');
            if (imageUrl.length > 30 && imageUrl.startsWith('data:image')) {
                uploadToGyazo(imageUrl);
            }
        });

        $('#photo').bind('drop', e => {
            resetDragDesign();
            e.preventDefault();
            var files = e.originalEvent.dataTransfer.files;
            var reader = new FileReader();
            if (files.length <= 0) return false;
            // 複数与えられた場合でも，読み込むのは最初のファイルのみ
            var file = files[0];

            if (!file.type.match('image.*')) return false;
            reader.onload = function (e) {
                var base64code = e.target.result;
                self.setPhoto(base64code);
            };
            reader.readAsDataURL(file);
        }).bind('dragenter', e => {
            setDragDesign();
            return false;
        }).bind('dragover', e => {
            return false;
        }).bind('dragleave', e => {
            resetDragDesign();
            return false;
        });
    }
}


var setBgColor = function (color) {
    var $bg = $('#response');
    $bg.css('background-color', color);
}


var uploadToGyazo = function (imageUrl) {
    var $img = $('#gyazo-session');
    $.ajax({
        url: '/api/v0/gyazo',
        type: 'post',
        data: JSON.stringify({
            //'client_id': apiKeys.gyazo_client_id,
            'image_url': imageUrl,
            'referer_url': 'https://daiiz-apps.appspot.com/labs/yui',
            'title': 'Yui'
        }),
        contentType: 'application/json',
        dataType: 'json'
    }).success(function (data) {
        var gyazoImgUrl = data.get_image_url;
        $img.attr('src', gyazoImgUrl);
        setBgColor('#448AFF');
    }).fail(function (err) {
        console.log(err);
    });
};

$(function () {
    var yui = new Yui2();
    setBgColor('#78909C');

    $('#btn-send').on('click', e => {
        yui.post();
    });

});
