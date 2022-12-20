var topic_page_num = 1;
var fetch_topic_page_posts = true;
var topic_comments_page_num = 1;
var topic_fetch_comments = true;
var topic_id = ""

document.addEventListener('turbolinks:before-render', () => {
    $("#comments_home").off();
    $("#comments_post").off();
    $("#video-list").off();
    $("#comments_live_tv").off();
    $('#write-comment').off();

    $("#live_tv_icon_topic").css("display", "none");
});

document.addEventListener("turbolinks:load", function () {
    /* Below JS prevents margin-right: 15px to be added to body on Bootstrap modal open.
        This is a feature/bug in Bootstrap itself! */
    $(document.body).on('hide.bs.modal,hidden.bs.modal', function () {
        $('body').css('padding-right', '0');
    });

    $('#write-comment').on('input keyup keypress cut copy paste', function (e) {
        const MAX_CHAR_COUNT = 200;

        if (e.target.value.length > MAX_CHAR_COUNT) {
            $("#character-count").html("0");
            e.preventDefault();
            return false;
        } else {
            write_comment(e);
        }
    });

    $("#live_tv_icon_topic").css("display", "block");
});


(() => {
    const application = Stimulus.Application.start()

    application.register("topicController", class extends Stimulus.Controller {

        static get targets() {
            return ["live_id", "topic_id"]
        }

        connect() {
            topic_id = `${this.topic_idTarget.value}`
            var search_location;
            $(".search_location_option_topic").click(function () {
                search_location = $(this).text();
                $("#search_location_topic").val(search_location);
                $(this).parents('.btn-group').find('.dropdown-toggle').html(search_location);
                if ($.trim($('#search_location').val()) != 'Select Location') {
                    Turbolinks.visit("/topics/odisha/" + encodeURIComponent(search_location));
                }
                // window.location.href = "/topics/odisha/" + encodeURIComponent(search_location);
            });
            $("#clear_filter_topic").click(function () {
                 Turbolinks.visit("/topics/odisha");
            });

            window.addEventListener('scroll', paginate_topic_posts);
            $("#topic_read_more").click(function () {
                paginate_topic_posts()
            })

            var live_id = `${this.live_idTarget.value}`;

            $(".comments-overflow").scroll(function () {
                load_comments(live_id);
            });

            if ($('body').width() > 768) {
                $.when(
                    $.getScript('https://d3pnd0n3snmitc.cloudfront.net/argus/video.min.js'),
                    $.getScript("https://d3pnd0n3snmitc.cloudfront.net/argus/videojs-ie8.min.js"),
                    $.Deferred(function (deferred) {
                        $(deferred.resolve);
                    })
                ).done(function () {
                    init_topics_livetv(); // Creates and attaches to DOM the <video> element (Live TV player)
                });
            }

            $("#widget-share-div").hide(100);
            $("#widget-share-btn").on('click', function () {
                $("#widget-share-div").toggle(500);
            });


            if (!document.documentElement.hasAttribute("data-turbolinks-preview")) {
                window.addEventListener('load', get_top_ads());
                if ($('body').width() >= 768) {
                    window.addEventListener('load', get_square_ad_template());
                }
            }


        }

        disconnect() {
            window.removeEventListener('scroll', paginate_topic_posts);
            if ($('body').width() > 768) {
                dispose_player_topics(); // Dispose the VideoJS Player
            }
            $("#widget-share-div").hide(100);
            $("#widget-share-btn").off("click");
        }

    });

    application.register("load_more_topics", class extends Stimulus.Controller {

        static get targets() {
            return ["live_id", "totalComments"]
        }

        load_topic_comments() {
            var live_id = `${this.live_idTarget.value}`
            var total = `${this.totalCommentsTarget.value}`

            if ((topic_comments_page_num + 1) * 5 >= total) {
                document.getElementById('load-more-button').style.display = "none";
            }

            if (topic_fetch_comments) {
                topic_comments_page_num += 1;
                topic_fetch_comments = false;
                $.ajax({
                    type: 'GET',
                    url: "/page/live_tv_home/comments/?post_id=" + live_id + "&page=" + String(topic_comments_page_num),
                }).done(function (data) {
                    $("#comments-card").append(data);
                    setTimeout(function () {
                        topic_fetch_comments = true;
                    }, 1000);
                });
            }
        }
    });
})();

function paginate_topic_posts() {
    if ((window.innerHeight + window.scrollY) >= (document.body.offsetHeight - 3000)) {
        if (fetch_topic_page_posts) {
            topic_page_num += 1;
            fetch_topic_page_posts = false;
            const location_string = $.trim($('#search_location_topic').val());
            let strUrl = "";
            if (location_string != '') {
                strUrl = "/page/topic_posts_lacation?topic_id=" + topic_id + "&page=" + String(topic_page_num) + "&location_string=" + String(location_string);
            } else {
                strUrl = "/page/topic_posts?topic_id=" + topic_id + "&page=" + String(topic_page_num);
            }
            $.ajax({
                type: 'GET',
                url: strUrl,
            }).done(function (data) {
                $("#home-posts").append(data);
                if ($('body').width() <= 768 && (topic_page_num >= 5)) {
                    window.removeEventListener('scroll', paginate_topic_posts);
                    $('#topic_footer_section').css('display', 'block');
                    $('#home-posts').append($('#home-posts #topic_footer_section'));
                }
                fetch_topic_page_posts = true;
            });
        }
    }
}

function write_comment(e) {
    const MAX_CHAR_COUNT = 200;
    let text_length = e.target.value.length;
    let char_count = $("#character-count");

    if (text_length == 0) {
        char_count.html(String(MAX_CHAR_COUNT));
    }

    char_count.html(MAX_CHAR_COUNT - text_length);
}

function load_comments(live_id) {
    if (($(".comments-overflow").height() + $(".comments-overflow").scrollTop()) >= (document.body.offsetHeight - 4000)) {
        if (topic_fetch_comments) {
            comments_page_num += 1;
            topic_fetch_comments = false;
            $.ajax({
                type: 'GET',
                url: "/page/live_tv_home/comments/?live_id=" + live_id + "&page=" + String(comments_page_num),
            }).done(function (data) {
                $("#comments-card").append(data);
                topic_fetch_comments = true;
            });
        }
    }
}

function init_topics_livetv() {
    /* Logic to initialize Live TV player */
    /* on connect() */

    let wrapper = $("#topics-player");
    let video = $('<video></video>');

    video.addClass('video-js');
    video.addClass('vjs-theme-fantasy');
    video.attr('id', "topics-livetv-video");
    wrapper.html("");
    video.appendTo(wrapper);

    videojs('topics-livetv-video', {
        autoplay: false,
        muted: true,
        controls: true,
        disablePictureInPicture: true,
        autoSetup: false,
        poster: "/app/static/img/argus_preview_mini.jpg",
        preload: "metadata",
        sources: [{
            src: source,
            type: "application/x-mpegURL",

        }],
        width: "295",
        height: "166",
        options: {navigationUI: 'show'},
        type: "application/x-mpegURL",
        notSupportedMessage: "Your browser does not support video; please enable JavaScript"
    });
    $(".vjs-picture-in-picture-control").addClass('d-none');

}

function dispose_player_topics() {

    /* Dispose the VideoJS player on exiting the page */
    /* on disconnect() */

    let player = videojs("topics-livetv-video");
    if (player) {
        player.dispose();
    }
}
