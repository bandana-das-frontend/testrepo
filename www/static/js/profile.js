document.addEventListener('turbolinks:before-render', () => {
    $("#comments_home").off();
    $("#comments_post").off();
    $("#video-list").off();
    $("#comments_live_tv").off();
    $('#write-comment').off();

    $("#live_tv_icon_topic").css("display", "none");
});

document.addEventListener("turbolinks:load", function () {

});


(() => {
    const application = Stimulus.Application.start()

    application.register("profileMenuController", class extends Stimulus.Controller {

        static get targets() {
            return []
        }

        connect() {
            $(".profile-menu-item").click(function(){
                $(".profile-menu-item").removeClass("active");
                $(".profile-menu-selected").addClass("d-none");
                $(this).addClass("active");
                $(this).children('.profile-menu-selected').removeClass('d-none');
            });
        }

        disconnect() {
        }

        userActivities() {
            $.ajax({
                type: 'GET',
                url: '/get_activities',
                success: function (data) {
                    $("#user-info-section").load('/get_activities #user-info-section');
                }
            });

        }

         userSavedStories() {
            $.ajax({
                type: 'GET',
                url: '/get_saved_stories',
                success: function (data) {
                    $("#user-info-section").load('/get_saved_stories #user-info-section');
                }
            });

        }

    });
})();