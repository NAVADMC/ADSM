
$(function(){
    open_panel_if_needed();
    check_disabled_controls();

    $(document).on('click', 'form.ajax .btn-cancel, .btn-cancel[form]', function(){
        var form = $(this).closest('form');
        var attachment = $(this).attr('form');
        if(typeof attachment !== 'undefined')
            form = $('#' + attachment)
        var $container = form.closest('div');
        if($container.closest('.layout-panel').attr('id') == 'main-panel'){
            window.location.reload()
        }else{
            clear_form_populate_panel($container);
        }
    })

    $(document).on('click', '#assign-function', function(){
        var $form = $(this).closest('.layout-panel').find('form')
        if($form.length){
            $form = $form.first()
            var action = $form.attr('action')
            var model = action.split('/')[2]
            var pk = action.split('/')[3] //the edit action URL has the pk in it
            var parent_select = get_parent_select($form)
            $(this).popover('destroy')
            if(parent_select != null){
                if(parent_select.attr('data-new-item-url').indexOf(model) != -1){ //correct model
                    if(pk != 'new'){
                        parent_select.val(pk)
                        parent_select.closest('.layout-panel').find('.btn-save').removeAttr('disabled')
                    }
                }else{
                    $(this).popover({'content': "Cannot assign a probability function to a relational field, or vice versa",
                                     'trigger': 'focus'}) //placement bottom would be nice, but it gets cut off by the panel
                    $(this).popover('show')
                }
            }else{
                $(this).popover({'content': "No active fields to assign",
                                 'trigger': 'focus'})
                $(this).popover('show')
            }
        }
    })

    $('form[action="/setup/RelationalFunction/new/"]').livequery(function(){
        make_function_panel_editable(); //new forms should come in editable
    })

    $('form[action="/setup/ProbabilityFunction/new/"]').livequery(function(){
        make_function_panel_editable(); //new forms should come in editable
    })


    $(document).on('click', '#functions_panel span', function(event){
        $('.function_dropdown').removeClass('in');
    })

    //$(document).on('change', '#functions_panel input', function(event){
    //    var $form = $(this).closest('form')
    //    var load_target = $('#function-graph')
    //    var formAction = load_target.attr('src');
    //    var formData = new FormData($form[0])
    //    ajax_submit_complex_form_and_replaceWith(formAction, formData, $form, load_target);
    //})

    $(document).on('click', '.TB_btn', function(){
        var already_open = $(this).hasClass('active') //check before altering anything
        $('.TB_btn.active').removeClass('active') //close anything that might be open
        $('.TB_panel').addClass('TB_panel_closed')

        if(!already_open){
            $(this).addClass('active')
            var target_str = $(this).attr('TB-target')
            $(target_str).removeClass('TB_panel_closed')
        }
    })
    
    $(document).on('click', 'a[load-target]', function(event){
        event.preventDefault()
        var selector = $(this).attr('load-target')

        //Wait until a problem comes up betwee 'active' and ':focus' to fix this
        //$input.closest('.layout-panel').find('.defined').removeClass('focused')
        //$(this).closest('.defined').addClass('focused');//?????????????????????????????????

        $(this).closest('.layout-panel').find('a').removeClass('active')  // nix .active from the earlier select
        $(this).addClass("active")  //@tjmahlin use .active to to style links between panels
        $(selector).load($(this).attr('href'), open_panel_if_needed)
        $('#center-panel').addClass('reveal') //allows toggle of box shadow on :before pseudo element
    })
    
    $(document).on('click', '[data-click-toggle]', function(){
        $(this).toggleClass($(this).attr('data-click-toggle'));
    });

    $(document).on('submit', '.ajax', function(event) {
        event.preventDefault();
        var $self = $(this)
        var formAction = $(this).attr('action');
        var formData = new FormData($self[0])
        var load_target = $self
        var loading_message = $self.attr('data-loading-message') || "Working..."
        if($self.parent().hasClass('fragment')){
            load_target = $self.parent()
        }
        if($self.parent().find('button[type=submit]').hasClass('btn-danger')) {//for deleting outputs on form submission
            ajax_submit_complex_form_and_replaceWith(formAction, formData, $self, load_target, function () {
                window.location.reload()
            }, loading_message);  //updates Navigation bar context
        }else{
            ajax_submit_complex_form_and_replaceWith(formAction, formData, $self, load_target, undefined, loading_message);
        }
    })

    $(document).on('click', '#update_adsm', function(event){
        event.preventDefault();
        $.get('/app/Update/', function(result){ });
    });

    $(document).on('saved', 'form:has(.unsaved)', function(){ //fixes 'Save' button with wrong color state
        $(this).find('.unsaved').removeClass('unsaved');
    })

    $(document).on('click', '.open_scenario', function(event){ // #new_scenario is handled by [data-copy-link]
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

    //$(document).on('click', '.btn-save', function() {
    //    if ($(this).closest('form').find(':invalid').length == 0) {
    //        $('.blocking-overlay').show().find('.message').text('Working...');
    //    }
    //});

    $(document).on('mousedown', '[data-new-item-url]', function(e){
            $(this).prop('last-selected', $(this).val()); // cache old selection
    });

    $(document).on('change focus', '[data-new-item-url]', function(event){
        //this needs to ignore the event if it's in the right panel, since that will open a modal
        //#422 "Edits" in the far right will open a modal, since we've run out of space
        if($(this).val() == 'data-add-new' || $(this).closest('.layout-panel').attr('id') != 'functions_panel'){
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
    
    
    $('[data-visibility-controller]').livequery(function(){
        attach_visibility_controller(this)})
    
    
    $('[data-visibility-context]').livequery(function(){
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
        var deleting_outputs = typeof outputs_exist !== 'undefined' && outputs_exist;
        var do_reload = $(this).hasClass('ajax-post') || deleting_outputs
        var direct_link = $(this).hasClass('direct_link')
        var $containing_panel = $(this).closest('.layout-panel')
        var object_type = link.split('/')[2]
        if (typeof object_type === 'undefined') {
            object_type = 'object';
        }
        var additional_msg = ''
        if(deleting_outputs){
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
                                    clear_form_populate_panel($containing_panel, link)
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

    $(document).on('click', '[data-copy-link]', function(){
        var link = $(this).attr('data-copy-link')
        var dialog = check_file_saved();
        if(dialog){
            event.preventDefault();
            dialog.$modal.on('hidden.bs.modal', function() {
                prompt_for_new_file_name(link);
            })
        }else{
            prompt_for_new_file_name(link);
        }
    })

    $('#id_disable_all_controls').change(function(event){
        var isChecked = $(this).prop('checked');
        var new_link = window.location;
        if(!isChecked){ //check if we're currently on a forbidden page
            var label = $('nav').find('a.active').first().text()
            $.each(['Vaccination', 'Protocol', 'Zone'], function(index, value){
                if(label.indexOf(value) != -1){
                    new_link = '/setup/ControlMasterPlan/1/'
                    console.log(new_link)
                }
            })
        }
        safe_save('/setup/DisableAllControls.json/', {use_controls: isChecked}, new_link);
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
    $('.defined').on('click', function(){
        $('.defined').removeClass('focused')
        $(this).addClass('focused');
    });

    $('#id_equation_type').livequery(hide_unneeded_probability_fields)

    $(document).on('change', '#id_equation_type', function(){
        hide_unneeded_probability_fields();
    });

    $(document).on('click', '.edit-button', function() {
        $('.edit-button-holder a, .edit-button-holder button').addClass('reveal')
    })

    $(document).on('click', '.overwrite-button', function () {
        make_function_panel_editable()
    })

    $('.edit-button-holder .copy-button').livequery(function() {
        $('.edit-button-holder .copy-button').on('click', function () {
            make_function_panel_editable()
            var target = $('#' + $(this).attr('form'))
            target.attr('action', target.attr('action').replace(/\d+/i, 'new')) //values already loaded, but this should go to /new/
            console.log(target.attr('action'))
            var name_in = $('#functions_panel #id_name')
            name_in.val(name_in.val() + ' - Copy')
        })
    })
})

//#####################################################################################//
//#####################################################################################//

function debounce(a, b, c) {
    var d;
    return function () {
        var e = this, f = arguments;
        clearTimeout(d), d = setTimeout(function () {
            d = null, c || a.apply(e, f)
        }, b), c && !d && a.apply(e, f)
    }
};


safe_save = function(url, data, new_link){
    if(typeof outputs_exist === 'undefined' || outputs_exist == false) { 
        $.post(url, data, function() {
            if(typeof new_link === 'undefined'){
                window.location.reload();
            }else{
                window.location = new_link;
            }
        });
    } else { //confirmation dialog so we don't clobber outputs
        var dialog = new BootstrapDialog.show({
            closable: false,
            title: '',
            type: BootstrapDialog.TYPE_WARNING,
            message: 'Changing input parameters will invalidate the currently computed results. Select "Proceed" to <strong>delete the results set</strong> and commit your changes.',
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
    check_if_TB_panel_form_mask_needed()
}

function populate_pdf_panel(select) {
    var $input = $(select)
    if($input.hasClass('grouplist') || $input.hasClass('productiontypelist'))  //grouplist uses the population_panel instead
        return;
    var load_target = '#functions_panel #current-function'
    var origin = $input.closest('.layout-panel').attr('id');
    if(origin == 'left-panel') { //use the center-panel if this is from left
        load_target = '#center-panel'
        $('#center-panel').addClass('reveal') //allows toggle of box shadow on :before pseudo element
    }
    if(origin == 'center-panel' || origin == 'main-panel'){
        $('#functions_panel').removeClass('TB_panel_closed')
    }
    if(origin == 'functions_panel'){ // we've run out of room and must use a modal
        modelModal.show($input);
        return
    }
    var url = $input.attr('data-new-item-url');
    if ($input.val() != 'data-add-new' && $input.val() != '')
        url = url.replace('new', $input.val());//will edit already existing model
    $(load_target).load(url)
    $input.closest('.layout-panel').find('select').removeClass('active')  // nix .active from the earlier select
    $input.addClass("active")  //@tjmahlin use .active to to style links between panels 
    $input.closest('.layout-panel').find('.controls').removeClass('active_linking') //made by tjmahlin - remove .active_linking from earlier select parent
    $input.parent('.controls').addClass("active_linking") //add .active_linking class to .active select parent in order to creat linking style between center and right column
}


function get_parent_select($self) {
    var parent = null
    var $inDomElement = $( '#'+ $self.find('input').last().attr('id') ) //grab the matching form from the DOM
    var actives = $inDomElement.closest('.layout-panel').prevAll('.layout-panel').first().find('select.active')
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
    if( $('.scenario-status.unsaved').length)
    {
        var filename = $('.filename').text().trim()
        var dialog = new BootstrapDialog.show({
            title: 'Unsaved Scenario Confirmation',
            closable: false,
            type: BootstrapDialog.TYPE_WARNING,
            message: 'Would you like to save your changes to <strong>' + filename + '</strong> before proceeding?',
            buttons: [
                {
                    label: 'Don\'t Save',
                    cssClass: 'btn btn-dont-save',
                    action: function(dialog){
                        dialog.close();
                    }
                },
                {
                    label: 'Save',
                    cssClass: 'btn-primary btn-save',
                    action: function(dialog){
                        var form = $('.filename').closest('form');
                        $.get(form.attr('action'), $(form).serialize(),
                            function(){
                                dialog.close()
                            }
                        ).always(function() {
                            $('.blocking-overlay').hide();
                        })
                    }
                }
            ]
        });
        return dialog;
    }
}


two_state_button = function(){
    if(typeof outputs_exist === 'undefined' || outputs_exist == false) {
        return 'class="btn btn-primary btn-save">Apply changes'
    } else {
        return 'class="btn btn-danger btn-save">Delete Results and Apply Changes'
    }
}


function contains_errors(html) {
    return $(html).find('span.error-inline').length
}

function add_model_option_to_selects(html, selectInput) {
    var action = $(html).find('form').first().attr('action');
    var pk = action.split('/')[3]; //the edit action URL has the pk in it
    var model_link = action.replace(pk, 'new'); //for targetting other selects
    var title = 'Newest Entry';
    try {
        title = $(html).find('input[type="text"]').first().val();
    } catch (e) { }

    $('select[data-new-item-url="' + model_link + '"] [value="data-add-new"]')
        .before($('<option value="' + pk + '">' + title + '</option>')); // Add option to all similar selects
    if(selectInput != null){
        selectInput.val(pk); // select option for select that was originally clicked
        selectInput.closest('.layout-panel').find('.btn-save').removeAttr('disabled')
    }
    //add functions to their panel lists
    var $new_link = $('.function_dropdown [href="' + model_link + '"]')
    if($new_link.length) {
        var $back_link = $new_link.clone()
        $back_link.attr('href', $back_link.attr('href').replace('new', pk))
        $back_link.text(title)
        $new_link.parent().after($('<li>' + $back_link.prop('outerHTML') + '</li>')); // Add new link with all properties
    }
}

var modelModal = {
    //processData: false,
                //contentType: false}
    ajax_submit: function(url, success_callback, fail_callback){
        var $form = $('.modal-body form')
        return $.ajax({
            url: url,
            type: "POST",
            data: new FormData($form[0]),
            cache: false,
            contentType: false,
            processData: false,
            success: function(html) {
                if (contains_errors(html)) { //html dataType  == failure probably validation errors
                    fail_callback(html)
                } else {
                    success_callback(html)
                }
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
    $('#left-panel').load(window.location + " #left-panel>*")
    if(typeof $form !== 'undefined'  && $form.length){
        var action = $form[0]['action'] //.attr('action');
        if(action.indexOf('ProductionGroup') != -1 || action.indexOf('ProductionType') != -1){
            $('#population_panel').load("/setup/OutputSettings/1/ #population_panel>*")
        }
    }
}

function check_if_TB_panel_form_mask_needed(){  // I'm currently assuming that all forms are coming from the [load-target] attribute
    var button = $('.TB_panel form .btn-cancel')  //cancellable form was the most specific thing I could think of
    if(button.length && button.closest('form').length){
        var $form = $(button.closest('form'))
        $('.panel-backdrop').show()
        $form.find('.btn-cancel').click(function(){$('.panel-backdrop').hide()})
        $form.find('.btn-save').click(function(){$('.panel-backdrop').hide()})
        $form.closest('.TB_panel').css('z-index', 1050)  // can't seem to bring out a smaller sub component with z-index
    }
}

function prompt_for_new_file_name(link) {
    var is_current_scenario = link == '/app/SaveScenario/'
    var dialog = new BootstrapDialog.show({
        title: 'Scenario Save As...',
        type: BootstrapDialog.TYPE_PRIMARY,
        message: 'Enter the name of the new scenario: <input type="text" id="new_name">',
        buttons: [
            {
                label: 'Cancel',
                cssClass: 'btn',
                action: function (dialog) {
                    dialog.close();
                }
            },
            {
                label: 'Save As',
                cssClass: 'btn-primary',
                action: function (dialog) {
                    dialog.close();
                    var $self = $('.filename input').closest('form');
                    if (is_current_scenario) {
                        $('.filename input').val($('#new_name').val())
                        //$self.submit()
                        ajax_submit_complex_form_and_replaceWith(link, new FormData($self[0]), $self, $self, function () {
                            $('h1.filename').text($('.filename input').val()) //match major title with form value
                        }, undefined);
                    } else {
                        //TODO: need FormData from form that is to be added in #NewScenario
                        //ajax_submit_complex_form_and_replaceWith(link, new FormData($self[0]), $self, $self, undefined);

                        window.location = link + $('#new_name').val();
                    }
                }
            }
        ]
    });
}

function clear_form_populate_panel($container_panel, delete_link) {
    if($container_panel.hasClass('layout-panel') == false //not a layout-panel
            && $container_panel.closest('.layout-panel').attr('id') != 'population_panel') { //inside function panel or left-panel
        $container_panel = $container_panel.closest('.layout-panel') //upgrade to function panel
    }
    var panel_id = $container_panel.attr('id');
    if (panel_id == 'functions_panel') {
        //load list of functions instead of blank
        $.get('/setup/Function/', function (newForm) {
            var $newForm = $($.parseHTML(newForm));
            $container_panel.html($newForm)
        })
    } else {
        if(panel_id == 'left-panel') {
            reload_model_list();
            var primary_key = delete_link.split('/')[3];
            var $center_form = $('#center-panel').find('form');
            if( $center_form.length){
                if(typeof delete_link !== 'undefined' && $center_form.attr('action').indexOf(primary_key) != -1){
                    $('#center-panel').html('')
                }
            }
        } else { //will still clear Create Group form inside of population_panel without destroying the whole panel
            $container_panel.html('') //delete everything from the div containing the form
        }
    }
}


function reload_image(load_target) {
    var target = load_target.find('form')
    if(target.hasClass('relational-form') || target.hasClass('probability-form')){
        var img = $('#function-graph'); //newly placed image
        d = new Date();
        var new_src = img.attr("src") + "?" + d.getTime();
        img.attr("src", new_src);
    }
}

function ajax_submit_complex_form_and_replaceWith(formAction, formData, $self, load_target, success_callback, loading_message) {
    var overlay = $('.blocking-overlay').show();
    if(typeof loading_message !== 'undefined'){
        overlay.find('.message').text(loading_message);
    }
    $.ajax({
        url: formAction,
        type: "POST",
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function (form_html) {
            $('.scenario-status').addClass('unsaved')
            // Here we replace the form, for the
            if ($self.closest('#main-panel').length) { //in the main panel, just reload the page
                if($(form_html).find('#main_panel').length ){
                    $('#main-panel').html($(form_html).find('#main_panel')[0])
                }else {
                    var matches = form_html.match(/(<body>[\S\s]*<\/body>)/i);//multiline match
                    var content = $(matches[1]);
                    $('body').html(content);
                }
            } else {
                if (formAction.lastIndexOf('new/') != -1) { //new model created
                    var parent_panel = $self.closest('.layout-panel').attr('id');
                    if(parent_panel == 'center-panel' || parent_panel == 'population_panel'){
                        reload_model_list($self); //reload left
                    }else{
                        var lastClickedSelect = get_parent_select($self);
                        add_model_option_to_selects(form_html, lastClickedSelect)
                    }
                }
                load_target.replaceWith(form_html)
                reload_image(load_target)
            }
            if(typeof success_callback !== 'undefined'){
                success_callback()
            }
        },
        error: function () {
            $self.find('.error-message').show()
        }
    }).always(function () {
        $('.blocking-overlay').hide();
    });
}

function hide_unneeded_probability_fields() {
    var $idEquationType = $('#id_equation_type');
    var equation_type = $idEquationType.val()
    var fields = $idEquationType.closest('.control-group').nextAll('.control-group');
    fields.each(function (index, control_group) {
        var help_text = $(control_group).find('.help-block').first().text();
        var functions = help_text.toLowerCase().match(/(\w[\w\s]*)(?=[,\.])/g);
        if (functions.indexOf(equation_type.toLowerCase()) >= 0) {
            $(control_group).show();
            $(control_group).find(':input').attr('required', 'required');
        }
        else {
            $(control_group).hide();
            $(control_group).find(':input').removeAttr('required');
        }
    });
}

function make_function_panel_editable() {
    $('.edit-button-holder a, .edit-button-holder button').removeClass('reveal') //collapse the edit buttons, possibly hide
    $('.edit-button-holder').css('display', 'none')

    $('#functions_panel .buttonHolder').removeAttr('hidden')
    $('#functions_panel, #functions_panel input').addClass('editable')
    $('#functions_panel :input').addClass('editable')
    //$('#tb_mask').css('visibility', 'visible')
    $('#functions_panel').css('pointer-events', 'all')
}

