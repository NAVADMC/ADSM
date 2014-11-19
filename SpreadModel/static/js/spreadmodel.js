function debounce(a,b,c){var d;return function(){var e=this,f=arguments;clearTimeout(d),d=setTimeout(function(){d=null,c||a.apply(e,f)},b),c&&!d&&a.apply(e,f)}};


safe_save = function(url, data){
    if(typeof outputs_computed === 'undefined' || outputs_computed == false) { 
        $.post(url, data, function() { window.location.reload() });
    } else { //confirmation dialog so we don't clobber outputs
        var dialog = new BootstrapDialog.show({
            title: 'Delete Results Confirmation',
            type: BootstrapDialog.TYPE_WARNING,
            message: 'You must delete your previously computed <strong><u>Results</u></strong> to change input parameters.  Are you sure you want to delete your Results?',
            buttons: [
                {
                    label: 'Cancel',
                    cssClass: 'btn',
                    action: function(dialog){
                        window.location.reload()
                    }
                },
                {
                    label: 'Delete Results',
                    cssClass: 'btn-danger',
                    action: function(dialog){
                        outputs_computed = false;
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
    

$(function(){
    $(document).on('click', '[data-click-toggle]', function(){
        $(this).toggleClass($(this).attr('data-click-toggle'));
    });

    $(document).on('submit', '.ajax', function(evt){ 
        evt.preventDefault();
        var posting = $.post($(this).attr('action'), $(this).serialize()); //this post method is currently not accessible anywhere that accidentally 
        // deleting Results could happen, otherwise wrap this in safe_save()
        posting.done(function( data ) {
            if (data.status == "success") {
                $('.ajax').trigger('saved');
            } else if (data.status == "failed") {
                alert_template = '<div class="alert alert-danger">' +
                                    '<a href="#" class="close" data-dismiss="alert">' +
                                        '&times;' +
                                    '</a>' +
                                    '<strong>Error:</strong> ' + data.message +
                                 '</div>';
                $('#title').before(alert_template);
            }
        });
    })
    
    $(document).on('click', '#update_adsm', function(event){
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
    })

    $(document).on('saved', 'form:has(.unsaved)', function(){ //fixes 'Save' button with wrong color state
        $(this).find('.unsaved').removeClass('unsaved');
    })

    $(document).on('click', 'header .buttonHolder a', function(evt){ //currently "Save is a button, not <a>.  This would be annoying otherwise
        var dialog = check_file_saved();
        console.log(dialog);
        if(dialog){
            evt.preventDefault();
            var link = $(this).attr('href');
            dialog.$modal.on('hidden.bs.modal', function(){
                window.location = link})
        }
    })

    $('.filename input').on('change', function(){
        $(this).closest('form').trigger('submit');
    });

    $(document).on('mousedown', '[data-new-item-url]', function(e){
            $(this).prop('last-selected', $(this).val()); // cache old selection
    });
    $(document).on('change', '[data-new-item-url]', function(e){
        if ($(this).val() == "data-add-new") {
            modelModal.show($(this))
        }
    });

    /*$('[data-visibility-controller]').each(function(){
        var controller = '[name=' + $(this).attr('data-visibility-controller') + ']'
        var hide_target = $(this).parents('.control-group, td')
        var required_value = $(this).attr('data-required-value') || 'True'
        $('body').on('change', controller, function(){
            if($(this).val() == required_value){
                hide_target.show()
            }else{
                hide_target.hide()
            }
        });
        $(controller).each(function(index, elem){ //each because radio buttons have multiple elem, same name
            if($(elem).attr('type') != 'radio' || elem.hasAttribute('checked')){
                //radio buttons are multiple elements with the same name, we only want to fire if its actually checked
                $(elem).trigger('change');
            }
        });
        $(hide_target).css('margin-left', '26px');
    }) */

    
    $('[data-visibility-controller]').each(function(){
        var controller = '[name=' + $(this).attr('data-visibility-controller') + ']'
        var hide_target = $(this).parents('.control-group')
        if (hide_target.length == 0){  //Sometimes it's not in a form group
            hide_target = $(this)
        }
        var disabled_value = $(this).attr('data-disabled-value')
        var required_value = $(this).attr('data-required-value')

        $('body').on('change', controller, function(){
            if($(this).val() == disabled_value){
                hide_target.hide()
            }else{
                if (typeof required_value !== 'undefined'){ //required value is specified
                    if($(this).val() == required_value || $(this).val() == ''){
                        hide_target.show()
                    }else{
                        console.log("Hiding", hide_target)
                        hide_target.hide()
                    }
                }else{
                    hide_target.show()
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
    })
    
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

    $('[data-delete-link]').click(function(){
        var link = $(this).attr('data-delete-link')
        var do_async = $(this).hasClass('ajax-post')
        var object_type = link.split('/')[2]
        if (typeof object_type === 'undefined') {object_type = 'object'}
        var additional_msg = ''
        if(typeof outputs_computed !== 'undefined' && outputs_computed){
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

    $(document).on('click', 'select + a i', function(event){
        var select = $(this).closest('.control-group, td').find('select');
        modelModal.show(select);
        event.preventDefault();
    });


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
                    cssClass: 'btn-primary',
                    action: function(dialog){
                        $.post($('header form').attr('action'), $('header form').serialize(), function(){dialog.close()});//ajax
                    }
                }
            ]
        });
        return dialog;
    }
}


two_state_button = function(){
    if(typeof outputs_computed === 'undefined' || outputs_computed == false) {
        return 'class="btn btn-primary">Save changes'
    } else {
        return 'class="btn btn-danger">Delete Results and Save Changes'
    }
}


var modelModal = {

    ajax_submit: function($form, url, success_callback, fail_callback){
        return $.ajax({url: url, type: "POST", data: new FormData($form[0]), success: function(data, status, xhr){
            if(typeof(data) == 'object') {
                if (data['status']=='success') { //redundant for now
                    success_callback(data)
                }
            } else {//html dataType  == failure probably validation errors
                fail_callback(data)
            }
        },
        processData: false,
        contentType: false});
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
        var $form = $newForm.find('form:not(.ajax, .admin)').first();
        $form.find('.buttonHolder').remove();
        modal.find('.modal-body').html($form);
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
        if(selectInput.val() != 'data-add-new')
            url = url.replace('new', selectInput.val());//will edit already existing model

        $.get(url, function(newForm){
            var $newForm = $($.parseHTML(newForm));
            var $form = self.populate_modal_body($newForm, modal);
            modal.find('.modal-title').html($newForm.find('#title').html());
            $('body').append(modal);
            $('#id_equation_type').trigger('change'); //see also probability-functions.js
            modal.find('.modal-footer .btn-primary').on('click', function() {
                self.ajax_submit($form, url, self.ajax_success(modal, selectInput), self.validation_error(modal));
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
                        <button type="button"' + two_state_button() + '</button>\
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

