$(document).ready(function () {
    $("#favourite").on("click", function() {
        $.ajax({
            url: '/favourite',
            type: 'POST',
            data: JSON.stringify({
                user_id: $("#favourite").attr('data-userid'),
                album_id: $("#favourite").attr('data-albumid')
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                if (response.favourited) {
                    $("#favourite").text("Favourited!");
                } else {
                    $("#favourite").text("Favourite");
                }

                $("#favourite").toggleClass("button-favourite button-unfavourite");
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});