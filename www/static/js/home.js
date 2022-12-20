var home_page_num = 1;
var fetch_home_page_posts = true;
var comments_page_num = 1;
var fetch_comments = true;
var isPiP = true;
var isPiPclosed = false

document.addEventListener('turbolinks:before-render', () => {
    $("#comments_home").off();
    $("#comments_post").off();
    $("#video-list").off();
    $("#comments_live_tv").off();
    $('#write-comment').off();
    $(".comments-overflow").off();

    if ($('body').width() <= 768) {
        $("#live_tv_icon_mob").css("display", "none");
    } else {
        $("#live_tv_icon_home").css("display", "none");
    }
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

    if ($('body').width() <= 768) {
        $("#live_tv_icon_mob").css("display", "block");
    } else {
        $("#live_tv_icon_home").css("display", "block");
    }

});


(() => {
    const application = Stimulus.Application.start()

    application.register("homeController", class extends Stimulus.Controller {

        static get targets() {
            return ["live_id", "subscribeEmail"]
        }

        connect() {
            window.addEventListener('scroll', paginate_home_posts);
            $("#home_read_more").click(function () {
                paginate_home_posts()
            })

            if (!document.documentElement.hasAttribute("data-turbolinks-preview")) {
                window.addEventListener('load', get_top_ads());
                if ($('body').width() >= 768) {
                    window.addEventListener('load', get_square_ad_template());
                }
            }

            var live_id = `${this.live_idTarget.value}`;
            const isMobile = window.matchMedia("only screen and (max-width: 760px)").matches;
            if (!isMobile) {
                $(".comments-overflow-home").scroll(function () {
                    load_comments(live_id);
                });

                $.when(
                $.getScript('https://d3pnd0n3snmitc.cloudfront.net/argus/video.min.js'),
                $.getScript( "https://d3pnd0n3snmitc.cloudfront.net/argus/videojs-ie8.min.js" ),
                $.Deferred(function( deferred ){
                    $( deferred.resolve );
                })
                ).done(function(){
                    init_home_livetv(); // Creates and attaches to DOM the <video> element (Live TV player)
                    init_home_mini_player(); // Mini player logic for low resolution devices
                });

                $("#home_live_close_icon").click(function () {
                    isPiPclosed = true
                    $("#home-video").css("position", "relative");
                    $("#home_live_close_icon").css("display", "none");
                })
            }

        }

        disconnect() {
            window.removeEventListener('scroll', paginate_home_posts);
            if ($('body').width() > 768) {
                dispose_player_home(); // Dispose the VideoJS Player
                $("#home-video").css("position", "fixed");
                isPiPclosed = false
            }

        }
    });

    application.register("load_more_home", class extends Stimulus.Controller {

        static get targets() {
            return ["live_id", "totalComments"]
        }

        load_home_comments() {
            var live_id = `${this.live_idTarget.value}`
            var total = `${this.totalCommentsTarget.value}`

            if ((comments_page_num + 1) * 5 >= total) {
                document.getElementById('load-more-button').style.display = "none";
            }

            if (fetch_comments) {
                comments_page_num += 1;
                fetch_comments = false;
                $.ajax({
                    type: 'GET',
                    url: "/page/live_tv_home/comments/?post_id=" + live_id + "&page=" + String(comments_page_num),
                }).done(function (data) {
                    $("#comments-card").append(data);
                    setTimeout(function () { fetch_comments = true; }, 1000);
                });
            }
        }
    });
})();

function paginate_home_posts() {
        if ((window.innerHeight + window.scrollY) >= (document.body.offsetHeight - 3000)) {
            if (fetch_home_page_posts) {
                home_page_num += 1;
                fetch_home_page_posts = false;
                $.ajax({
                    type: 'GET',
                    url: "/page/home_posts?page=" + String(home_page_num),
                }).done(function (data) {
                    $("#home-posts").append(data);
                    if ($('body').width() <= 768 && (home_page_num >= 5)) {
                        window.removeEventListener('scroll', paginate_home_posts);
                        $('#home_footer_section').css('display', 'block');
                        $('#home-posts').append($('#home-posts #home_footer_section'));
                    }
                    fetch_home_page_posts = true;
                });
            }
        }
    if ($('body').width() > 768) {
        init_home_mini_player(); // Mini player logic on scroll
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
    if (($(".comments-overflow-home").height() + $(".comments-overflow-home").scrollTop()) >= (document.body.offsetHeight - 5000)) {
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

function init_home_livetv() {
    /* Logic to initialize Live TV player */
    /* on connect() */

    let wrapper = $("#home-player");
    let video = $('<video></video>');

    video.addClass('video-js');
    video.addClass('vjs-theme-fantasy');
    video.attr('id', "home-livetv-video");
    wrapper.html("");
    video.appendTo(wrapper);

    videojs('home-livetv-video', {
        autoplay: false,
        muted: true,
        disablePictureInPicture:true,
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
        notSupportedMessage: "Your browser does not support video; please enable JavaScript"
    });

    $(".vjs-picture-in-picture-control").addClass('d-none')
}

function init_home_mini_player() {

    /* Method to get Live TV player into mini player */
    /* for low resolution devices */

    let top_of_element = $("#home-video-wrapper").offset().top;
    let bottom_of_screen = $(window).scrollTop() + $(window).innerHeight();
    let video_home = document.getElementById('home-video');

    if ((bottom_of_screen > (top_of_element + $("#home-video-wrapper").outerHeight())) || isPiPclosed) {
        isPiP = false;
    } else {
        isPiP = true;
    }


    if (isPiP) {
        $("#home_live_close_icon").css("display", "flex")
        $("#home_live_close_icon").css("position", "absolute")
        $("#home_live_close_icon").css("z-index", "100")
        $("#home_live_close_icon").css("right", "8px");
        $("#home_live_close_icon").css("top", "8px");
        $(video_home).css("position", "fixed");
        $(video_home).css("right", "0");
        $(video_home).css("bottom", "0");
        $(video_home).css("width", "295px");
        $(video_home).css("height", "166px");
        $(video_home).css("z-index", "2");
    } else {
        $("#home_live_close_icon").css("display", "none")
        $(video_home).css("position", "relative");
    }
}

function dispose_player_home() {

    /* Dispose the VideoJS player on exiting the page */
    /* on disconnect() */

    let player = videojs("home-livetv-video");
    if (player) {
        player.dispose();
    }
}

// function is used to count lines in breaking news  div in desktop
// we have other div with id = desk-bn-hidden which is hidden , we are calculating line from it than changing fontsize according to it.
// to get lines accurate so used another hidden breking news div
function countLines() {
    var el = document.getElementById('desk-bn-hidden');

    if (el != null || undefined) {
        var divHeight = el.offsetHeight
        var lines = divHeight / 34;
        if (lines < 3) {
            $('#desk-bn').css({'font-size': '26px', 'line-height': '36px'})
        } else if (lines == 3) {
            $('#desk-bn').css({'font-size': '22px', 'line-height': '28px'})
        } else if (lines > 3) {
            $('#desk-bn').css({'font-size': '20px', 'line-height': '24px'})
        }
    }

}