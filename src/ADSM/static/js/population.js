var progressBar = (function(){
    var progress = $('<div class="progress progress-striped active" style="width:500px"></div>'),
        progressBar = $('<div class="progress-bar" style="width: 0%;"></div>'),
        progressStatus = $('<div class="progress-status">Upload starting...</div>'),
        progressInterval;

    var progressChecker =  function() {
        $.get('/setup/UploadPopulation/', function(data){
            var newWidth;
            if (data.percent <= 0) {
                newWidth = 10
                setStatus(data.status, newWidth);
            } else if (data.percent >= 100) {
                newWidth = progressBar.width() < 500 ? progressBar.width()+1 : null;
                setStatus(data.status, newWidth);
            } else {
                setStatus(data.status + " " + Math.round(data.percent*100)/100 + "%", (data.percent*0.7 + 20));
            }
        });
    };

    var setStatus = function(text, width) {
        if (text)
            progressStatus.html(text);
        if (typeof(width) == "number"){
            progressBar.css('width', width + "%");
        }
    };

    return {
       'hide': function(e){
            $('#load_population_widget').show().before('<div class="alert alert-warning"><a href="#" class="close" data-dismiss="alert">&times;</a><strong>Error:</strong> ' + e.message + '</div>');
            progress.remove();
            progressStatus.hide();

        },
        'show': function(){
            $('.alert').alert('close');
            $('#load_population_widget').hide()
                .after(progress.append(progressBar))
                .after(progressStatus);
        },
        'startProgressChecker': function() {
            progressInterval = progressInterval || setInterval(progressChecker, 500);
        },
        'stopProgressChecker': function() {
            clearInterval(progressInterval);
        },
        'setStatus': setStatus
    };
})();

$(function(){
    $('#submit-id-submit').attr('disabled', 'disabled');

    $(document).one('change', '#farm_list input, #farm_list select', function(){
        $('#submit-id-submit').removeAttr('disabled').addClass('unsaved');
    });


    $(document).on('click','.ajax-post', function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: $(this).attr('href'),
            data: $(this).data(), 
            success: completeHandler
        })
        progressBar.show();
        progressBar.setStatus('Loading...', 10);
        progressBar.startProgressChecker();
    });


    $(document).on('submit', '#pop-upload', function(e){
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
        progressBar.show();
    });
    var progressHandler = function(progress) {
        var percent_uploaded = (progress.loaded / progress.total)*100;
        progressBar.setStatus('Loading file ' + Math.round(percent_uploaded) + '%', percent_uploaded*0.1);
        if (progress.loaded == progress.total) {
            progressBar.startProgressChecker();
        }
    };
    var completeHandler = function(e) {
        progressBar.stopProgressChecker();
        if (e.status == "complete") {
            window.location = e.redirect;
        } else {
            progressBar.hide(e);
        }
    };
    var errorHandler = function(e) {
        console.log('error', e);
        progressBar.stopProgressChecker();
    };
});




/*Utility function for getting a GET parameter from the current URL*/
function getQueryParam(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}


/* Construct a query URL based on the value of the filter selects.  Two major types are
* 1) choice selects = fairly simple
* 2) numeric input = have both min and max fields and require additional handling */
var population_filter_string = function() {
    var filters = $('#farm_filter tr').map( function() {
        if($(this).find('td:nth-child(3) select').length) { //state select field
            if($(this).find('td:nth-child(3) select').val()) {
                var str = $(this).attr('id') + '=' + $(this).find('td:nth-child(3) select').val(); //must be a select
                return str.replace(/ /g, '%20'); // global replace
            }else {
                return ''
            }
        }
        else { //this must be a numeric filter, because of the input field
            var name = $(this).attr('id');
            var minimum = $(this).find('td:nth-child(3) input').val() ? //empty string if no value
                name + '__gte=' + $(this).find('td:nth-child(3) input').val() : '';
            var maximum = $(this).find('td:nth-child(5) input').val() ? //empty string if no value
                name + '__lte=' + $(this).find('td:nth-child(5) input').val() : '';
            if(minimum.length && maximum.length) //if both are present, we need to stick an & between them
                return minimum + "&" + maximum;
            else
                return  minimum + maximum; // return one or the other or a blank string if neither
        }
    });
    return filters.get().join('&');
}

/*Updates the page and URL with the latest filter and sort settings.*/
function update_population_filter_and_sort(sort_by) {
    if(sort_by === undefined){ //try and find it in the URL
        var sorting = getQueryParam('sort_by') ?
            'sort_by=' + getQueryParam('sort_by') : '';
    } else{ //sort_by already provided
        var sorting = 'sort_by=' + sort_by;
    }
    var new_url = '?' + population_filter_string();//build URL
    new_url = new_url + sorting;
    //get it with AJAX and insert new HTML with load()
    window.history.replaceState('', 'Population Filters', new_url);
    $('#farm_list').parent().load(new_url + ' #farm_list');
}

//Validation checking for minimums in the filter
$(document).on('change', '#farm_filter input', function(event){ //this needs to come before update_population_filter_and_sort()
    var name = $(this).closest('td').prev().text().toLowerCase();
    if( name.indexOf('max') != -1 ) {
        var min_val = $(this).closest('td').prev().prev().find('input').val();
        $(this).val( Math.max(min_val, $(this).val()) ); //bump up to "Min:" if that is higher
    }
    if( $(this).attr('min') && $(this).val() < $(this).attr('min')) {
        $(this).val( $(this).attr('min') );
    }
});

$(document).on('change', '#farm_filter select, #farm_filter input', function(){
    update_population_filter_and_sort();
});

$(document).on('click', '#farm_list .sortControls a', function(event){
    update_population_filter_and_sort($(this).attr('data-sort-by'));
    event.preventDefault()
});

$(document).on('click', '#refresh_map', function(){
    $('#population_map_container').html('')  //clear previous contents
    //TODO: set background of container to working.gif
    //TODO: request 
    var new_url = '?' + population_filter_string()
    //$('#population_map_container img').attr('src', '/results/Population.png' + new_url)

    var img = new Image();
    $(img).load(function(){
        $('#population_map_container').append($(this));
    }).attr({
        id:'unit_map',
        src: '/results/Population.png' + new_url
    })
    
});

$(document).on('click', '#edit_population', function(){
    $('#population_grid_wraper .buttonHolder').removeAttr('hidden')
    $('#edit-mask').css('visibility', 'visible')
})