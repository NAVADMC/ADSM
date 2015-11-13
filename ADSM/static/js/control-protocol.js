get_parent_title = function(element) {
    return $(element).parents('.model-banner').find('[load-target="#center-panel"]').first();
};

current_is_active = function (element) {
    var current = $('#center-panel form').attr('action');
    var parent_title_link = get_parent_title(element);
    var should_be = parent_title_link.attr('href');
    return current == should_be;
};

function active_tab(element) {
//select the tab
    $('.tab-pane').removeClass('active');
    var target = $('.tab-pane a').filter(function () {
        return $(this).text().toLowerCase() === $(element).text().toLowerCase();
    });
    var id = target.attr('href');
    $(id).addClass('active');
    check_enabled_tabs();
}

switch_tabs = function(element){
    //first, verify we're talking about the same protcol
    if(!current_is_active(element)){
        //activate the correct protocol rather than navigating
        load_target_link.call(get_parent_title(element), function(){active_tab(element)});
    }else{
        active_tab(element);
    }
};


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
                    $('<div class="model-banner defined_wrapper"> ' +
                        '<a class="accordion-toggle" role="button" data-toggle="collapse" data-parent="#accordion" href="#sub-model'+index+'">' +
                        '<a href="/setup/ControlProtocol/' + entry.pk + '/" load-target="#center-panel" >' + //nested for collapse/expand vs load panel functions
                        entry.name +'</a></a>' +
                        '<a href="#" class="delete-icon pull-right" title="delete" data-delete-link="/setup/ControlProtocol/2/delete/"></a> ' +
                        '<a href="/setup/ControlProtocol/' + entry.pk + '/copy/" load-target="#center-panel" class="copy-icon pull-right" title="duplicate"></a>' +
                    ' </div>');

                var $container = $('<div id="sub-model' + index + '" class="panel-collapse collapse" role="tabpanel">');
                var $sub_headings = $('<ul class="file_list compact">');
                entry['tabs'].forEach(function(tab, tab_index){
                    $sub_headings.append(
                        $('<li class="defined"> ' +
                            '<div class="defined_wrapper">' +
                                '<input type="checkbox" name="'+ tab['field'] + '" ' + //used in endpoint url
                                (tab['enabled'] ? "checked" : "") +  //initial checked state
                                ' data-proxy="#id_'+ tab['field'] +
                                '" class="checkboxinput fat_checkbox">' +
                                '<div class="defined_name" onClick="switch_tabs(this);">'+
                                tab['name'] + '</div>' +
                            '</div>' +
                        '</li>'));
                });
                $container.append($sub_headings);
                $header.append($container);//children
                $accordion.append($header);
            });
            $('#protocol_list').append($accordion);
            //$('.collapse').collapse(); //enable bootstrap javascript
        }});
    };

    var hide_hidden_labels = function(){
        $(':checkbox').each(function(index, use_check){
            if($(use_check).attr('hidden')){
                var container = $(use_check).closest('.control-group');
                container.hide();
            }
        });
    };


    var check_enabled_tabs = function(use_check){
        //handle proxy before computing
        if(typeof use_check !== 'undefined' &&
                $(use_check).attr('data-proxy')){ // this check box is in the model list, not in a form
            var value = $(use_check).prop('checked');
            var url = get_parent_title(use_check).attr('href') + $(use_check).attr('name') + '/'; // use_detection
            $.post(url, {'value': value});

            if(current_is_active(use_check)) { // this is relevant to the currently active form and not some other one
                $($(use_check).attr('data-proxy')).prop('checked', $(use_check).prop('checked'));
                use_check = $($(use_check).attr('data-proxy'));
            }
        }
        if(typeof use_check === 'undefined'){
            use_check = $('.tab-pane.active').find(':checkbox').first();
        }

        //do visibility
        if(use_check.length > 0 && use_check[0].id.indexOf('use_') != -1) { // one of the use_detection, use_tracing, etc check boxes
            use_check.closest('.tab-pane').children('div').each(function (index, element) {
                if( $(element).find('#' + use_check[0].id).length == 0) {//not my direct parent
                    if ( !use_check.is(':checked')) {
                        $(element).attr('disabled', 'disabled');
//                            $(element).find(':input').attr('disabled', true);
                         // important not to disable inputs so that default, required values are still sent
                    } else {
                        $(element).removeAttr('disabled');
                        $(element).find(':input').removeAttr('disabled');
                    }
                }
           });
        }
    };

$(function(){

    $(':checkbox').livequery(function(){ //when new checkboxes crop up they will have an event handler assigned to them
        $(this).change(function(){
            check_enabled_tabs(this)
        });
    });
    $('form').livequery(hide_hidden_labels);
});