$(function(){
    var progressBar = $('<div class="progress-bar" style="width: 0%;"></div>');
    var progressStatus = $('<div class="progress-status">Upload starting...</div>');
    var progressInterval;

    $('#file-upload').on('submit', function(e){
        e.preventDefault();
        var formData = new FormData($(this)[0]);
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            xhr: function() {
                var myXhr = $.ajaxSettings.xhr();
                if(myXhr.upload){
                    myXhr.upload.addEventListener('progress',progressHandler, false);
                }
                return myXhr;
            },
            // beforeSend: beforeSendHandler,
            success: completeHandler,
            error: errorHandler,
            data: formData,
            cache: false,
            contentType: false,
            processData: false
        });
        $('#file-upload').hide().after($('<div class="progress progress-striped active" style="width:500px"></div>').append(progressBar)).after(progressStatus);
    });
    var progressHandler = function(progress) {
        var percent_uploaded = (progress.loaded/progress.total)*100;
        progressStatus.html('Loading file ' + Math.round(percent_uploaded) + '%');
        progressBar.css('width', percent_uploaded*0.1 + "%");
        if (progress.loaded == progress.total) {
            progressInterval = setInterval(progressChecker, 500);
        }
    };
    var completeHandler = function(e) {
        clearInterval(progressInterval);
        window.location = e.redirect;
    };
    var errorHandler = function(e) {
        console.log('error', e);
        clearInterval(progressInterval);
    };
    var progressChecker = function() {
        $.get('/setup/UploadPopulation/', function(data){
            if (data.percent <= 0) {
                progressStatus.html(data.status);
                if (progressBar.width() < 100) {
                    progressBar.width(progressBar.width()+2);
                }
            } else if (data.percent >= 100) {
                progressStatus.html(data.status);
                if (progressBar.width() < 500) {
                    progressBar.width(progressBar.width()+1);
                }
            } else {
                progressStatus.html(data.status + " " + Math.round(data.percent*100)/100 + "%");
                progressBar.css('width', (data.percent*0.7 + 20) + "%");
            }
        });
    };
});