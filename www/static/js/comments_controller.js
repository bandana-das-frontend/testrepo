
(() => {
    const application = Stimulus.Application.start()
    application.register("comments", class extends Stimulus.Controller {

        static get targets() {
            return ["comment_text", "post", "truncated_comment", "show_comment", "type"]
        }

        expand() {
            this.truncated_commentTarget.classList.remove('truncated-comment')
            this.show_commentTarget.style.display = "none"
        }

        write_comment() {
            var text = `${this.comment_textTarget.value}`
            var post = `${this.postTarget.value}`
            var comment_type = `${this.typeTarget.value}`
            if (text == '') {

                /* need to specify what exactly needs to be done 
                from technical side to disable the comment when 
                it has empty text
                */

                return false;
            }
            else {
                $.ajax({
                    type: 'post',
                    url: '/add_comment',
                    data: { comment_text: text, post_id: post, comment_type: comment_type },
                    success: function () {
                        $("#comments-wrapper").load(location.href + " #comments-wrapper>*", "");
                    }
                });
            }
        }

        open_login_prompt() {
            $('#sign-in-phone-modal').appendTo("body");
            $('#sign-in-phone-modal').modal({
                backdrop: 'static',
            });
        }

        get text() {
            return this.comment_textTarget.value
        }

        get post() {
            return this.postTarget.value
        }

        open_mobile_comments() {
            $("header").css('z-index', 1);
            $('#comments-modal').appendTo("body");
            $('#comments-modal').modal({
                backdrop: 'static',
            });
        }

        write_comment_mobile() {
            var text = `${this.comment_textTarget.value}`;
            var post = `${this.postTarget.value}`;
            var comment_type = `${this.typeTarget.value}`;
            if (text == '') {
                /* need to specify what exactly needs to be done 
                from technical side to disable the comment when 
                it has empty text
                */

                return false;
            } else {
                $.ajax({
                    type: 'post',
                    url: '/add_comment',
                    data: { comment_text: text, post_id: post, comment_type: comment_type },
                    success: function (data) {
                        $('#comments-modal').modal('toggle');
                        location.reload();
                    }
                });
            }
        }
    });
})();
