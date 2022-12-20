var home_page_num = 1;
var comments_page_num = 1;
var live_tv_comments_num = 1;
var details_page_videos_num = 1;
var live_tv_num = 1;
var live_tv_comments_num = 1;
var post_comments_page_num = 1;
var details_page_num = 1;
var topic_page_num = 1;
var topic_comments_page_num = 1;
var search_string;
var searched_page_num = 1;
var footer_view_flag = false;

document.addEventListener('turbolinks:before-render', () => {
    $("#comments_post").off();
    $('input[name="search"]').off();

    if (home_page_num > 1) {
        home_page_num = 1;
    }
    if (comments_page_num > 1) {
        comments_page_num = 1;
    }
    if (live_tv_comments_num > 1) {
        live_tv_comments_num = 1;
    }
    if (details_page_videos_num > 1) {
        details_page_videos_num = 1;
    }
    if (live_tv_num > 1) {
        live_tv_num = 1;
    }
    if (live_tv_comments_num > 1) {
        live_tv_comments_num = 1;
    }
    if (post_comments_page_num > 1) {
        post_comments_page_num = 1;
    }
    if (details_page_num > 1) {
        details_page_num = 1;
    }
    if (topic_page_num > 1) {
        topic_page_num = 1;
    }
    if (topic_comments_page_num > 1) {
        topic_comments_page_num = 1;
    }
});

document.addEventListener('turbolinks:request-start', () => {
    $("#top-thin-line").addClass("d-none");
});

document.addEventListener('turbolinks:request-end', () => {
    $("#top-thin-line").removeClass("d-none");
});

document.addEventListener("turbolinks:load", function () {

    $('#footer_move_top').on('click', function () {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    });

    if ($('body').width() <= 768) {
        // md and smaller devices
        $(".main-wrapper").removeClass('container').addClass('container-fluid');
        $(".bottom-fade").addClass("d-none");
        $("#side-bar-btn").removeClass('d-none');
        $("#side-bar-mobile").removeClass('d-none');
        $(".non-mobile-brand-name").addClass("d-none");
        $(".mobile-brand-name").removeClass("d-none");


        slidup_download_prompt()
        $(".close-download-prompt").on('click', function () {
            $(".download-app-prompt").hide(1000);
            setTimeout(function () {
                $(".download-app-prompt").css("bottom", "-100px");
                $(".download-app-prompt").show();
                slidup_download_prompt()
            }, 15000);
        })

    }
    else {
        $(".main-wrapper").removeClass('container-fluid').addClass('container');
        $(".bottom-fade").removeClass("d-none");
        $("#side-bar-btn").addClass('d-none');
        $("#side-bar-mobile").addClass('d-none');
        $(".non-mobile-brand-name").removeClass("d-none");
        $(".mobile-brand-name").addClass('d-none');
        $('#desktop_base_footer').css('display', 'none')
        window.addEventListener('scroll', trigger_footer);
    }

    /* Below JS prevents margin-right: 15px to be added to body on Bootstrap modal open.
    This is a feature/bug in Bootstrap itself! */
    $(document.body).on('hide.bs.modal,hidden.bs.modal', function () {
        $('body').css('padding-right', '0');
    });

    $('input[name="search"]').keyup(function () {
        if (window.scrollY >= 53) {
            document.getElementById("search").value = document.getElementById("search-header").value;
        }
        else {
            document.getElementById("search-header").value = document.getElementById("search").value;
        }
    });


    //If the popup banner is clicked hide the banner and redirect to corresponding Url and set session var(contest_switch) to false
    $("#contest_banner").on('click', function () {
        $('#contest_popup_modal').modal('hide')
        sessionStorage.setItem("contest_switch", false);
    });

    //If the popup close btn is clicked hide the banner and set session var(contest_switch) to false
    $("#contest_close").on('click', function () {
        sessionStorage.setItem("contest_switch", false);
    });

    $('#subscribe_email').on('input', function () {
        if ($('#subscribe_email').val().length == 0) {
            $("#subscribe_btn").css('background', '#E3E3E3')
        } else {
            $("#subscribe_btn").css('background', '#E21E22')
        }
    });

    $('#subscribe_btn').off('click').on('click', function (e) {
        $('#newsletter_success_div').css('display', 'none');
        e.preventDefault();
        let email_address = $('#subscribe_email').val();
        // var email_address = `${this.emailTarget.value}`
        if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email_address)) {
            let data = {
                "email": email_address
            }
            $.ajax({
                type: 'POST',
                url: "/save_subscriber_email/",
                data: data
            }).done(function (data) {
                if (data.status === "PASS") {
                    $("#newsletter_mail_div").css("display", "none");
                    $("#newsletter_success_div").css("display", "block");
                }
            });
        } else {
            $('#email_validation_err').css('display', 'flex');
        }
    })

    $(document).ready(function () {
        $('.carousel').carousel({
            interval: 3000
        })
    });


});

document.addEventListener('turbolinks:render', () => {
});

function slidup_download_prompt() {
    setTimeout(function () {
        $('.download-app-prompt').animate({bottom: 12});
    }, 5000);
}

function trigger_footer() {
    if ($(this).scrollTop() >= 2000 && (!footer_view_flag)) {     // This is window object
        $('#desktop_base_footer').css('display', 'block');
        $('#desktop_base_footer').animate({bottom: 0}, {duration: 400, easing: "swing",});
        $('#footer_move_top').css('display','block')
        footer_view_flag = true
    } else if ($(this).scrollTop() < 2000 && footer_view_flag) {
        $('#desktop_base_footer').animate({bottom: -200,}, {duration: 400, easing: "swing",});
        $('#footer_move_top').css('display','none')
        footer_view_flag = false
    }
}


function update_ad_clicks(ad_id) {
    if (ad_id) {
        let data = {
            "ad_id": ad_id
        }
        $.ajax({
            type: 'POST',
            url: "/update_ad_click/",
            data: data
        }).done(function (data) {

        });
    }
}


function get_top_ads() {
    $.ajax({
        type: 'GET',
        url: '/get_top_ads',
        data: {
        },
        success: function (response) {
               $(".top-ads-container").html(response);
               $('.carousel').carousel({interval:3000})

        }
    });
}




function get_square_ad_template() {
        $.ajax({
                type: 'GET',
                url: '/get_square_ad/',
                dataType: "html",
                success: function (response) {
                    $(".desktop-square-ad").html(response)
                    $('.carousel').carousel({interval:3000})
                }
            });
}


function get_main_ad(div_id){
        $.ajax({
            async:false,
            type: 'POST',
            url: '/get_main_ad',
            success: function (response) {
                console.log(response['id'], 'coming')
                create_main_ad_image_element(response,div_id)
            }
        });
}


async function create_main_ad_image_element(response,div_id) {
    if (response['id'] != undefined) {
        const div = document.createElement(`div`);
        div.className = `main-ads`;
        // div.onclick = 'update_ad_clicks('+response['id']+')'
        div.setAttribute("onclick",'update_ad_clicks('+response['id']+')')

        const a = document.createElement(`a`);
        a.target = `_blank`;
        a.href = response['ad_link']

        const img = document.createElement(`img`);
        img.src = response['ad_image']

        a.append(img)
        div.append(a)

        // adding ad to respective position
        $("#" + div_id).empty().append(div)
    }
}


$(window).on('load', function() {

        // If contest popup is not shown, get the contest popup data if it is activated and show them once per session
    if (String(sessionStorage.getItem("contest_switch")) != "false") {
        $.ajax({
            type: 'POST',
            url: "/get_contest_popup_data",
        }).done(function (data) {
            if (data.status == 'PASS') {
                $("#contest_banner").attr('src', data.popup_img)
                if (data.popup_url.trim() !== '') {
                    $("#contest_banner_link").attr('href', data.popup_url)
                }
                $('#contest_popup_modal').modal({
                    backdrop: 'static',
                });
                $('#contest_popup_modal').appendTo("body");
            }
        });
    }


})