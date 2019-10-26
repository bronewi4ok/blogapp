function turnThePage () {
    $("#next_page_btn").click(function (event) {
        event.preventDefault();
        var page = $(this).attr('href');
        $.ajax({
            data: { 'page' : page },
            success: function (data) {
                $(".main").empty();
                $(".main").append( $(data).find(".main").html() );

                $(".pagination").empty();
                $(".pagination").append( $(data).filter(".pagination").html() );
            },
            error: function () {
                alert('опаньки');
            }
        })
    });
}

$(document).ready( function() {
    turnThePage();
})

$(document).ajaxStop( function() {
    turnThePage();
})