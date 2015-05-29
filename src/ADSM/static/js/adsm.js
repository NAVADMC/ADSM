
$(function(){
    open_panel_if_needed();
    check_disabled_controls();
    
    $(document).on('click', 'form.ajax .btn-cancel', function(){
        $(this).closest('form').closest('div').html('') //delete everything from the div containing the form
    })
    
    $(document).on('click', '#TB_population', function(){
        $('#population_panel').toggleClass('TB_panel_closed')
    })
    
    $(document).on('click', 'a[load-target]', function(event){
        event.preventDefault()
        var selector = $(this).attr('load-target')
        $(this).closest('.layout-panel').find('a').removeClass('active')  // nix .active from the earlier select
        $(this).addClass("active")  //@tjmahlin use .active to to style links between panels
        $(selector).load($(this).attr('href'), open_panel_if_needed)
    })
    
    $(document).on('click', '[data-click-toggle]', function(){
        $(this).toggleClass($(this).attr('data-click-toggle'));
    });


    $(document).on('submit', '.ajax', function(event) {
        event.preventDefault();
        var $self = $(this)
        var formAction = $(this).attr('action');
        $.ajax({
            url: formAction,
            type: "POST",
            data: $(this).serialize(),
            success: function(form_html) {
                // Here we replace the form, for the
                if($self.closest('#main-panel').length){ //in the main panel, just reload the page
                    $('#main-panel').replaceWith(form_html)
                }else{
                    $self.replaceWith(form_html)
                    if(formAction.lastIndexOf('new/') != -1){ //new model created
                        var lastClickedSelect = get_parent_select($self);
                        add_model_option_to_selects(form_html, lastClickedSelect)
                        reload_model_list($self);
                    }
                }
            },
            error: function () {
                $self.find('.error-message').show()
            }
        }).always(function() {
            $('.blocking-overlay').hide();
        });
    })
    
    $(document).on('click', '#update_adsm', function(event){
        $(this).removeClass('loading_button')
        event.preventDefault();
        $.get('/app/Update/', function(result){
            if( result == "success"){
                var dialog = new BootstrapDialog.show({
                    title: 'Update ADSM on Restart',
                    type: BootstrapDialog.TYPE_INFO,
                    message: 'ADSM is now set to update next time you start the application.',
                    buttons: [
                        {
                            label: 'Ok',
                            cssClass: 'btn-info',
                            action: function(dialog){
                                dialog.close();
                            }
                        }
                    ]
                });
            }
        });
    }); 
    
    $(document).on('saved', 'form:has(.unsaved)', function(){ //fixes 'Save' button with wrong color state
        $(this).find('.unsaved').removeClass('unsaved');
    })

    $(document).on('click', '#open_scenario, #new_scenario', function(event){
        var dialog = check_file_saved();
        if(dialog){
            event.preventDefault();
            var link = $(this).attr('href');
            dialog.$modal.on('hidden.bs.modal', function(){
                window.location = link})
        }
    })

    $('.filename input').on('change', function(){
        $(this).closest('form').trigger('submit');
    });

    $(document).on('click', '.btn-save', function() {
        if ($(this).closest('form').find(':invalid').length == 0) {
            $('.blocking-overlay').show().find('.message').text('Working...');
        }
    });

    $(document).on('mousedown', '[data-new-item-url]', function(e){
            $(this).prop('last-selected', $(this).val()); // cache old selection
    });

    $(document).on('change focus', '[data-new-item-url]', function(event){
        //this needs to ignore the event if it's in the right panel, since that will open a modal
        //#422 "Edits" in the far right will open a modal, since we've run out of space
        if($(this).val() == 'data-add-new' || $(this).closest('.layout-panel').attr('id') != 'right-panel'){
            populate_pdf_panel(this);
        }
    });
    
    $(document).on('click', '[data-new-item-url] + a i', function(event) {
        event.preventDefault()
        var select = $(this).closest('.control-group, td').find('select');
        populate_pdf_panel(select);

    })
    
    $(document).on('change', ':input, select', function(){
        $(this).closest('.layout-panel').find('.btn-save').removeAttr('disabled')
    });
    
    $(document).on('input', 'input, textarea', function(){
        $(this).closest('.layout-panel').find('.btn-save').removeAttr('disabled')
    });
    
    
    $('[data-visibility-controller]').each(function(){attach_visibility_controller(this)})
    
    
    $('[data-visibility-context]').each(function(){
        var context_var = window[$(this).attr('data-visibility-context')]
        if(typeof $(this).attr('data-visibility-flipped') !== 'undefined') {
            context_var = !context_var;
        }
        var hide_target = $(this).parents('.control-group')
        if (hide_target.length == 0){  //Sometimes it's not in a form group
            hide_target = $(this)
        }
        if(context_var){
            hide_target.show();
        }else{
            hide_target.hide();
        }
    });
    
    
    $("#open_file").change(function(){
        $(this).parent('form').submit();
    })

    $(document).on('click', '[data-delete-link]', function(){
        var link = $(this).attr('data-delete-link')
        var do_reload = $(this).hasClass('ajax-post')
        var direct_link = $(this).hasClass('direct_link')
        var $containing_panel = $(this).closest('.layout-panel')
        var object_type = link.split('/')[2]
        if (typeof object_type === 'undefined') {object_type = 'object'}
        var additional_msg = ''
        if(typeof outputs_exist !== 'undefined' && outputs_exist){
            additional_msg = ' and <strong><u>All Results</u></strong>' 
        }
        var dialog = new BootstrapDialog.show({
            title: 'Delete Confirmation',
            type: BootstrapDialog.TYPE_WARNING,
            message: 'Are you sure you want to delete the selected ' + object_type + additional_msg + '?',
            buttons: [
                {
                    label: 'Cancel',
                    cssClass: 'btn',
                    action: function(dialog){
                        dialog.close();
                    }
                },
                {
                    label: 'Delete',
                    cssClass: 'btn-danger',
                    action: function(dialog){
                        if(do_reload){
                            $.post(link).done(function(){
                                window.location.reload()
                            });
                        } else {
                            if(direct_link){
                                dialog.close();
                                window.location = link;
                            } else {//neither tag
                                $.post(link).done(function () {
                                    $containing_panel.html('')
                                    var newLink = '/setup/' + link.split('/')[2] + '/new/' //[2] model name
                                    var pk = link.split('/')[3];
                                    // remove option pointing to delete model
                                    $('select[data-new-item-url="' + newLink + '"] [value="' + pk + '"]').remove()
                                    console.log('select[data-new-item-url="' + newLink + '"]', $('select[data-new-item-url="' + newLink + '"]'))
                                    dialog.close();
                                });
                            }
                        } 
                    }
                }
            ]
        });
    });

    $('#id_disable_all_controls').change(function(event){
        var isChecked = $(this).prop('checked');
        safe_save('/setup/DisableAllControls.json/', {use_controls: isChecked});
    });
    
    $(window).resize( function(){
        var nav = document.getElementById('setupMenu');  //need DOM element
        if(nav.scrollHeight > nav.clientHeight){ // returns true if there's a `vertical` scrollbar, false otherwise..
            $('#setupMenu-after, #setupMenu-before').css({'visibility': 'visible'})
        }else{
            $('#setupMenu-after, #setupMenu-before').css({'visibility': 'hidden'})
        }
    }); 
    
    $('#pop-upload').on('submit',function(event){
        var filename = $(this).find('input[type=file]').val()
        if( filename.indexOf('.xml') == -1 && filename.indexOf('.csv') == -1) {
            alert("Uploaded files must have .xml or .csv in the name: " + filename)
            event.preventDefault();
            return false;
        }
    });
    
    $('#file-upload').on('submit',function(event){
        var filename = $(this).find('input[type=file]').val()
        var valid_extensions = {"application/x-sqlite3": '.sqlite3',
                                "application/xml": '.xml'}
        var file_extension = valid_extensions[$(this).find('input[type=file]').attr('accept')]
        if( typeof file_extension !== 'undefined' && filename.indexOf(file_extension) == -1) {
            alert("Uploaded files must have "+file_extension+" in the name: " + filename)
            console.log(file_extension);
            event.preventDefault();
            return false;
        }
    });

})

//#####################################################################################//
//#####################################################################################//

function debounce(a,b,c){var d;return function(){var e=this,f=arguments;clearTimeout(d),d=setTimeout(function(){d=null,c||a.apply(e,f)},b),c&&!d&&a.apply(e,f)}};


safe_save = function(url, data){
    if(typeof outputs_exist === 'undefined' || outputs_exist == false) { 
        $.post(url, data, function() { 
            window.location.reload() 
        });
    } else { //confirmation dialog so we don't clobber outputs
        var dialog = new BootstrapDialog.show({
            closable: false,
            title: '',
            type: BootstrapDialog.TYPE_WARNING,
            message: 'Changing input parameters will invalidate the currently computed results. Would you like to <strong><u>Delete the Results</u></strong> and proceed?',
            buttons: [
                {
                    label: 'Cancel',
                    cssClass: 'btn',
                    action: function(dialog){
                        window.location.reload()
                    }
                },
                {
                    label: 'Proceed',
                    cssClass: 'btn-danger btn-save',
                    action: function(dialog){
                        outputs_exist = false;
                        $.post(url, data, function(){
                            window.location.reload()
                        });
                        dialog.close()
                    }
                }
            ]
        });
    }
}

function open_panel_if_needed(){
     $('.productiontypelist, .grouplist').each(function(){
        $('#population_panel').removeClass('TB_panel_closed')
    })
}

function populate_pdf_panel(select) {
    var $input = $(select)
    if($input.hasClass('grouplist') || $input.hasClass('productiontypelist'))  //grouplist uses the population_panel instead
        return;
    var load_target = '#right-panel'
    var position = $input.closest('.layout-panel').attr('id');
    if(position == 'left-panel'){ //use the center-panel if this is from left
        load_target = '#center-panel'
    }else if(position == 'right-panel'){ // we've run out of room and must use a modal
        modelModal.show($input);
        return
    }
    var url = $input.attr('data-new-item-url');
    if ($input.val() != 'data-add-new' && $input.val() != '')
        url = url.replace('new', $input.val());//will edit already existing model
    $(load_target).load(url)
    $input.closest('.layout-panel').find('select').removeClass('active')  // nix .active from the earlier select
    $input.addClass("active")  //@tjmahlin use .active to to style links between panels 
}


function get_parent_select($self) {
    var parent = null
    var $inDomElement = $( '#'+ $self.find('input').last().attr('id') ) //grab the matching form from the DOM
    var actives = $inDomElement.closest('.layout-panel').prev('.layout-panel').find('select.active')
    if(actives.length){
        parent = actives.first()
    }
    return parent
}


var attach_visibility_controller = function (self){
    var controller = '[name=' + $(self).attr('data-visibility-controller') + ']'
    var hide_target = $(self).parents('.control-group')
    if (hide_target.length == 0 || $(self).attr('class') === 'help-block'){  //Sometimes it's not in a form group
        hide_target = $(self)
    }
    var disabled_value = $(self).attr('data-disabled-value')
    var required_value = $(self).attr('data-required-value')

    $('body').on('change', controller, function(){
        if($(self).val() == disabled_value){
            hide_target.hide()
        }else{
            if($(this).attr('type') == 'checkbox') {
                if( $(this).is(':checked') == (disabled_value === 'false')){
                    hide_target.show()
                }else {
                    hide_target.hide()
                }
            }
            else {
                if (typeof required_value !== 'undefined'){ //required value is specified
                    if($(this).val() == required_value || $(this).val() == ''){
                        hide_target.show()
                    }else{
                        hide_target.hide()
                    }
                }else{
                    hide_target.show()
                }
            }
        }
    })
    $(controller).each(function(index, elem){ //each because radio buttons have multiple elem, same name
        if($(elem).attr('type') != 'radio' || elem.hasAttribute('checked')){
            //radio buttons are multiple elements with the same name, we only want to fire if its actually checked
            $(elem).trigger('change');
        }
    });
    $(hide_target).css('margin-left', '26px');
}


var check_file_saved = function(){
    if( $('body header form div button').hasClass('unsaved'))
    {
        var filename = $('body header form .filename input').attr('value')
        var dialog = new BootstrapDialog.show({
            title: 'Unsaved Scenario Confirmation',
            closable: false,
            type: BootstrapDialog.TYPE_WARNING,
            message: 'Would you like to save your changes to <strong>' + filename + '</strong> before proceeding?',
            buttons: [
                {
                    label: 'Don\'t Save',
                    cssClass: 'btn',
                    action: function(dialog){
                        dialog.close();
                    }
                },
                {
                    label: 'Save',
                    cssClass: 'btn-primary btn-save',
                    action: function(dialog){
                        $.get($('header form').attr('action'), $('header form').serialize(), function(){dialog.close()});
                    }
                }
            ]
        });
        return dialog;
    }
}


two_state_button = function(){
    if(typeof outputs_exist === 'undefined' || outputs_exist == false) {
        return 'class="btn btn-primary btn-save">Save changes'
    } else {
        return 'class="btn btn-danger btn-save">Delete Results and Save Changes'
    }
}


function contains_errors(html) {
    return $(html).find('span.error-inline').length  //TODO: more specific class
    
}

function add_model_option_to_selects(html, selectInput) {
    var action = $(html).find('form').first().attr('action');
    var pk = action.split('/')[3]; //the edit action URL has the pk in it
    var model_link = action.replace(pk, 'new'); //for targetting other selects
    var title = 'Newest Entry';
    try { //TODO: there's a possibility of a form without a name field, in this case the python str() method is preferrable
        title = $(html).find('input[type="text"]').first().val();
    } catch (e) { }

    $('select[data-new-item-url="' + model_link + '"] [value="data-add-new"]')
        .before($('<option value="' + pk + '">' + title + '</option>')); // Add option to all similar selects
    if(selectInput != null){
        selectInput.val(pk); // select option for select that was originally clicked
    }
}

var modelModal = {
    //processData: false,
                //contentType: false}
    ajax_submit: function(url, success_callback, fail_callback){
        var $form = $('.modal-body form')
        return $.post( url, $form.serialize()).done(function (html, status, xhr){
            if (contains_errors(html)) { //html dataType  == failure probably validation errors
                fail_callback(html)
            } else {
                success_callback(html)
            }
        }).always(function() {
            $('.blocking-overlay').hide();
        });
    },

    ajax_success: function(modal, selectInput){
        return function(html) {
            //console.log('ajax_success', modal, selectInput, html.slice(0,100));
            add_model_option_to_selects(html, selectInput);
            modal.modal('hide');
        };
    },

    populate_modal_body: function($newForm, modal) {
        var $form = $newForm.find('form').first();
        $form.find('.buttonHolder').remove();
        modal.find('.modal-body').html($form);
        modal.find('.modal-title').html($newForm.find('#title').html());
        $('body').append(modal);
        return $form;
    },

    validation_error: function(modal) {
        var self = this;
        return function(html) {
            console.log('validation_error:\n');
            self.populate_modal_body($(html), modal);
        };
    },

    show: function($selectInput) {
        var self = this;
        var modal = this.template.clone();
        modal.attr('id', $selectInput.attr('name') + '_modal');
        var url = $selectInput.attr('data-new-item-url');
        if($selectInput.val() != 'data-add-new' && $selectInput.val() != '')
            url = url.replace('new', $selectInput.val());//will edit already existing model

        $.get(url, function(newForm){
            var $newForm = $($.parseHTML(newForm));
            self.populate_modal_body($newForm, modal);
            modal.find('.modal-footer button[type=submit]').on('click', function() {
                self.ajax_submit(url, self.ajax_success(modal, $selectInput), self.validation_error(modal));
            });

            modal.modal('show');
            $(modal).on('hidden.bs.modal', function(){
                $(this).remove(); // deletes it from the DOM so it doesn't get cluttered
            })
        });

        },
    
    template: $('<div class="modal fade">\
                  <div class="modal-dialog">\
                    <div class="modal-content">\
                      <div class="modal-header">\
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
                        <h4 class="modal-title"></h4>\
                      </div>\
                      <div class="modal-body">\
                      </div>\
                      <div class="modal-footer">\
                            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\
                            <button type="submit"' + two_state_button() + '</button>\
                      </div>\
                    </div>\
                  </div>\
                </div>')
}

function check_disabled_controls() {
    /*Disables all the inputs on the Control Master Plan if the disable_all check box is checked on page load */
    if (typeof controls_enabled !== 'undefined' && !controls_enabled && $('#id_destruction_program_delay').length) { //global from context processor
        $('.layout-panel form').first().children('div:not(#div_id_name)').each(function (index, value) {
            $(value).attr('disabled', 'disabled')
            $(value).find(':input').attr('disabled', true);
        });
    }//else do nothing
};

function reload_model_list($form) {
    var action = $form.attr('action');
    $('#left-panel').load(window.location + " #left-panel>*")
    if(action.indexOf('ProductionGroup') != -1 || action.indexOf('ProductionType') != -1){
        $('#population_panel').load("/setup/OutputSettings/1/ #population_panel>*")
    }
}
