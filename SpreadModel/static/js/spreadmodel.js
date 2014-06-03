
$(function(){
    $(document).on('mousedown', '[data-new-item-url]', function(e){
            $(this).prop('last-selected', $(this).val()); // cache old selection
    });
    $(document).on('change', '[data-new-item-url]', function(e){
        if ($(this).val() == "data-add-new") {
            e.preventDefault();
            $(this).val($(this).prop('last-selected')); //undo selection
            modelModal.show($(this));
        }
    });

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
            console.log('ajax_success', modal, selectInput, data);
            $('select[data-new-item-url="' + selectInput.attr('data-new-item-url') + '"] [value="data-add-new"]')
                .before($('<option value="'+data['pk']+'">'+data['title'] + '</option>')); // Add option to all similar selects
            selectInput.val(data['pk']); // select option for select that was originally clicked
            modal.modal('hide');
        };
    },

    validation_error: function(modal){
        return function(data) {
            console.log('validation_error', modal, data)
            var $form = $(data).find('form');
            $form.find('button[type=submit]').remove();
            modal.find('.modal-body').html($form);
        }
    },

    show: function(selectInput) {
        var self = this;
        var modal = this.template.clone();
        modal.attr('id', selectInput.attr('name') + '_modal');
        var url = selectInput.attr('data-new-item-url');
        $.get(url, function(newForm){
            var $newForm = $($.parseHTML(newForm));

            modal.find('.modal-title').html($newForm.find('#title').html());
            var $form = $newForm.not('header, nav').find('form');
            $form.find('.buttonHolder').remove();
            modal.find('.modal-body').html($form);
            $('body').append(modal);
            modal.find('.modal-footer .btn-primary').on('click', function() {
                self.ajax_submit($form, url, self.ajax_success(modal, selectInput), self.validation_error(modal));
            });

            modal.modal('show');
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
                        <button type="button" class="btn btn-primary">Save changes</button>\
                      </div>\
                    </div>\
                  </div>\
                </div>')
}

/*Utility function for getting a GET parameter from the current URL*/
function getQueryParam(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}


/* This watches for the first column select which determines what the Farms are being filtered by.
It inserts a new row from the example templates with the correct value and input types.  Values of
these selects are used below to construct a query URL. */
$(document).on('change', '#farm_filter td:first-child select', function(){
    if( $(this).val() ){
        $(this).parents('tr').before($('#farm_filter_templates #' + $(this).val()).clone());
        $('#farm_filter option[value=' + $(this).val() +']').attr("disabled","disabled");
    }

    if( !$(this).parents('tr').is(':last-child') ){
        var my_row = $(this).parents('tr')
        var prev_val = my_row.attr('id') //re-enable filter option after it's removed
        $('#farm_filter option[value=' + prev_val +']').removeAttr("disabled");
        my_row.remove();
    }
    else{
        $(this).val('')
    }
});


/*Construct a query URL based on the value of the filter selects.  Two major types are
* 1) choice selects = fairly simple
* 2) numeric input = have both min and max fields and require additional handling*/
var population_filter_string = function(){
    var filters = $('#farm_filter tr').map(function(){
        if($(this).find('td:nth-child(3) select').length) { //state select field
            var str = $(this).attr('id') + '=' + $(this).find('td:nth-child(3) select').val(); //must be a select
            return str.replace(/ /g, '%20'); // global replace
        }
        else { //this must be a numeric filter, because of the input field
            var name = $(this).attr('id');
            var minimum = $(this).find('td:nth-child(3) input').val() ? //empty string if no value
                name + '__gte=' + $(this).find('td:nth-child(3) input').val() : '';
            var maximum = $(this).find('td:nth-child(5) input').val() ? //empty string if no value
                name + '__lte=' + $(this).find('td:nth-child(5) input').val() : '';
            if(minimum.length && maximum.length) //if both are present, we need to stick an & between them
                return minimum + "&" + maximum;
            else
                return  minimum + maximum; // return one or the other or a blank string if neither
        }
    });
    var new_url = filters.get().join('&');
    return new_url;
}

/*Updates the page and URL with the latest filter and sort settings.*/
function update_population_filter_and_sort(sort_by) {
    if(sort_by === undefined){ //try and find it in the URL
        var sorting = window.location.getParameter('sort_by') ?
            'sort_by=' + window.location.getParameter('sort_by') : '';//TODO: Bug: loses previous state somehow #95
    } else{ //sort_by already provided
        var sorting = 'sort_by=' + sort_by;
    }
    var new_url = '?' + population_filter_string();//build URL
    new_url = new_url + sorting;
    //get it with AJAX and insert new HTML with load()
    window.history.replaceState('', 'Population Filters', new_url); //TODO Bug: update URL bar state
    $('#farm_list').parent().load(new_url + ' #farm_list');
}

$(document).on('change', '#farm_filter select, #farm_filter input', function(){
    update_population_filter_and_sort();
});

$(document).on('click', '#farm_list .sortControls a', function(event){
    update_population_filter_and_sort($(this).attr('data-sort-by'));
    event.preventDefault()
});
