var fetch_live_tv_videos = true;
var live_tv_comments_num = 1;
var fetch_live_tv_comments = true;


document.addEventListener('turbolinks:before-render', () => {
    $("#comments_home").off();
    $("#comments_post").off();
    $("#video-list").off();
    $("#comments_live_tv").off();
    $('#write-comment').off();
    $("#live_tv_icon_topic").css("display", "none");
});

document.addEventListener("turbolinks:load", function () {

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

    application.register("commandoShakti", class extends Stimulus.Controller {

        static get targets() {
            return ["topic", "live_id",]
        }

        connect() {
            let live_tv_icon_topic = document.getElementById("live_tv_icon_topic");
            window.addEventListener('scroll', paginate_commando_shakti);

            var live_id = `${this.live_idTarget.value}`;
            console.log(live_id)

            $(".livetv-page-comments").scroll(function () {
                load_comments_livetv(live_id);
            });

            if ($('body').width() > 768) {
                $.when(
                    $.getScript('https://d3pnd0n3snmitc.cloudfront.net/argus/video.min.js'),
                    $.getScript("https://d3pnd0n3snmitc.cloudfront.net/argus/videojs-ie8.min.js"),
                    $.Deferred(function (deferred) {
                        $(deferred.resolve);
                    })
                ).done(function () {
                    init_commando_livetv(); // Creates and attaches to DOM the <video> element (Live TV player)
                });
            }


        }

        disconnect() {
             if ($('body').width() > 768) {
                dispose_player_trending(); // Dispose the VideoJS Player
            }
            window.removeEventListener('scroll', paginate_commando_shakti);
        }
    });

    application.register("load_more_commando", class extends Stimulus.Controller {

        static get targets() {
            return ["live_id", "totalComments"]
        }

        load_live_tv_comments() {
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
                    url: "/page/live_tv_home/comments/?post_id=" + live_id + "&page=" + String(live_tv_comments_num),
                }).done(function (data) {
                    $("#comments-card").append(data);
                    setTimeout(function () {
                        fetch_live_tv_comments = true;
                    }, 1000);
                });
            }
        }
    });
})();

function paginate_commando_shakti() {
    if ((window.innerHeight + window.scrollY) >= (document.body.offsetHeight - 500)) {
        if (fetch_live_tv_videos) {
            live_tv_num += 1;
            fetch_live_tv_videos = false;
            $.ajax({
                type: 'GET',
                url: "/page/commando-shakti-videos" + "/?page=" + String(live_tv_num),
            }).done(function (data) {
                $("#video-list").append(data);
                fetch_live_tv_videos = true;
            });
        }
    }
}

function load_comments_livetv(live_id) {
    if (($(".livetv-page-comments").height() + $(".livetv-page-comments").scrollTop()) >= (document.body.offsetHeight - 3500)) {
        if (fetch_live_tv_comments) {
            live_tv_comments_num += 1;
            fetch_live_tv_comments = false;
            $.ajax({
                type: 'GET',
                url: "/page/live_tv/comments?live_id=" + live_id + "&page=" + String(live_tv_comments_num),
            }).done(function (data) {
                $("#comments-card").append(data);
                fetch_live_tv_comments = true;
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
        if (fetch_comments) {
            comments_page_num += 1;
            fetch_comments = false;
            $.ajax({
                type: 'GET',
                url: "/page/live_tv_home/comments/?live_id=" + live_id + "&page=" + String(comments_page_num),
            }).done(function (data) {
                $("#comments-card").append(data);
                fetch_comments = true;
            });
        }
    }
}

function init_commando_livetv() {
    /* Logic to initialize Live TV player */
    /* on connect() */

    let wrapper = $("#commando-player");
    let video = $('<video></video>');

    video.addClass('video-js');
    video.addClass('vjs-theme-fantasy');
    video.attr('id', "commando-livetv-video");
    wrapper.html("");
    video.appendTo(wrapper);

    videojs('commando-livetv-video', {
        autoplay: false,
        muted: true,
        controls: true,
        autoSetup: false,
        poster: "/app/static/img/argus_preview_mini.jpg",
        preload: "metadata",
        sources: [{
            src: source,
            type: "application/x-mpegURL",

        }],
        width: "295",
        height: "166",
        options: { navigationUI: 'show' },
        type: "application/x-mpegURL",
        notSupportedMessage: "Your browser1 does not support video; please enable JavaScript"
    });

}

function dispose_player_trending() {

    /* Dispose the VideoJS player on exiting the page */
    /* on disconnect() */

    let player = videojs("commando-livetv-video");
    if (player) {
        player.dispose();
    }
}