// below two variables help in dynamic card flip for multiple widgets
let topCard = 1;
let facingUp = true;

$(document).ready(function () {
    /*
        custom_widget_bg is used in js to set background for custom widget
        to opacity 10% of given background color, and title font should be
        the same color
     */
//    $(".custom-widget-wrapper").css("background-color", hex_to_rgba(custom_widget_bg, 0.1));
//    $(".custom-title").css("color", custom_widget_bg);

    // Add the appropriate content to the initial "front side"
    let frontFace = $('.face1');
    let frontContent = $('.store li:first-child').html();
    frontFace.html(frontContent);

    let i = 1;
    setInterval(function () {
        /*
            We set interval for 3 seconds for widgets to flip
            after last widget appears, we reset to 1st widget
            and flip continues
         */
        flipCard(i);
        i += 1;
        if (i > num_widgets) {
            i = 1;
        }
    }, 3000);

});

function flipCard(n) {
    if (topCard === n) return;

    // Replace the contents of the current back-face with the contents
    // of the element that should rotate into view.
    let curBackFace = $('.' + (facingUp ? 'face2' : 'face1'));
    let nextContent = $('.store li:nth-child(' + n + ')').html();
    curBackFace.html(nextContent);

    // Rotate the content
    $('.card').toggleClass('flipped');
    topCard = n;
    facingUp = !facingUp;
}

function hex_to_rgba(hex, opacity = null) {
    /*
        We return rgba value of hex code, where
        a value is 0.1 always
        Requirement: background of widget should
        be of same color of font, but with opacity
        of 10%
     */
    let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ?
        "rgba(" + parseInt(result[1], 16) + ","
        + parseInt(result[2], 16) + ","
        + parseInt(result[3], 16) + ","
        + opacity + ")"
        : null;
}

function open_custom_widget_link(link) {
    /*
        check if the link contains http or https, else add it
     */
    if (!/^https?:\/\//i.test(link)) {
        link = 'https://' + link;
    }
    window.location.href = link;
}
