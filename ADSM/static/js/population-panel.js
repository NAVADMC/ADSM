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

$(document).on('click', '#ProductionTypes li, .productiontypelist option', function(event){
    event.preventDefault()
    var text = $(this).text();
    if(this.tagName == 'LI'){  // I want the click target to be the whole row, but the name is defined in pt-name
        text = $(this).find('.pt-name').text();
    }
    select_production_type(text, '.productiontypelist option')
})

$(document).on('click', '#ProductionGroups li, .productiontypelist option', function(event){
    event.preventDefault()
    var text = $(this).text();
    if(this.tagName == 'LI'){  // I want the click target to be the whole row, but the name is defined in pt-name
        text = $(this).find('.pt-name').text();
    }
    select_production_type(text, '.grouplist option')
})
