(() => {
    const application = Stimulus.Application.start()
    application.register("liveUpdateController", class extends Stimulus.Controller {

        static get targets() {
        }

        connect() {
            if (!document.documentElement.hasAttribute("data-turbolinks-preview")) {
                window.addEventListener('load', get_top_ads());
                if ($('body').width() >= 768) {
                    window.addEventListener('load', get_square_ad_template());
                }
            }
        }

        disconnect() {
        }

    });
})();




