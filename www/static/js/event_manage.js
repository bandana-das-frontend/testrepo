var fetch_searched_page_posts = true;
var search_type;

document.addEventListener("turbolinks:load", function () {


    $(document).ready(function () {
        // Since form submission is handle programmatically, form field validation for required fields
        // is done using jquery validation library
        // Initializing jquery form validation
        $("#event_form").validate();
    })

    let file_count = 0
    var media_url = ''
    var is_uploading = false;

    // Starting video upload to S3 as soon as the file is chosen
    document.getElementById('event_media').addEventListener('change', function (event) {
        $("#empty_media_preview_div").css("display", 'none');
        $("#media_loading_icon").css("display", 'block');
        s3upload();
                file_count = event.target.files.length
                var file = event.target.files[0];
                var fileReader = new FileReader();
                if (file.type.match('image')) {

                    fileReader.onload = function () {
                        var img = document.getElementById('image2_preview');
                        $("#img_preview_div").css("display", 'block');
                        $("#event_media_modify").css("display", 'flex');
                        img.src = fileReader.result;
                    };
                    fileReader.readAsDataURL(file);
                } else {
                    fileReader.onload = function () {
                        var blob = new
                        Blob([fileReader.result], {type: file.type});
                        var url = URL.createObjectURL(blob);
                        var
                            video = document.createElement('video');
                        var timeupdate = function () {
                            if (snapImage()) {
                                video.removeEventListener('timeupdate', timeupdate);
                                video.pause();
                            }
                        };
                        video.addEventListener('loadeddata',
                            function () {
                                if (snapImage()) {
                                    video.removeEventListener('timeupdate', timeupdate);
                                }
                            });
                        var snapImage = function () {
                            var canvas = document.createElement('canvas');
                            canvas.width = video.videoWidth;
                            canvas.height = video.videoHeight;
                            canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
                            var image = canvas.toDataURL();
                            var success = image.length > 10000;

                            if (success) {
                                var img = document.getElementById('image2_preview');
                                $("#img_preview_div").css("display", 'block');
                                $("#event_media_modify").css("display", 'flex');
                                img.src = image;
                                URL.revokeObjectURL(url);
                            }
                            return success;
                        };
                        video.addEventListener('timeupdate', timeupdate);
                        video.preload = 'metadata';
                        video.src = url;
                        // Load video in Safari / IE11
                        video.muted = true;
                        video.playsInline = true;
                        video.play();
                    };
                    fileReader.readAsArrayBuffer(file);
                }
    });

    // Util function to generate UUID
    // Adding generateUUID() to add_video.html as util.js doesn't load until force refresh sometime
    function generateUUID() {
        var d = new Date().getTime();
        var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = (d + Math.random() * 16) % 16 | 0;
            d = Math.floor(d / 16);
            return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
        return uuid;
    }

    // This function is used to show loader while request is in progress and
    // disable the submit button click to avoid multiple clicks
    function show_loading() {
        var btn = document.getElementById('submit_cta');
        btn.disabled = true;
        $('#form_submit').css('display','none');
        $('#form_submitting').css('display','block');
    }

    // Click listener for form submit button.
    var is_submitted = false;
    $("#submit_cta").click(function (e) {
        // Check the form validation for required fields
        if ($("#event_form").valid()) {
            // Show loading on the Submit button and disable it for accidental clicks
            show_loading();
            is_submitted = true;
            // Form is not submitted if video upload is in progress
            if (!is_uploading) {
                // Submit the form and send create request
                $("#event_form").submit();
            } else {
                e.preventDefault()
            }
        } else {
            e.preventDefault()
        }
    });



    // Bucket Region : Singapore
    var bucketRegion = 'ap-southeast-1';
    // IdentityPoolId is the anonymous identity setup for direct S3 upload
    var IdentityPoolId = 'ap-southeast-1:c7def7cd-b8f6-4fa5-a9c0-6900c85f7cf5';
    // Bucket name of the S3 upload
    var bucketName = 'poll.media';
    // Updating AWS Config
    AWS.config.update({
        region: bucketRegion,
        credentials: new AWS.CognitoIdentityCredentials({
            IdentityPoolId: IdentityPoolId
        }),
    });

    // Initializing S3 instance
    var s3 = new AWS.S3({
        apiVersion: '2006-03-01',
        params: {Bucket: bucketName},
    });

    // Function to upload selected file to S3, this is called on file select event
    function s3upload() {
        // Getting the selected file
        var files = document.getElementById('event_media').files;
        if (files) {
            var file = files[0];
            var file_name = file.name;
            // Split the filename by '.' and get the last item as file_extension
            var file_extension = file_name.split('.').pop();
            // Use UUID + file_extension as unique file name for upload file
            var uuid_file_name = generateUUID() + '.' + file_extension;
            // Path to upload in S3 bucket
            var filePath = 'posts/' + uuid_file_name;
            s3.upload({
                Key: filePath,
                Body: file,
                ACL: 'public-read'
            }, function (err, data) {
                if (err) {
                    console.log(err);
                    reject('error');
                }
                $("#media_loading_icon").css("display", 'none');
                console.log('Successfully uploaded to S3');
                // Set is_uploading flag to false, after upload is complete
                is_uploading = false;
                // Set the S3 uploaded file  in the form hidden input field 'media_url'
                media_url = data['Location'];
                console.log(media_url)
                $("#media_url").val(media_url);
                // Check if the form is submitted and waiting for upload to complete
                if (is_submitted) {
                    // Submit the form
                    $("#event_form").submit();
                }
            }).on('httpUploadProgress',
                function (progress) {
                    // Setting is_uploading flag to true when video upload is in progress
                    is_uploading = true;
                    // Removing the name attribute of the input video file field in the form, to stop sending the file in Form submit POST request
                    $("#event_media").removeAttr('name');
                    // Removing the required attribute of the input video file field in the form
                    $("#event_media").removeAttr('required');
                    // Updating the progress bar value based on video upload status
                    // var uploaded = parseInt((progress.loaded * 100) / progress.total);
                    // $("#progress").show()
                    // $("#progress").val(uploaded);
                });
        }
    }

    $('#event_media_delete').click(function () {
        $('#media_url').val('');
        $('#image2_preview').attr('src', '');
         $("#media_loading_icon").css("display", 'none');
        $("#img_preview_div").css("display", 'none');
        $("#empty_media_preview_div").css("display", 'block');
        $("#event_media_modify").css("display", 'none');
        file_count = 0
    });

});



