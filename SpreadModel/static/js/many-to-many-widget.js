/** Javascript widget designed to make many group assignments as quick and painless as possible.
 * Described in https://github.com/NAVADMC/SpreadModel/issues/77.
 * Used in Disease Spread Assignment and Zone assignment.
 * Possibly could be used in Assigning Progression and Protocols as well.
 * Created by Josiah and Marshall on 6/5/14.
 */
var form_state;

$(function(){

//state object
form_state = (function(form){
    var state = {};
    //load done by views.py queryset
    //list Assignments already in DB
    //serialize -> POST
    //get(source destination)
    var flatten_form_array = function(serialized_array){
        var row = {};
        $.each(serialized_array, function(index, container){
            var name = container.name.replace(/form-\d+-/g, "")
            row[name] = container.value;
        });
        return row;
    };

    var get = function(filters){
        if(typeof filters != "object"){
            throw new TypeError("Must be an object containing, (field, value) pairs");
        }
        var matching_row;
        form.find('tbody tr').each(function(){
            var row_data = flatten_form_array($(this).find(':input').serializeArray());
            var pass = true;
            $.each( filters, function( key, value ) {
                if(!row_data.hasOwnProperty(key))
                    return pass = false;
                else if(row_data[key] != value)
                    return pass = false;
            })// we have gotten through all filters with matching value == test passed
            if( pass ){
                matching_row = row_data;
                return false; //break
            }
        });
        return matching_row
    };
    //set [sources, destinations]
    var set = function(){};

    return {
        'save': function(){$.post('', form.serialize())},
        'get':  get,
        'set':  set
    };
})($('section form'));

//widget
    //jquery events
        //select change
    //render row
    //bulk apply
    //select source
    //select destination
    //draw arrows




});



























