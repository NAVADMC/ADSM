/** Created by Josiah on 2/18/2015. */

function toggle(element, attribute){
    if($(element).attr(attribute)) {
        $(element).attr(attribute, false);
    } else {
        $(element).attr(attribute, attribute);
    }
}

function select_production_type(text, selector) { 
    $(selector).each(function() {
        if ($(this).text() == text) {
            toggle(this, 'selected')
        }
    })
}

//$('.production_list option[value=2]').removeAttr('selected')


$(document).on('click', '#population_panel #ProductionTypes a', function(event){
    event.preventDefault()
    select_production_type($(this).text(), '.production_list option')
})

$(document).on('click', '#population_panel #ProductionGroups a', function(event){
    event.preventDefault()
    select_production_type($(this).text(), '.group_list option')
})
