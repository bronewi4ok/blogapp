$(function () {
    var navlink = $(".nav-link")
    $(window).scroll(function () {
        var scroll = $(window).scrollTop();

        if (scroll >= 100) {
            navlink.removeClass('p-3').addClass("p-2 ");
        } else {
            navlink.removeClass('p-2 mdb-color darken-4').addClass("p-3");
        }
    });
});

$(function () {
    $(window).on('resize', function () {
        if ($(window).width() > 767) {
            // $('#navbar').addClass('fixed-top');
            // $('#navbar').removeClass('fixed-bottom');
            $('#navbar').addClass('p-3');
            $('#navbar').removeClass('p-1');
            $('#btnNewPost').addClass('btn-circle');
            $('#btnNewPost').removeClass('btn-social');


        } else {
            // $('#navbar').addClass('fixed-bottom');
            // $('#navbar').removeClass('fixed-top');
            $('#navbar').addClass('p-1');
            $('#navbar').removeClass('p-3');
            $('#btnNewPost').addClass('btn-social');
            $('#btnNewPost').removeClass('btn-circle');

        }
    })
});





