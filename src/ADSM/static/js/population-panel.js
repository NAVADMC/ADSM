/** Created by Josiah on 2/18/2015. */

function toggle(element, attribute){
    if($(element).attr(attribute)) {
        $(element).removeAttr(attribute, false);
    } else {
        $(element).attr(attribute, attribute);
    }
}

function check_empty_status(self) {
    var $self = $(self)
    if($self.find('option[selected]').length == 0) { //empty
        $self.addClass('empty')
    } else {
        $self.removeClass('empty')
    }
}

function select_production_type(text, selector) { 
    $(selector).each(function() {
        if ($(this).text() == text) {
            toggle(this, 'selected')
        }
    })
    check_empty_status($(selector).first().closest('.productiontypelist'));
}

//child has selected attr, then remove .empty  has .productiontypelist
//on load have .empty
//editing existing 

$(document).on('load', '.productiontypelist, .grouplist', function(event){
    check_empty_status(this)
})

$(document).on('focus', '.productiontypelist', function(event){
    production_type_list_last_clicked = '#' + $(this).attr('id')
})

$(document).on('click', '#population_panel #ProductionTypes a, .productiontypelist option', function(event){
    event.preventDefault()
    if($('.productiontypelist').length > 1 && typeof production_type_list_last_clicked !== 'undefined'){
        select_production_type($(this).text(), production_type_list_last_clicked + ' option')
    }else{
        select_production_type($(this).text(), '.productiontypelist option')
    }
})

$(document).on('click', '#population_panel #ProductionGroups a, .productiontypelist option', function(event){
    event.preventDefault()
    select_production_type($(this).text(), '.grouplist option')
})
