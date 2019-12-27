$(document).ready(function () {

    $(".delete_comment").click(function (event) {
        event.preventDefault();
        var comment_id = $(this).attr('id');
        var comment_url = $(this).attr("href")
        var comment = $(this).closest(".this_comment");
        var post_id = comment.attr("koko1");
        var comment_id = comment.attr("koko2");

        $.ajax({
            url: comment_url,
            data: {
                "pk": post_id,
                "com_id": comment_id
            },
            success: function (data) {
                comment.addClass("animated").addClass("hinge").css("z-index", "2000").delay(2000).slideUp( "slow", "swing");
                // alert(data['good_news'])
            },
            error: function (errorData) {
                console.log("error")
                console.log(errorData)
            }

        })

    });
});
