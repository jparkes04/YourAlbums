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
            success: function(response){
                console.log(response);

                $("#favourite").text("Favourited!");
                console.log("Favourited!");
                $("#favourite").toggleClass("button-favourite button-unfavourite");
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    //$("#favourite").hasClass("button-unfavourite"
});