
$(function(){
    $('body').on('click', '.btn-add', function(){
        var $selector = $($(this).attr('rel'));
        var model = $selector.attr('name'); // field name
        modelModal.show(model, $selector);
    })

    $('[data-toggle-controller]').each(function(){
        var controller = '[name=' + $(this).attr('data-toggle-controller') + ']'
        var hide_target = $(this).parents('.control-group')
        var required_value = $(this).attr('data-required-value') || 'True'
        $('body').on('change', controller, function(){
            if($(this).val() == required_value){
                hide_target.show()
            }else{
                hide_target.hide()
            }
        }).trigger('change')  //TODO: this doesn't trigger on page load properly
    })

    $("#open_file").change(function(){
        $(this).parent('form').submit();
    })

    $('[data-remove-file]').click(function(){
        var filename = $(this).attr('data-remove-file')
        var link = '/setup/DeleteScenario/' + filename
        var dialog = new BootstrapDialog.show({
            title: 'Delete Scenario Confirmation',
            type: BootstrapDialog.TYPE_WARNING,
            message: 'Are you sure you want to delete <strong>' + filename + '</strong>?',
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
                        window.location = link;
                    }
                }
            ]
        });
    })

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
                        $('header form').submit();
                    }
                }
            ]
        });
    }
}


var modelModal = {

    ajax_submit: function($form, url, success_callback, fail_callback){
        return $.post(url, $form.serialize(), function(data, status, xhr){
            if(typeof(data) == 'object') {
                if (data['status']=='success') { //redundant for now
                    success_callback(data)
                }
            } else {//html dataType  == failure probably validation errors
                fail_callback(data)
            }
        });
    },

    ajax_success: function(modal, selectInput){
        return function(data) {
            console.log('ajax_success', modal, selectInput, data)
            selectInput.find('option').removeAttr('selected');
            selectInput.append($('<option value="'+data['pk']+'" selected>'+data['title'] + '</option>'));// update original select input
            modal.modal('hide');// close modal
        }
    },

    validation_error: function(modal){
        return function(data) {
            console.log('validation_error', modal, data)
            var $form = $(data).find('form');
            $form.find('button[type=submit]').remove();
            modal.find('.modal-body').html($form);
        }
    },

    show: function(model, selectInput) {
        var self = this;
        var modal = this.template.clone();
        modal.attr('id', model+'_modal');
        var url = selectInput.attr('data-new-item-url');
        $.get(url, function(newForm){
            var $newForm = $($.parseHTML(newForm));

            modal.find('.modal-title').html($newForm.find('#title').html());
            console.log($newForm)
            var $form = $newForm.not('header, nav').find('form');
            $form.find('.buttonHolder').remove();
            modal.find('.modal-body').html($form);
            $('body').append(modal);
            modal.find('.modal-footer .btn-primary').on('click', function() {
                self.ajax_submit($form, url, self.ajax_success(modal, selectInput), self.validation_error(modal));
            });

            modal.modal('show');
        })

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
                        <button type="button" class="btn btn-primary">Save changes</button>\
                      </div>\
                    </div>\
                  </div>\
                </div>')
}

//This adds the getParameter utility to the window.location prototype
if (!window.location.getParameter ) {
    window.location.getParameter = function(key) {
        function parseParams() {
            var params = {},
                e,
                a = /\+/g,  // Regex for replacing addition symbol with a space
                r = /([^&=]+)=?([^&]*)/g,
                d = function (s) { return decodeURIComponent(s.replace(a, " ")); },
                q = window.location.search.substring(1);

            while (e = r.exec(q))
                if (typeof params[d(e[1])] == 'array') params[d(e[1])].push(d(e[2]))
                else if (params[d(e[1])]) params[d(e[1])] = [params[d(e[1])],d(e[2])]
                else params[d(e[1])] = d(e[2]);

            return params;
        }

        if (!this.queryStringParams)
            this.queryStringParams = parseParams();

        if (key) return this.queryStringParams[key];
        else return this.queryStringParams;
    };
}
