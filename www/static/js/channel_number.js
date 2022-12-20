
var topic_page_num = 1;
var fetch_topic_page_posts = true;
var topic_comments_page_num = 1;
var topic_fetch_comments = true;

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

    application.register("channelNumberController", class extends Stimulus.Controller {

        static get targets() {
            return ["live_id"]
        }

        connect() {
            channel_number()

            if (!document.documentElement.hasAttribute("data-turbolinks-preview")) {
                window.addEventListener('load', get_top_ads());
                if ($('body').width() >= 768) {
                    window.addEventListener('load', get_square_ad_template());
                }
            }

            let live_tv_icon_topic = document.getElementById("live_tv_icon_topic");

            var live_id = `${this.live_idTarget.value}`;

            $(".comments-overflow").scroll(function () {
                load_comments(live_id);
            });

            if ($('body').width() > 768) {
                $.when(
                $.getScript('https://d3pnd0n3snmitc.cloudfront.net/argus/video.min.js'),
                $.getScript( "https://d3pnd0n3snmitc.cloudfront.net/argus/videojs-ie8.min.js" ),
                $.Deferred(function( deferred ){
                    $( deferred.resolve );
                })
                ).done(function(){
                    init_trending_livetv(); // Creates and attaches to DOM the <video> element (Live TV player)
                });
            }

        }

        disconnect() {
            if ($('body').width() > 768) {
                dispose_player_trending(); // Dispose the VideoJS Player
            }
        }

    });

    application.register("load_more_trending", class extends Stimulus.Controller {

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
                    setTimeout(function () { topic_fetch_comments = true; }, 1000);
                });
            }
        }
    });
})();

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

function init_trending_livetv() {
    /* Logic to initialize Live TV player */
    /* on connect() */

    let wrapper = $("#trending-player");
    let video = $('<video></video>');

    video.addClass('video-js');
    video.addClass('vjs-theme-fantasy');
    video.attr('id', "trending-livetv-video");
    wrapper.html("");
    video.appendTo(wrapper);

    videojs('trending-livetv-video', {
        autoplay: false,
        muted: true,
        controls: true,
        autoSetup: false,
        disablePictureInPicture:true,
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
        notSupportedMessage: "Your browser does not support video; please enable JavaScript"
    });
    $(".vjs-picture-in-picture-control").addClass('d-none')
}

function dispose_player_trending() {

    /* Dispose the VideoJS player on exiting the page */
    /* on disconnect() */

    let player = videojs("trending-livetv-video");
    if (player) {
        player.dispose();
    }
}


function channel_number(){
          $("#myInput").on("keyup", function () {
          var value = $(this).val().toLowerCase();
          $("#myTable tr").filter(function () {
              $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
          });
      });
}