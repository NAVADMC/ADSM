/**
 * Created by Josiah on 2/18/2015.
 */

function toggle(element, attribute){
    if($(element).attr(attribute)) {
        $(element).attr(attribute, false);
    } else {
        $(element).attr(attribute, attribute);
    }
}

function select_production_type(text) { // consider using value=3 instead of text... could be unstable
    $('.production_list option').each(function(text) {
        if ($(this).text() == text) {
            toggle(this, 'selected')
        }
    })
}

$('.production_list option[value=2]').removeAttr('selected')