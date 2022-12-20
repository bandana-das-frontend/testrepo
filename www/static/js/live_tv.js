var fetch_live_tv_videos = true;
var live_tv_num = 1;
var live_tv_comments_num = 1;
var fetch_live_tv_comments = true;
var topic;

document.addEventListener('turbolinks:before-render', () => {
    $(".livetv-page-comments").off();
    $('#write-comment').off();
});

document.addEventListener("turbolinks:load", function () {
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
});

document.addEventListener('turbolinks:request-start', () => {
    $("#top-thin-line").addClass("d-none");
});

document.addEventListener('turbolinks:request-end', () => {
    $("#top-thin-line").removeClass("d-none");
});

(() => {
    const application = Stimulus.Application.start()

    application.register("livetvController", class extends Stimulus.Controller {

        static get targets() {
            return ["topic", "live_id",]
        }

        connect() {
            topic = `${this.topicTarget.value}`;
            if (topic == "" || topic == null)
                topic = "All";
            live_tv_num = 1;

            window.addEventListener('scroll', paginate_live_tv);
            $("#livetv_read_more").click(function () {
                paginate_live_tv()
            })



            var live_id = `${this.live_idTarget.value}`;

            $(".livetv-page-comments").scroll(function () {
                load_comments_livetv(live_id);
            });

            $.when(
                $.getScript('https://d3pnd0n3snmitc.cloudfront.net/argus/video.min.js'),
                $.getScript( "https://d3pnd0n3snmitc.cloudfront.net/argus/videojs-ie8.min.js" ),
                $.Deferred(function( deferred ){
                    $( deferred.resolve );
                })
            ).done(function(){
                init_livetv(); // Creates and attaches to DOM the <video> element (Live TV player)
            });

            if (!document.documentElement.hasAttribute("data-turbolinks-preview")) {
                window.addEventListener('load', get_top_ads());
                if ($('body').width() >= 768) {
                    window.addEventListener('load', get_square_ad_template());
                }
            }

        }

        disconnect() {
            window.removeEventListener('scroll', paginate_live_tv);

            dispose_player_livetv(); // Dispose the VideoJS Player
        }
    });

    application.register("load_more_livetv", class extends Stimulus.Controller {

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
                    setTimeout(function () { fetch_live_tv_comments = true; }, 1000);
                });
            }
        }
    });
})();

function paginate_live_tv() {
    if ((window.innerHeight + window.scrollY) >= (document.body.offsetHeight - 500)) {
        if (fetch_live_tv_videos) {
            live_tv_num += 1;
            fetch_live_tv_videos = false;
            $.ajax({
                type: 'GET',
                url: "/page/live_tv_videos/" + topic + "/?page=" + String(live_tv_num),
            }).done(function (data) {
                $("#video-list").append(data);
                    if ($('body').width() <= 768 && (live_tv_num >= 5)) {
                        window.removeEventListener('scroll', paginate_live_tv);
                        $('#livetv_footer_section').css('display','block');
                        $('#video-list').append($('#video-list #livetv_footer_section'));
                    }
                fetch_live_tv_videos = true;
            });
        }
    }



    if (($('.header-custom').offset().top - $('.live-tv-header').offset().top) >= 0) {
        $(".live-head-section").addClass("sticky-head");
    }
    if (($('.header-custom').offset().top - $('.topics-section').offset().top) >= 0) {
//        $(".topics-section").addClass("sticky-topics");
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

function init_livetv() {
    /* Logic to initialize Live TV player */
    /* on connect() */

    let wrapper = $("#livetv-player");
    let video = $('<video></video>');

    video.addClass('video-js');
    video.addClass('vjs-theme-fantasy');
    video.attr('id', "livetv-page-video");
    wrapper.html("");
    video.appendTo(wrapper);

    if ($('body').width() > 768) {
        videojs('livetv-page-video', {
            autoplay: true,
            muted: true,
            controls: true,
            autoSetup: false,
            poster: "/app/static/img/argus_preview.png",
            preload: "metadata",
            sources: [{
                src: source,
                type: "application/x-mpegURL",

            }],
            width: "612",
            height: "344",  // dimension to match 16:9 aspect ratio
            options: { navigationUI: 'show' },
            type: "application/x-mpegURL",
            notSupportedMessage: "Your browser does not support video; please enable JavaScript"
        });
    } else {
        videojs('livetv-page-video', {
            autoplay: true,
            muted: true,
            controls: true,
            autoSetup: false,
            poster: "/app/static/img/argus_preview.png",
            preload: "metadata",
            sources: [{
                src: source,
                type: "application/x-mpegURL",

            }],
            width: "336",
            height: "217",
            options: { navigationUI: 'show' },
            type: "application/x-mpegURL",
            notSupportedMessage: "Your browser does not support video; please enable JavaScript"
        });
    }
}


function dispose_player_livetv() {

    /* Dispose the VideoJS player on exiting the page */
    /* on disconnect() */

    let player = videojs("livetv-page-video");
    if (player) {
        player.dispose();
    }
}