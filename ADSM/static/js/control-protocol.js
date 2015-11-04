switchTabs = function(element){
    //first, verify we're talking about the same protcol
    var current = $('#center-panel form').attr('action');
    var parent_title_link = $(element).parents('.model-banner').find('[load-target="#center-panel"]').first();
    var should_be = parent_title_link.attr('href');
    if(current != should_be){
        parent_title_link.click();//activate the correct protocol rather than navigating
        //timing reliability is tricky so I'm going to leave this for a second click from the user
    }else{
        //select the tab
        $('.tab-pane').removeClass('active');
        var target = $('.tab-pane a').filter(function(){ return $(this).text().toLowerCase() === $(element).text().toLowerCase();});
        var id = target.attr('href');
        $(id).addClass('active');
    }
};

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
                                '<input type="checkbox" name="use_detection" checked="" id="id_'+
                                tab['field'] + '" class="checkboxinput fat_checkbox">' +
                                '<div class="defined_name" onClick="switchTabs(this);">'+
                                tab['name'] + '</div>' +
                            '</div>' +
                        '</li>'));
                });
                $container.append($sub_headings);
                $header.append($container);//children
                $accordion.append($header);
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