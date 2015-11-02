
$(function(){

    var build_protocols_list = function(){
        $.ajax({
        url: '/setup/Protocols.json',
        data: {},
        dataType: 'json',
        success: function(json){
            if($('#accordion').length){//only add it once (was happening twice because of the 301 response
                return;
            }
            var $accordion = $('<div class="panel-group" id="accordion" role="tablist">');
            json.forEach(function(entry, index){
                index += 2; // leave a space at the beginning for parent submodel
                var $header =
                    $('<div class="model-banner">\
                        <a class="accordion-toggle" role="button" data-toggle="collapse" data-parent="#accordion'+
                        '" href="#sub-model'+index+'">'+ entry.name +'</a>\
                       </div>');

                var $sub_headings = $('<div id="sub-model' + index + '" class="panel-collapse collapse" role="tabpanel">');
                entry['tabs'].forEach(function(tab, tab_index){
                    $sub_headings.append($('<label class="checkbox"><input type="checkbox" name="use_detection" checked="" id="id_'+
                        tab['field'] + '" class="checkboxinput">' +
                        tab['name'] + '</label>'));
                });
                $accordion.append($header);
                $accordion.append($sub_headings);//siblings
                console.log("Adding one protocol: " + index);
            });
            console.log("Adding one panel group to the DOM ");
                $('#left-panel').append($accordion);
            //$('.collapse').collapse(); //enable bootstrap javascript
        }});
    };
    build_protocols_list();

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