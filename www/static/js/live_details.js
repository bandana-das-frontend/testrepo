var fetch_live_tv_comments = true;
var live_tv_comments_num = 1;
var details_page_videos_num = 1;
var fetch_details_page_videos = true;
var details_id;

document.addEventListener('turbolinks:before-render', () => {
});

document.addEventListener("turbolinks:load", function () {
});

document.addEventListener('turbolinks:request-start', () => {
    $("#top-thin-line").addClass("d-none");
});

document.addEventListener('turbolinks:request-end', () => {
    $("#top-thin-line").removeClass("d-none");
});

(() => {
    const application = Stimulus.Application.start()
    application.register("load_more", class extends Stimulus.Controller {

        static get targets() {
            return ["live_id", "totalComments"]
        }

        load_live_comments() {
            var live_id = `${this.live_idTarget.value}`
            var total = `${this.totalCommentsTarget.value}`

            if ((live_tv_comments_num + 1) * 5 >= total) {
                document.getElementById('load-more-button').style.display = "none";
            }

            if (fetch_live_tv_comments) {
                live_tv_comments_num += 1;
                fetch_live_tv_comments = false;
                $.ajax({
                    type: 'GET',
                    url: "/page/live_details/comments?live_id=" + live_id + "&page=" + String(live_tv_comments_num),
                }).done(function (data) {
                    $("#comments-card").append(data);
                    setTimeout(function () { fetch_live_tv_comments = true; }, 1000);
                });
            }
        }
    });

    application.register("videoDetails", class extends Stimulus.Controller {

        static get targets() {
            return ["leftSection", "middleSection", "rightSection", "video"]
        }

        connect() {
            details_id = `${this.videoTarget.value}`;
            window.addEventListener('scroll', paginate_details_video);
            $("#live_detail_read_more").click(function () {
                paginate_details_video()
            })

            let live_id = `${this.videoTarget.value}`;
            $('.comments-modal-content').scroll(function () {
                load_mobile_comments(live_id);
            });
            $(".live-post-text").html($(".live-post-text").html().replace(/(#\S+)/g, "<span class='hashtag'>$1</span>"));
            $(".hashtag").click(function () {
                search_string = (this.innerText).trim();
                Turbolinks.visit("/search-articles?search_string=" + encodeURIComponent(search_string));
            });

            if (!document.documentElement.hasAttribute("data-turbolinks-preview")) {
                window.addEventListener('load', get_top_ads());
                if ($('body').width() >= 768) {
                    window.addEventListener('load', get_square_ad_template());
                }
            }
        }

        disconnect() {
            window.removeEventListener('scroll', paginate_details_video);
            $(".comments-modal-content").off();
            $(".hashtag").off();
        }
    });

})();

function paginate_details_video() {
    if ((window.innerHeight + window.scrollY) >= (document.body.offsetHeight) - 3000) {
        if (fetch_details_page_videos) {
            details_page_videos_num += 1;
            fetch_details_page_videos = false;
            $.ajax({
                type: 'GET',
                url: "/page/details_videos?video_id=" + details_id + "&page=" + String(details_page_videos_num),
            }).done(function (data) {
                $("#video_details").append(data);
                if ($('body').width() <= 768 && (details_page_videos_num >= 5)) {
                    window.removeEventListener('scroll', paginate_details_video);
                    $('#live_detail_footer_section').css('display','block');
                    $('#video_details').append($('#video_details #live_detail_footer_section'));
                }

                fetch_details_page_videos = true;
            });
        }
    }
}

function load_mobile_comments(live_id) {
    if (($(".comments-modal-content").height() + $(".comments-modal-content").scrollTop()) >= (document.body.offsetHeight) - 500) {
        if (fetch_live_tv_comments) {
            live_tv_comments_num += 1;
            fetch_live_tv_comments = false;
            $.ajax({
                type: 'GET',
                url: "/page/live_details/comments?live_id=" + live_id + "&page=" + String(live_tv_comments_num),
            }).done(function (data) {
                $("#comments-mobile-card").append(data);
                fetch_live_tv_comments = true;
            });
        }
    }
}