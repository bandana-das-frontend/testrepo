var fetch_searched_page_posts = true;
var search_type;
var search_location;
var search_topic;

document.addEventListener('turbolinks:before-render', () => {
});

document.addEventListener('turbolinks:request-start', () => {
    $("#top-thin-line").addClass("d-none");
});

document.addEventListener('turbolinks:request-end', () => {
    $("#top-thin-line").removeClass("d-none");
});

document.addEventListener("turbolinks:load", function () {
});

(() => {
    const application = Stimulus.Application.start()

    application.register("searchResults", class extends Stimulus.Controller {

        static get targets() {
            return ["leftSection", "middleSection", "rightSection", "searchtype", 'searchstring', 'searchlocation', 'searchtopic']
        }

        connect() {
            search_type = `${this.searchtypeTarget.value}`;
            search_string = `${this.searchstringTarget.value}`;
            search_location = `${this.searchlocationTarget.value}`;
            search_topic = `${this.searchtopicTarget.value}`;
            window.addEventListener('scroll', paginate_searched_posts);
            if ($('body').width() <= 768) {
                $("#mob-search-section").hide();
                $("#mob-header").show();
                $("#mob-search-input").val(search_string);
            } else {
                $("#search-section").show(function () {
                    $("#main-container").css("top", "180px");
                    $(".desktop-top-ad").css("top", "180px");
                    $("#search-input").val(search_string);
                });
            }

            $(".search_topic_option").click(function () {
                search_topic = $(this).text();
                search_location = $("#search_location").val();
                $("#search_topic").val(search_topic);
                $(this).parents('.btn-group').find('.dropdown-toggle').html(search_topic);
                Turbolinks.visit("/search-articles?search_string=" + encodeURIComponent(search_string) + "&topic=" + encodeURIComponent(search_topic) + "&location=" + encodeURIComponent(search_location));
            });

            $(".search_location_option").click(function () {
                search_location = $(this).text();
                search_topic = $("#search_topic").val();
                $("#search_location").val(search_location);
                $(this).parents('.btn-group').find('.dropdown-toggle').html(search_location);
                Turbolinks.visit("/search-articles?search_string=" + encodeURIComponent(search_string) + "&topic=" + encodeURIComponent(search_topic) + "&location=" + encodeURIComponent(search_location));
            });
            $("#clear_filter").click(function () {
                Turbolinks.visit("/search-articles?search_string=" + encodeURIComponent(search_string));
            });

        }
        disconnect() {
            $("#mob-search-section").hide();
            $("#mob-header").show();
            window.removeEventListener('scroll', paginate_searched_posts);
            $("#clear_filter").off();
        }
    });
})();

// function to handle Pagintion in search page on scroll
function paginate_searched_posts() {
    var url_path = ""
    if( search_type == "None"){
        url_path = "/paginated-search-articles?search_string=" + encodeURIComponent(search_string) +"&topic=" + encodeURIComponent(search_topic) + "&location=" + encodeURIComponent(search_location)
    }
    else{
        url_path = "/paginated-search-articles/"+search_type+"?search_string=" + encodeURIComponent(search_string) +"&topic=" + encodeURIComponent(search_topic) + "&location=" + encodeURIComponent(search_location)
    }

    if ((window.innerHeight + window.scrollY) >= (document.body.offsetHeight) - 3000) {
        if (fetch_searched_page_posts) {
            searched_page_num += 1;
            fetch_searched_page_posts = false;
            $.ajax({
                type: 'GET',
                url: url_path + "&page=" + String(searched_page_num),
            }).done(function (data) {
                $("#searched_posts").append(data);
                fetch_searched_page_posts = true;
            });
        }
    }
}
