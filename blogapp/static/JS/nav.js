$(function () {
    var header = $("#navbar");
    var navlink = $(".nav-link")
    $(window).scroll(function () {
        var scroll = $(window).scrollTop();

        if (scroll >= 50) {
            // header.removeClass('rgba-stylish-strong').addClass("rgba-stylish-light");
            navlink.removeClass('p-3').addClass("p-2 ");
        } else {
            // header.removeClass("rgba-stylish-light").addClass('rgba-stylish-strong');
            navlink.removeClass('p-2 mdb-color darken-4').addClass("p-3");
        }
    });
});



$('.carousel').carousel({
    touch: true // default
    })



$(document).ready(function () {
    $("#searchForm").submit(function (e) {
        e.preventDefault();
        var serializedData = $(this).serialize();
        $.ajax({
            type: 'GET',
            url: "{% url 'blogapp:search' %}",
        });
    });
}); 



$(document).ready(function(){
    $("#contactForm").submit(function(e){
     // prevent from normal form behaviour
           e.preventDefault();
         // serialize the form data  
           var serializedData = $(this).serialize();
           $.ajax({
               type : 'POST',
               url :  "{% url 'contact_submit' %}",
               data : serializedData,
               success : function(response){
             //reset the form after successful submit
                   $("#contactForm")[0].reset(); 
               },
               error : function(response){
                   console.log(response)
               }
           });
    });
 });
 