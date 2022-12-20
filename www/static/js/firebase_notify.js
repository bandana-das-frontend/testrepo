
// Initialize
document.addEventListener('turbolinks:before-render', () => {
})

document.addEventListener("turbolinks:load", function () {
    if (Notification.permission !== "granted" & Notification.permission !== "denied") {
        if (sessionStorage.getItem("web_notify_flag") === null) {
            setTimeout(function () {
                $("#notify-permission-div").addClass("notify_animate_slide");
            }, 25000);
        }
    }

//if allow btn is clicked show native notification prompt

    $("#allow_notify").on('click', function () {
        $("#notify-permission-div").addClass("remove_notify_animate_slide");
        $("#notify-permission-div").removeClass("notify_animate_slide");
        sessionStorage.setItem("web_notify_flag", "granted")
        showdefaultNotifyPopup()
    })

//if not now btn is clicked show nothing
    $("#block_notify").on('click', function () {
        $("#notify-permission-div").addClass("remove_notify_animate_slide");
        $("#notify-permission-div").removeClass("notify_animate_slide");
        sessionStorage.setItem("web_notify_flag", "denied")
    })

});



firebase.initializeApp(firebaseConfig);
var messaging = firebase.messaging();

// if serviceWorkers are supported in the browser, register firebase-messaging-sw.js service worker

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/firebase-messaging-sw.js').then(function (registration) {
        // registration worked
        messaging.useServiceWorker(registration);
    }).catch(function (error) {
        // registration failed
    });
}


function showdefaultNotifyPopup() {
    if (!("Notification" in window)) {
        console.log("This browser does not support system notifications");
    } else if (Notification.permission === "granted") {
    } else if (Notification.permission !== 'denied') {
        if (String(sessionStorage.getItem("web_notify_flag")) == "granted")
            askpermission();
    }
}


// ask for "send notification" permission, if granted get token and send it to server.
function askpermission() {
    Notification.requestPermission(function (permission) {
        if (permission === "granted") {
            messaging.getToken({vapidKey: vapidKey}).then((currentToken) => {
                if (currentToken) {
                    url_path = "/save_browser_notification_token"
                    const client = new ClientJS();
                    system_fingerprint = client.getFingerprint()
                    let notif_data = {"currentToken": currentToken, "system_fingerprint": system_fingerprint}
                    $.ajax({
                        type: 'post',
                        url: url_path,
                        data: notif_data,
                    }).done(function (data) {
                    });

                }
            }).catch((err) => {
            });
        }
    });
}
