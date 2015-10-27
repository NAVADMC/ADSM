
$(function(){

    var build_protocols_list = function(){
        $.get('/setup/Protocols.json', function(json){
            json.forEach(function(entry, index){
                index += 2; // leave a space at the beginning for parent submodel
                var id = 'accordion-'+index;
                var $accordion =
                $('<div class="panel-group" id="accordion-'+index+'">\
                    <div class="model-banner">\
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion-'+index+
                        '" href="#sub-model'+index+'">'+ entry.name +'</a>\
                    </div>\
                   </div>');
                var $sub_headings = $('<div id="sub-model' + index + '" class="panel-collapse collapse in" style="height: auto;">');
                entry['tabs'].forEach(function(tab, tab_index){
                    $sub_headings.append($('<label class="checkbox"><input type="checkbox" name="use_detection" checked="" id="id_'+
                        tab['field'] + '" class="checkboxinput">' +
                        tab['name'] + '</label>'));
                });
                $accordion.append($sub_headings);
                $('#sub-model1').append($accordion);
            });
        });
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