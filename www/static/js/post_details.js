var post_comments_page_num = 1;
var fetch_post_comments = true;
var details_page_num = 1;
var fetch_details_page_posts = true;
var details_id;
var postImage;


document.addEventListener('turbolinks:before-render', () => {
});

document.addEventListener('turbolinks:request-start', () => {
    $("#top-thin-line").addClass("d-none");
});

document.addEventListener('turbolinks:request-end', () => {
    $("#top-thin-line").removeClass("d-none");
});

document.addEventListener("turbolinks:load", function () {

});



(() => {
    const application = Stimulus.Application.start()
    application.register("load_more", class extends Stimulus.Controller {

        static get targets() {
            return ["post_id", "totalComments"]
        }

        load_comments() {
            var post_id = `${this.post_idTarget.value}`
            var total = `${this.totalCommentsTarget.value}`

            if ((post_comments_page_num + 1) * 5 >= total) {
                document.getElementById('load-more-button').style.display = "none";
            }

            if (fetch_post_comments) {
                post_comments_page_num += 1;
                fetch_post_comments = false;
                $.ajax({
                    type: 'GET',
                    url: "/post/page/comments?post_id=" + post_id + "&page=" + String(post_comments_page_num),
                }).done(function (data) {
                    $("#comments-card").append(data);
                    setTimeout(function () { fetch_post_comments = true; }, 1000);
                });
            }
        }
    }) 

    application.register("postDetails", class extends Stimulus.Controller {

        static get targets() {
            return ["leftSection", "middleSection", "rightSection", "post","postImage"]
        }

        connect() {

            details_id = `${this.postTarget.value}`;

            if (!document.documentElement.hasAttribute("data-turbolinks-preview")) {
                window.addEventListener('load', get_top_ads());
                if ($('body').width() >= 768) {
                    window.addEventListener('load', get_square_ad_template());
                }

            }

            window.addEventListener('scroll', paginate_details_posts);
            $("#post_details_read_more").click(function () {
                paginate_details_posts()
            })

            let post_id = `${this.postTarget.value}`;
            $('.comments-modal-content').scroll(function () {
                load_mobile_comments(post_id);
            });

            $('.details-description a').not('.details-description a[href*="twitter.com/"]').attr('target','_blank');

            // Add span tag with hastag class for all the hastags in article.
            if ($(".fp-para-text").html()){
                $(".fp-para-text").html($(".fp-para-text").html().replace(/(#\S+)/g, "<span class='hashtag'>$1</span>"));
            }

            if ($(".post-text").html()){
                $(".post-text").html($(".post-text").html().replace(/(#\S+)/g, "<span class='hashtag'>$1</span>"));
            }

            //Once the hashtag is clicked open that particular hashtag in search bar
            $(".hashtag").click(function () {
                search_string = (this.innerText).trim();
                Turbolinks.visit("/search-articles?search_string=" + encodeURIComponent(search_string));
            });
        }

        disconnect() {

            $("#brand-logo-sec-wrapper").removeClass("d-none").addClass("d-flex");
            $(".header-back-btn").removeClass("d-block").addClass("d-none");
            $(".comments-modal-content").off();
            // window.removeEventListener('scroll', paginate_details_posts);
            $(".hashtag").off();
        }
    });
})();

function paginate_details_posts() {
    if ((window.innerHeight + window.scrollY) >= (document.body.offsetHeight) - 3000) {
        if (fetch_details_page_posts) {
            details_page_num += 1;
            fetch_details_page_posts = false;
            $.ajax({
                type: 'GET',
                url: "/page/details_posts?post_id=" + details_id + "&page=" + String(details_page_num),
            }).done(function (data) {
                $("#post_detail").append(data);
                if($('body').width() <= 768 && (details_page_num >= 5)){
                    window.removeEventListener('scroll', paginate_details_posts);
                    $('#post_details_footer_section').css('display','block');
                    $('#post_detail').append($('#post_detail #post_details_footer_section'));
                }
                fetch_details_page_posts = true;
            });
        }
    }
}

function load_mobile_comments(post_id) {
    if (($(".comments-modal-content").height() + $(".comments-modal-content").scrollTop()) >= (document.body.offsetHeight) - 500) {
        if (fetch_post_comments) {
            post_comments_page_num += 1;
            fetch_post_comments = false;
            $.ajax({
                type: 'GET',
                url: "/post/page/comments?post_id=" + post_id + "&page=" + String(post_comments_page_num),
            }).done(function (data) {
                $("#comments-mobile-card").append(data);
                fetch_post_comments = true;
            });
        }
    }
}



function track_ad_impressions(ads_list, top_ads, desktop_ads){

    $.ajax({
        type: 'POST',
        data :{"ads_id_list":ads_list,"top_ads": top_ads, "desktop_ads": desktop_ads},
        url: "/update_ad_impressions",
    }).done(function (data) {
    });

}
