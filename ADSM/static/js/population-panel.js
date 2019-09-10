/** Created by Josiah on 2/18/2015. */

function toggle(element, attribute){
    if($(element).prop(attribute) || $(element).attr(attribute)) {
        $(element).prop(attribute, false);
        $(element).removeAttr(attribute, false);
    } else {
        $(element).prop(attribute, true);
        $(element).attr(attribute, attribute);
    }

}

function toggle_added_state(text) {
    $('#ProductionTypes li').filter(function () {
        return $(this).find('.pt-name').text() == text;  // must be an exact match NOT :contains()
    }).toggleClass('pt-added');  // for styling rows that have already been added
}

function select_production_type(text) {
    var selectors = ['.productiontypelist.focus option', '.grouplist option'];
    $.each(selectors, function(index, selector){
        $(selector).each(function() {
            if ($(this).text() == text) {
                toggle(this, 'selected')
                $(this).closest('.layout-panel').find('.btn-save').removeAttr('disabled'); //unsaved changes
                $(this).closest('.layout-panel').find('.fragment').addClass('scrollbar-danger'); //unsaved changes
                document.getElementById("unsaved-form-header").classList.remove('hidden'); //unsaved changes
            }
        })
    });
    toggle_added_state(text);
}

$(document).on('mousedown', '#ProductionTypes li, #ProductionGroups li, .productiontypelist option', function(event){
    //It's really critical this is mousedown and not click.  the default mousedown event behavior deselects all the other options
    event.preventDefault()
    var text = $(this).text();
    if(this.tagName == 'LI'){  // I want the click target to be the whole row, but the name is defined in pt-name
        text = $(this).find('.pt-name, .pt-group-name').text();
    }
    select_production_type(text)
})

$('.productiontypelist, .grouplist').livequery(function(){
    // clears old data
    $('#ProductionTypes li').removeClass('pt-added');
    $('.productiontypelist').removeClass('focus');
})

$(document).on('focus', '.productiontypelist', function (event) {
    $('.productiontypelist.focus').removeClass('focus');
    $(this).addClass('focus');

    $('#ProductionTypes li').removeClass('pt-added');
    $(this).find('option[selected]').each(function (index, element) {
        $('#ProductionTypes li').filter(function () {
            return $(this).find('.pt-name').text() == $(element).text();  // must be an exact match NOT :contains()
        }).addClass('pt-added');  // for styling rows that have already been added
    })
});

$(document).on('blur', '.productiontypelist', function (event) {
    $('.productiontypelist.focus').removeClass('focus');
    $('#ProductionTypes li').removeClass('pt-added');
});
