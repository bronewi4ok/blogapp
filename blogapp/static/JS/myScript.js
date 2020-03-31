// Scroll progress



var prev = 0;
var $window = $(window);
var nav = $('.navbar');

$window.on('scroll', function () {
    var scrollTop = $window.scrollTop();
    nav.toggleClass('hidden', scrollTop > prev);
    prev = scrollTop;

    if (scrollTop == 0) {
        $('.navbar').removeClass('rgba-stylish-light').addClass('z-depth-0');
    } else {
        $('.navbar').addClass('rgba-stylish-light').removeClass('z-depth-0');
    }
}); 


// function nextPage() {
//     $(".js_page_btn").click(function (event) {
//         event.preventDefault();
//         var page = $(this).attr('href');
//         console.log("KUKUMBER")

//         $.ajax({
//             data: { 'page' : page },
//             success: function (data) {
//                 $(".ajax_main").empty();
//                 $(".ajax_main").append( $(data).find(".main").html() );

//                 $(".pagination").empty();
//                 $(".pagination").append( $(data).filter(".pagination").html() );
//             },
//             error: function () {
//                 alert('опаньки');
//             }
//         })
//     });
// }

// function previousPage () {
//     $(".js_page_btn").click(function (event) {
//         event.preventDefault();
//         var page = $(this).attr('href');
//         $.ajax({
//             data: { 'page' : page },
//             success: function (data) {
//                 console.log("KUKUMBER")
//                 $(".ajax_main").empty();
//                 $(".ajax_main").append( $(data).find(".main").html() );

//                 $(".pagination").empty();
//                 $(".pagination").append( $(data).filter(".pagination").html() );
//             },
//             error: function () {
//                 alert('опаньки');
//             }
//         })
//     });
// }

// $(document).ready( function() {
//     nextPage();
//     previousPage();
// })

// $(document).ajaxStop( function() {
//     previousPage();
//     nextPage();
// })


// Last attempt
// $(".js_page_btn").click(function (event) {
//     event.preventDefault();
//     var page = $(this).attr('href');

//     $.ajax({
//         url: page,
//         data: {horible: page},
//         success: function (data) {
//             $(".ajax_main").empty();
//             // $(".ajax_main").append($(data).find('.ajax_main').html());
//             // $(".ajax_main").append(data);

//             $(".ajax_main").append( $(data).filter(".ajax_main").html(data) );
//             // var opop = $(".ajax_main").find('.hz_ajax').html();



//             $(".pagination").empty();
//             $(".pagination").append( $(data).find(".pagination").html() );
//         },
//         error: function () {
//             console.log("MASAKRA")
//         },

//     })
// });