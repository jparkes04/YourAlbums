$(document).ready(function () {
    $("#favourite").on("click", function () {
        $.ajax({
            url: '/favourite',
            type: 'POST',
            data: JSON.stringify({
                // Pass user and album IDs so that the favourite can be added to database
                user_id: $("#favourite").attr('data-userid'),
                album_id: $("#favourite").attr('data-albumid')
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (response) {
                if (response.favourited) {
                    // Favourite added - change button text
                    $("#favourite").text("Favourited!");
                } else {
                    // Favourite removed - change button text
                    $("#favourite").text("Favourite");
                }

                // Toggle button styling
                $("#favourite").toggleClass("button-favourite button-unfavourite");
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});