
$(function(){

    var check_enabled_tabs = function(){
        $('.tab-pane').each(function(){
            var use_check = $(this).find(':checkbox').first();
            if(use_check.length > 0 && use_check[0].id.indexOf('use_') != -1) { // one of the use_detection, use_tracing, etc check boxes
                $(this).children('div').each(function (index, value) {
                    if( $(this).find('#' + use_check[0].id).length == 0) {//not my direct parent
                        if ( !use_check.is(':checked')) {
                            $(value).attr('disabled', 'disabled');
//                            $(value).find(':input').attr('disabled', true); 
                             // important not to disable inputs so that default, required values are still sent
                        } else {
                            $(value).removeAttr('disabled');
                            $(value).find(':input').removeAttr('disabled');
                        }
                    }
               });
            }
        })
    }
    
    $(':checkbox').change(check_enabled_tabs);
    check_enabled_tabs(); //run once at the beginning
})