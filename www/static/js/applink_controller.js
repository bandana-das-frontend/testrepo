(() => {
    const application = Stimulus.Application.start()
    application.register("applink", class extends Stimulus.Controller {

        static get targets() {
            return ["wrapper",]
        }

        close() {
            this.wrapperTarget.classList.add("d-none");
        }

        open_app_link() {
            window.open("https://play.google.com/store/apps/details?id=com.glynk.theargus");
        }
    });
})();
