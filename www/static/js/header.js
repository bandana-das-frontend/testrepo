document.addEventListener('turbolinks:before-render', () => {
    window.removeEventListener('scroll', () => { });
    $("#comments_home").off();
    $("#comments_post").off();
    $("#video-list").off();
    $("#comments_live_tv").off();
    $("#phone_number").off();
    $("#otp").off();
    $("#fname").off();
    $("#sign-in-btn").off();
    $("#login-with-phone").off();
    $("#phone-modal-back-icon").off();
    $("#phone-modal-back-text").off();
    $("#log-out-btn").off();
    $("#change_phone_number").off();
    $("#resend_otp").off();
    $("#enter-btn").off();
    $("#brand-logo-sec-wrapper").off();
    $("#logo-dropdown").off();
});

document.addEventListener("turbolinks:load", function () {

    if ($('body').width() <= 768) {
        $("#log-out-section").addClass("d-none");
        $("#sign-in-btn").addClass("d-none");

        $("#brand-logo-sec-wrapper").on('click', function () {
            $('#side-bar-mobile').appendTo("body");
            $('#side-bar-mobile').modal('toggle');
        });

        $("#logo-dropdown").on('click', function () {
            $('#side-bar-mobile').appendTo("body");
            $('#side-bar-mobile').modal('toggle');
        });

        init_mobile_header_scroll();

        // Show search bar and hide header after clicking search icon in mobile web
        $("#search-icon-mob").on('click', function () {
            $("#mob-search-section").show();
            $("#search-result-div").css("filter", "blur(4px)");
            $("#mob-header").hide();
            $("#mob-search-input").val(search_string);

        });
        // hide search bar and show header after clicking  back search icon in mobile web
        $("#search-back-mob").on('click', function () {
            $("#mob-search-section").hide();
            $("#search-result-div").css("filter", "none");
            $("#mob-header").show();
        });

        // If the search input is not blank visit the article search api in mobile web
        $("#mob-search-addon").on('click', function () {
            let inputString = $("#mob-search-input").val();
            inputString = inputString.replace(/[@:&\/\\+~%!|?]/g, '')
            inputString = inputString.trim();
            if (inputString.length > 0) {
                search_string = inputString;
                searched_page_num = 1;
                Turbolinks.visit("/search-articles?search_string=" + encodeURIComponent(inputString));
            }
        });

        // if user press enter btn and If the search input is not blank visit the article search api in mobile web
        $(document).on('keypress', function (e) {
            if ($("#mob-search-section").css("display") != "none") {
                let inputString = $("#mob-search-input").val();
                inputString = inputString.replace(/[@:&\/\\+~%!|?]/g, '')
                inputString = inputString.trim();
                if (e.which == 13 && inputString != "undefined" && inputString.length > 0 && $("#mob-search-input").is(':focus')) {
                    search_string = inputString
                    searched_page_num = 1;
                    Turbolinks.visit("/search-articles?search_string=" + encodeURIComponent(inputString));
                }
            }
        });


        // Place the red bottom border based on the selected language after clicking the language in mobile web
        $('.lang_opt').each(function () {
            $(this).on('click', function () {
                if (this.textContent == "En" & $('#selected_lang').attr('data-lang') !== "English") {
                    $('#lang_options li.active_lang').removeClass("active_lang");
                    this.classList.add('active_lang');
                    $("#lang_border").css("left", '0%');
                } else if (this.textContent != "En" & $('#selected_lang').attr('data-lang') == "English") {
                    $('#lang_options li.active_lang').removeClass("active_lang");
                    this.classList.add('active_lang');
                    $("#lang_border").css("left", '44%');
                }
            })
        })

    } else {
        $("#brand-logo-sec-wrapper").off();
        $("#logo-dropdown").off();

        $("#search-icon").on('click', function () {
            $("#search-section").toggle(500, function () {
                if ($("#search-section").css("display") == "none") {
                    $(".sticky-topics").css("top","130px");
                    $("#main-container").css("top", "130px");
                    $(".desktop-top-ad").css("top", "130px");
                } else {
                    $(".sticky-topics").css("top","185px");
                    $("#main-container").css("top", "180px");
                    $(".desktop-top-ad").css("top", "180px");
                }
            });
        });

        $("#close_search_bar").on('click', function () {
            $(".sticky-topics").css("top","130px");
            $("#search-section").hide(500)
            $("#main-container").css("top", "130px");
            $(".desktop-top-ad").css("top", "130px");
        });


        // If the search input is not blank visit the article search api in mobile web
        $("#search-addon").on('click', function () {
            let inputString = $("#search-input").val();
            inputString = inputString.replace(/[@:&\/\\+~%!|?]/g, '')
            inputString = inputString.trim();
            if (inputString.length > 0) {
                search_string = inputString
                searched_page_num = 1;
                Turbolinks.visit("/search-articles?search_string=" + encodeURIComponent(inputString));
            }
        });

        // if user press enter btn and If the search input is not blank visit the article search api in desktop web
        $(document).on('keypress', function (e) {
            if ($("#search-section").css("display") != "none") {
                let inputString = $("#search-input").val();
                inputString = inputString.replace(/[@:&\/\\+~%!|?]/g, '')
                inputString = inputString.trim();
                if (e.which == 13 && inputString != "undefined" && inputString.length > 0 && $("#search-input").is(':focus')) {
                    search_string = inputString
                    searched_page_num = 1;
                    Turbolinks.visit("/search-articles?search_string=" + encodeURIComponent(inputString));
                }
            }
        });

         // Place the red bottom border based on the selected language after clicking the language in mobile web
        $('.lang_opt').each(function () {
            $(this).on('click', function () {
                if (this.textContent == "English" & $('#selected_lang').attr('data-lang') !== "English") {
                    $('#lang_options li.active_lang').removeClass("active_lang");
                    this.classList.add('active_lang');
                    $("#lang_border").css("left", '0%');
                    $("#lang_border").css("width", '50px');
                } else if (this.textContent != "English" & $('#selected_lang').attr('data-lang') == "English") {
                    $('#lang_options li.active_lang').removeClass("active_lang");
                    this.classList.add('active_lang');
                    $("#lang_border").css("width", '35px');
                    $("#lang_border").css("left", '40%');
                }
            })
        })
    }

    // ToDo: Un comment this later

    // $("#sign-in-btn").on('click', function () {
    //     $("#phone_number").val('');
    //     $("#otp").val('');
    //     $("#otp-section-wrapper").addClass("visibility-hidden");

    //     /* wherever you see Bootstarp Modal opened using .appendTo("body");
    //         This is to keep position: fixed; for header to keep working */

    //     $('#sign-in-first-modal').appendTo("body");
    //     $('#sign-in-first-modal').modal({
    //         backdrop: 'static',
    //     });
    // });

    // $("#login-with-phone").on('click', function () {
    // $('#close-first-modal').trigger('click');

    $("#sign-in-btn").on('click', function () {
         $.ajax({
             url: "https://ipapi.co/json",
                success: function (data, text) {
                if (data.country_code != 'IN'){
                    openEmailLogin()
                }
                else{
                    openPhoneLogin()
                }
                },
                error: function (request, status, error) {
                    openPhoneLogin()
                }
         });
    });

    $("#phone-modal-back-icon, #phone-modal-back-text").on('click', function () {
        $("#phone_number").val('');
        $("#otp").val('');
        $("#close-phone-modal").trigger('click');
        $('#sign-in-first-modal').appendTo("body");
        $('#sign-in-first-modal').modal({
            backdrop: 'static',
        });
    });


    $("#log-out-btn").on('click', function () {
        $.ajax({
            url: "/logout",
        }).done(function (data) {
            $("#sign-in-btn").removeClass("d-none");
            $("#log-out-section").addClass("d-none");

            $('#logout-modal').appendTo("body");
            $('#logout-modal').modal({
                backdrop: 'static',
            });

            setTimeout(function () {
                $('#logout-modal').modal('hide');
            }, 2000);
            location.reload();
        });
    });

    $("#change_phone_number").on('click', function () {
        $("#otp-section-wrapper").addClass("visibility-hidden");
        $("#phone_number").val('');
        $("#phone_number").focus();
        let submit_btn = $("#submit-phone");
        submit_btn.removeClass("disabled-btn").addClass("enabled-btn");
        submit_btn.prop("onclick", null).off("click");
    });

    $("#resend_otp").on('click', function () {
        submit_phone_number();
    });


    $("#change_email").on('click', function () {
        $("#email-otp-section-wrapper").addClass("visibility-hidden");
        $("#user-email").val('');
        $("#user-email").focus();
    });

    $("#resend_email_otp").on('click', function () {
        submit_email();
    });



    /*** Validations ***/
    // Phone number
    $("#phone_number").bind('keyup keypress paste', function (e) {
        let val = e.target.value; //total value
        let character = String.fromCharCode(e.which); //Which character was typed

        // Length check
        if (val.length >= 10) {
            e.preventDefault();
        }

        // Digit only check for character typed
        let reg = /^\d+$/;
        if (!reg.test(character)) {
            e.preventDefault();
        }

        let phone_error = $("#phone-error");
        if (val.length >= 1) {
            phone_error.html('&nbsp');
            phone_error.addClass('visibility-hidden');
        } else {
            phone_error.val('Phone Number is required.');
            phone_error.removeClass('visibility-hidden');
        }

        // Enable/Disable Submit button logic
        let submit_btn = $("#submit-phone");
        if (val.length === 10) {
            submit_btn.removeClass("disabled-btn").addClass("enabled-btn");
            submit_btn.on('click', function () { submit_phone_number() });
        } else {
            submit_btn.removeClass("enabled-btn").addClass("disabled-btn");
            submit_btn.prop("onclick", null).off("click");
        }
    });


    $("#user-email").bind('keyup keypress paste', function (e) {
     $("#user-email-error").addClass("visibility-hidden")
      let user_email = e.target.value; //total value
      if (validateEmail(user_email) == true){
      $(".submit-email").addClass('active-button')
       $(".submit-email").removeAttr("disabled")

//      $(".submit-email").on('click', function () { submit_email() });
      }
      else{
         $(".submit-email").removeClass('active-button')
           $(".submit-email").prop("disabled", true)
//        $(".submit-email").prop("onclick", null).off("click");
      }
    });


    // OTP validation
    $("#otp").bind('keyup keypress paste', function (e) {
        let val = e.target.value; //total value
        let character = String.fromCharCode(e.which); //Which character was typed

        // Digit only check for character typed
        let reg = /^\d+$/;
        if (!reg.test(character)) {
            e.preventDefault();
        }

        let otp_error = $("#otp-error");
        if (val.length >= 1) {
            otp_error.html('&nbsp');
            otp_error.addClass('visibility-hidden');
        } else {
            otp_error.val('OTP is required.');
            otp_error.removeClass('visibility-hidden');
        }

        let submit_phone_otp = $("#submit-phone-otp");
        if (val.length >= 6) {
            submit_phone_otp.removeClass("disabled-btn").addClass("enabled-btn");
            submit_phone_otp.on('click', function () { submit_otp_phone() });
        } else {
            submit_phone_otp.removeClass("enabled-btn").addClass("disabled-btn");
            submit_phone_otp.prop("onclick", null).off("click");
        }
    });


     // OTP validation
    $("#email-otp").bind('keyup keypress paste', function (e) {
        let val = e.target.value; //total value
        let character = String.fromCharCode(e.which); //Which character was typed

        $("#email-otp-error").empty().append('')
        $("#email-otp-error").addClass('visibility-hidden');

        // Digit only check for character typed
        let reg = /^\d+$/;
        if (!reg.test(character)) {
//            e.preventDefault();
        }

        let otp_error = $("#otp-error");
        if (val.length >= 1) {
            otp_error.html('&nbsp');
            otp_error.addClass('visibility-hidden');
        } else {
            otp_error.val('OTP is required.');
            otp_error.removeClass('visibility-hidden');
        }

        let submit_email_otp = $("#submit-email-otp");
        if (val.length >= 6) {
            submit_email_otp.removeClass("disabled-btn").addClass("enabled-btn");
            submit_email_otp.on('click', function () { submit_otp_email() });
        } else {
            submit_email_otp.removeClass("enabled-btn").addClass("disabled-btn");
            submit_email_otp.prop("onclick", null).off("click");
        }
    });

    $("#enter-btn").on('click', function () {
        let first_name = $("#fname").val().length === 0;
        let gender = $('input[name="gender"]:checked').length === 0;

        if (gender) {
            $("#gender-error").html('&nbsp;');
            $("#gender-error").removeClass("visibility-hidden");
            $("#gender-error").text("Gender is required.");
        }

        if (first_name) {
            $("#name-error").html('&nbsp;');
            $("#name-error").removeClass("visibility-hidden");
            $("#name-error").text("Name is required.");
        }

        if (!gender && !first_name) {
            data = {
                "first_name": $("#fname").val(),
                "last_name": $("#lname").val(),
                "gender": $('input[name="gender"]:checked').val()
            }
            $.ajax({
                type: 'POST',
                url: '/update_user_name_gender',
                data: data
            }).done(function (data) {
                $('#user-details-modal').modal('hide');
                $("#sign-in-btn").addClass("d-none");
                $("#log-out-section").removeClass("d-none");
                window.location.href = '/';
            });
        }
    });

    $("#fname").bind('keyup keypress paste', function (e) {
        let val = e.target.value; //total value
        let character = String.fromCharCode(e.which); //Which character was typed

        // Don't allow spaces
        if (character == " ") {
            e.preventDefault();
        }

        // show/hide error message logic
        let name_error = $("#name-error");
        if (String(val).trim().length > 0) {
            name_error.html('&nbsp;');
            name_error.addClass("visibility-hidden");
        } else {
            name_error.html('&nbsp;');
            name_error.removeClass("visibility-hidden");
            name_error.text("Name is required.");
        }
    });

    $('input[type=radio][name=gender]').change(function () {
        $("#gender-error").html('&nbsp;');
        $("#gender-error").addClass("visibility-hidden");
    });

    /*** End of Validations ***/
}); // End of Turbolinks on load


/* Helper Functions */

function submit_phone_number() {
    let submit_btn = $("#submit-phone");

    /* Make phone number submit button disabled 
    on click (as per design) */
    submit_btn.removeClass("enabled-btn").addClass("disabled-btn");
    submit_btn.prop("onclick", null).off("click");

    let data = {
        "phone_number": $("#phone_number").val(),
        "country_code": "+91"
    }

    $.ajax({
        type: 'POST',
        url: "/send_otp_to_phone_number",
        data: data
    }).done(function (data) {
        if (data.status === "PASS") {
            $("#otp-section-wrapper").removeClass("visibility-hidden");
            $("#otp").focus();
        } else {
            $("#phone-error").val('Sorry, try again.');
            submit_btn.removeClass("disabled-btn").addClass("enabled-btn");
            submit_btn.on('click', function () { submit_phone_number() });
        }
    });
}




function submit_email() {
    let submit_btn = $("#submit-email");

    /* Make phone number submit button disabled
    on click (as per design) */
    submit_btn.removeClass('active-button')
    submit_btn.prop("disabled", true)


    let data = {
        "email": $("#user-email").val(),
        "community_code": "THEARGUS"
    }

    $.ajax({
        type: 'POST',
        url: "/send_otp_to_email",
        data: data
    }).done(function (data) {
        if (data.status === "PASS") {
            $("#email-otp-section-wrapper").removeClass("visibility-hidden");
            $("#otp").focus();
        } else {
            $("#user-email-error").val('Sorry, try again.');
            submit_btn.removeClass("disabled-btn").addClass("enabled-btn");
            submit_btn.on('click', function () { submit_otp_email() });
        }
    }).fail(function (jqXHR, textStatus) {
            $("#user-email-error").removeClass("visibility-hidden")
            $("#user-email-error").empty().append('Sorry, try again.');
            submit_btn.removeClass("disabled-btn").addClass("enabled-btn");
            submit_btn.on('click', function () { submit_otp_email() });

});
}



function submit_otp_phone() {
    let submit_phone_otp = $("#submit-phone-otp");

    /* Make phone number submit button disabled 
    on click (as per design) */
    submit_phone_otp.removeClass("enabled-btn").addClass("disabled-btn");
    submit_phone_otp.prop("onclick", null).off("click");

    let otp_error = $("#otp-error");
    otp_error.html('&nbsp');
    otp_error.addClass('visibility-hidden');

    let data = {
        "phone_number": $("#phone_number").val(),
        "otp": $("#otp").val()
    }
    $.ajax({
        type: 'POST',
        url: "/verify_phone_number_otp",
        data: data
    }).done(function (resp) {
        if (resp.status === "PASS") {
            let access_token = String(resp.access_token);
            let data_to_pass = {
                "access_token": access_token,
                "country_code": "+91",
                "backend_type": "CUSTOM_SMS",
                "phone_number": $("#phone_number").val()
            }
            $.ajax({
                type: 'POST',
                url: "/signup_with_token",
                data: data_to_pass
            }).done(function (obj) {
                if (obj.status === "PASS") {
                    let user = obj.user;
                    if (user.first_name && user.gender) {
                        $("#close-user-modal").removeClass("d-none");
                        $("#sign-in-btn").addClass("d-none");
                        $("#log-out-section").removeClass("d-none");
                        $("#close-phone-modal").trigger('click');
                        window.location.href = '/';
                    } else {
                        $("#close-user-modal").addClass("d-none");
                        $("#close-phone-modal").trigger('click');

                        $('#user-details-modal').appendTo("body");
                        $('#user-details-modal').modal({
                            backdrop: 'static',
                        });
                    }
                } else {
                    $("#otp").val('');
                    $("#otp-error").val('Sorry, try again.');
                    submit_phone_otp.removeClass("disabled-btn").addClass("enabled-btn");
                    submit_phone_otp.on('click', function () { submit_otp_phone() });
                }
            });
        } else {
            $("#otp").val('');
            $("#otp-error").val('Sorry, try again.');
            submit_phone_otp.removeClass("disabled-btn").addClass("enabled-btn");
            submit_phone_otp.on('click', function () { submit_otp_phone() });
        }
    });
}

function init_mobile_header_scroll() {
    var lastScrollTop = 0, delta = 5;
    $(window).scroll(function () {
        var nowScrollTop = $(this).scrollTop();
        if (Math.abs(lastScrollTop - nowScrollTop) >= delta) {
            if (nowScrollTop > lastScrollTop) {
                $("#header-mob-main").removeClass("pos-sticky-main-header").fadeIn("slow");;
                $("#header-mob-sub").removeClass("pos-sticky-sub-header").fadeIn("slow");;
            } else {
                $("#header-mob-main").addClass("pos-sticky-main-header").fadeIn("slow");;
                $("#header-mob-sub").addClass("pos-sticky-sub-header").fadeIn("slow");;
            }
            lastScrollTop = nowScrollTop;
        }
    });
}

function submit_otp_email(){

     let submit_email_otp = $("#submit-email-otp");

    /* Make phone number submit button disabled
    on click (as per design) */
    submit_email_otp.removeClass("enabled-btn").addClass("disabled-btn");
    submit_email_otp.prop("onclick", null).off("click");

    let otp_error = $("#otp-error");
    otp_error.html('&nbsp');
    otp_error.addClass('visibility-hidden');

        let data = {
            "email": $("#user-email").val(),
            "otp":$("#email-otp").val()
        }

        $.ajax({
            type: 'POST',
            url: "/verify_email_otp/",
            data: data
        }).done(function (resp) {
                let access_token = String(resp.access_token);
                let data_to_pass = {
                    "access_token": access_token,
                    "backend_type": "CUSTOM_EMAIL",
                    "email": $("#user-email").val().trim(),

                }
                if(resp.status === "PASS"){
                                      $.ajax({
                    type: 'POST',
                    url: "/signup_with_token/",
                    data: data_to_pass
                }).done(function (obj) {
                    if (obj.status === "PASS") {
                        let user = obj.user;
                        if (user.first_name && user.gender) {
                            $("#close-user-modal").removeClass("d-none");
                            $("#sign-in-btn").addClass("d-none");
                            $("#log-out-section").removeClass("d-none");
                            $("#close-email-modal").trigger('click');
                            window.location.reload()
                        } else {
                            $("#close-user-modal").addClass("d-none");
                            $("#close-email-modal").trigger('click');

                            $('#user-details-modal').appendTo("body");
                            $('#user-details-modal').modal({
                                backdrop: 'static',
                            });
                        }
                    } else {
                        $("#otp").val('');
                        $("#email-otp-error").val('Sorry, try again.');
                        submit_email_otp.removeClass("disabled-btn").addClass("enabled-btn");
                        submit_email_otp.on('click', function () { submit_otp_email() });
                    }
                })
                }
                else{
                    $("#email-otp-error").empty().append('The OTP you entered is incorrect')
                    $("#email-otp-error").removeClass('visibility-hidden');
                }
        })
}

function validateEmailOtp() {
    let submit_email_otp = $("#submit-email-otp");
    let val = $('.otp-value').map((_,el) => el.value).get().join("")
    // Digit only check for otp typed
    let reg = /^\d+$/;

    // check for digits-only
    if (reg.test(val)) {
        // check for otp length
        if (val.length == 6) {
            return true
        }
        else {
            return false;
        }
    }
    else {
        return false
    }
}


function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function openPhoneLogin(){
      $('#sign-in-phone-modal').appendTo("body");
      $('#sign-in-phone-modal').modal({
            backdrop: 'static',
        });
}

function openEmailLogin(){
      $('#sign-in-email-modal').appendTo("body");
      $('#sign-in-email-modal').modal({
            backdrop: 'static',
        });
}
