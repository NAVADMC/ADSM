function debounce(a,b,c){var d;return function(){var e=this,f=arguments;clearTimeout(d),d=setTimeout(function(){d=null,c||a.apply(e,f)},b),c&&!d&&a.apply(e,f)}};


safe_save = function(url, data){
    if(typeof outputs_exist === 'undefined' || outputs_exist == false) { 
        $.post(url, data, function() { window.location.reload() });
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
     $('.production_list, .group_list').each(function(){
        $('#population_panel').removeClass('TB_panel_closed')
    })
}
    

$(function(){
    open_panel_if_needed();
    
    $(document).on('click', '#TB_population', function(){
        $('#population_panel').toggleClass('TB_panel_closed')
    })
    
    $(document).on('click', 'a[load-target]', function(event){
        event.preventDefault()
        var selector = $(this).attr('load-target')
        $(selector).load($(this).attr('href'), open_panel_if_needed)
    })
    
    $(document).on('click', '[data-click-toggle]', function(){
        $(this).toggleClass($(this).attr('data-click-toggle'));
    });


    $(document).on('submit', '.ajax', function(event) {
        event.preventDefault();
        var $self = $(this)
        $.ajax({
            url: $(this).attr('action'),
            type: "POST",
            data: $(this).serialize(),
            success: function(form_html) {
                // Here we replace the form, for the
                if($self.closest('#main-panel').length){ //in the main panel, just reload the page
                    $('body').replaceWith(form_html);
                }else{
                    $self.replaceWith(form_html);
                    $('#left-panel').load(window.location + " #left-panel>*")
                }
            },
            error: function () {
                $self.find('.error-message').show()
            }
        }).always(function() {
            $('.blocking-overlay').hide();
        });
    })

    ////This is probably the code used for reporting bad scenario titles
    //$(document).on('submit', '.ajax', function(evt) {
    //    evt.preventDefault();
    //    $.post($(this).attr('action'), $(this).serialize())
    //        .done(function( data ) {
    //            if (data.status == "success") {
    //                $('.ajax').trigger('saved');
    //            } else if (data.status == "failed") {
    //                alert_template = '<div class="alert alert-danger">' +
    //                                    '<a href="#" class="close" data-dismiss="alert">' +
    //                                        '&times;' +
    //                                    '</a>' +
    //                                    '<strong>Error:</strong> ' + data.message +
    //                                 '</div>';
    //                $('#title').before(alert_template);
    //        }
    //    }).always(function() {
    //        $('.blocking-overlay').hide();
    //    });
    //});
    
    $(document).on('click', '#check_update', function(event) {
        $(this).addClass('loading_button')
    });
    
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

    function populate_pdf_panel(self) {
        var selector = '#right-panel'
        var url = $(self).attr('data-new-item-url');
        if ($(self).val() != 'data-add-new' && $(self).val() != '')
            url = url.replace('new', $(self).val());//will edit already existing model
        $(selector).load(url)
        $(self).closest('.layout-panel').find('select').removeClass('active')  // nix .active from the earlier select
        $(self).addClass("active")  //@tjmahlin use .active to to style links between panels 
        //TODO: add newly saved model to the list of options
    }

    $(document).on('change focus', '[data-new-item-url]', function(event){
        //event.preventDefault()
        populate_pdf_panel(this);
    });
    
    $(document).on('click', '[data-new-item-url] + a i', function(event) {
        event.preventDefault()
        var select = $(this).closest('.control-group, td').find('select');
        populate_pdf_panel(select);

    })
    
    $(document).on('change', ':input, select', function(){
        $('.btn-save').removeAttr('disabled')
    });
    
    $(document).on('input', 'input, textarea', function(){
        $('.btn-save').removeAttr('disabled')
    });
    
    
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
        var do_async = true //$(this).hasClass('ajax-post')
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
                        if(do_async){
                            $.post(link).done(function(){window.location.reload()});
                        } else {
                            window.location = link;
                        }
                    }
                }
            ]
        });
    });

    //$(document).on('click', 'select + a i', function(event){
    //    var select = $(this).closest('.control-group, td').find('select');
    //    modelModal.show(select);
    //    event.preventDefault();
    //});


    $('#id_disable_all_controls').change(function(event){
        //toggle global disabled state and submit form.  views.py will update the context and redirect
        //It is important to un-disable fields before submit so that their values go to the DB
        //Josiah: I'm not entirely happy with the jumpiness of this solution, but it does satisfy Issue #79
        var form = $(this).closest('form');
        form.children().each(function (index, value) {
            $(value).removeAttr('disabled');
            $(value).find(':input').removeAttr('disabled');//remove disabled
        });
        console.log(form.serialize());
        safe_save('', form.serialize());//will cause page reload
        // window.location.reload();
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


var modelModal = {
                //processData: false,
                //contentType: false}
    ajax_submit: function(url, success_callback, fail_callback){
        var $form = $('.modal-body form')
        return $.post( url, $form.serialize()).done(function (data, status, xhr){
            if(typeof(data) == 'object') {
                if (data['status']=='success') { //redundant for now
                    success_callback(data)
                }
            } else {//html dataType  == failure probably validation errors
                fail_callback(data)
            }
        }).always(function() {
            $('.blocking-overlay').hide();
        });
    },

    ajax_success: function(modal, selectInput){
        return function(data) {
            console.log('ajax_success', modal, selectInput, data);
            $('select[data-new-item-url="' + selectInput.attr('data-new-item-url') + '"] [value="data-add-new"]')
                .before($('<option value="'+data['pk']+'">'+data['title'] + '</option>')); // Add option to all similar selects
            selectInput.val(data['pk']); // select option for select that was originally clicked
            modal.modal('hide');
        };
    },

    populate_modal_body: function($newForm, modal) {
        var $form = $newForm.filter('section').find('form').first();
        $form.find('.buttonHolder').remove();
        modal.find('.modal-body').html($form);
        modal.find('.modal-title').html($newForm.find('#title').html());
        $('body').append(modal);
        $('#id_equation_type').trigger('change'); //see also probability-functions.js
        return $form;
    },

    validation_error: function(modal) {
        var self = this;
        return function(data) {
            console.log('validation_error:\n');
            self.populate_modal_body($(data), modal);
        };
    },

    show: function(selectInput) {
        var self = this;
        var modal = this.template.clone();
        modal.attr('id', selectInput.attr('name') + '_modal');
        var url = selectInput.attr('data-new-item-url');
        if(selectInput.val() != 'data-add-new' && selectInput.val() != '')
            url = url.replace('new', selectInput.val());//will edit already existing model

        $.get(url, function(newForm){
            var $newForm = $($.parseHTML(newForm));
            self.populate_modal_body($newForm, modal);
            modal.find('.modal-footer button[type=submit]').on('click', function() {
                self.ajax_submit(url, self.ajax_success(modal, selectInput), self.validation_error(modal));
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
                        <h4 class="modal-title">Modal title</h4>\
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
    var form = $('section form');
    var $checkbox = form.find('#id_disable_all_controls');
    if($checkbox.length){
        if ($checkbox.is(':checked')) {
            form.children('div:not(#div_id_name, #div_id_disable_all_controls)').each(function (index, value) {
                $(value).attr('disabled', 'disabled')
                $(value).find(':input').attr('disabled', true);
            });
        }
    }//else do nothing
};

