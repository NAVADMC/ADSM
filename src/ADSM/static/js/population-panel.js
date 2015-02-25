/** Created by Josiah on 2/18/2015. */

function toggle(element, attribute){
    if($(element).attr(attribute)) {
        $(element).attr(attribute, false);
    } else {
        $(element).attr(attribute, attribute);
    }
}

function check_empty_status(self) {
    var $self = $(self)
    if($self.find('input[checked]').length == 0) { //empty
        $self.addClass('empty')
    } else {
        $self.removeClass('empty')
    }
}

function select_production_type(text, selector) { 
    $(selector).each(function() {
        if ($(this).attr('name') == text) {
            toggle(this, 'checked')
        }
    })
    check_empty_status($(selector).first().closest('.production_list'));
}

//$('.production_list option[value=2]').removeAttr('selected')

//child has selected attr, then remove .empty  has .production_list
//on load have .empty
//editing existing 

$(document).on('load', '.production_list, .group_list', function(event){
    check_empty_status(this)
})

$(document).on('click', '#population_panel #ProductionTypes a', function(event){
    event.preventDefault()
    select_production_type($(this).text(), '.production_list input')
})

$(document).on('click', '#population_panel #ProductionGroups a', function(event){
    event.preventDefault()
    select_production_type($(this).text(), '.group_list input')
})
