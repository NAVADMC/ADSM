/** Javascript widget designed to make many group assignments as quick and painless as possible.
 * Described in https://github.com/NAVADMC/SpreadModel/issues/77.
 * Used in Disease Spread Assignment and Zone assignment.
 * Possibly could be used in Assigning Progression and Protocols as well.
 * Created by Josiah and Marshall on 6/5/14.
 */
var form_state;
var many_to_many_widget;

(function($){
    $.fn.disableSelection = function() {
        return this
            .attr('unselectable', 'on')
            .css('user-select', 'none')
            .css('-webkit-user-select', 'none')
            .on('selectstart', false);
    };
})(jQuery);


    
check_disable_spread_checboxes = function(){
    var elements = $('table').first().find('tr:first-child th:nth-child(n+3)')
    $(elements).each(function(index){
        var active = $(this).find('input').prop('checked');
        var children = $('table').first().find('tbody tr:nth-child(n) >*:nth-child('+(index+3)+') *, thead tr:nth-child(2) td:nth-child('+(index+3)+') *');
        $(children).each(function(){
            if(active){
                $(this).removeAttr('disabled')
            } else {
                $(this).attr('disabled', 'disabled')
            }
        })
    });
}


function headerify_columns1_2() {
    $('tbody tr td:nth-child(-n+2)').replaceWith(function (i, html) {
        return '<th>' + html + '</th>';
    });
}

$(function(){

//state object
form_state = (function(form){
    var recentClick = {};
    //load done by views.py queryset
    //list Assignments already in DB  //done by views.py
    //serialize -> POST   //standard formset views.py

    var format_form_array = function(serialized_array){
        var row = {};
        $.each(serialized_array, function(index, container){
            var form_prefix = /form-(\d+)-/g;
            var name = container.name.replace(form_prefix, "");
            row[name] = container.value;
            row['form_number'] = form_prefix.exec(container.name)[1];
        });
        return row;
    };

    /*Gets all the rows in the formset that matches 'filters' criteria*/
    var get = function(filters){
        if(typeof filters != "object"){
            throw new TypeError("Must be an object containing, (field, value) pairs");
        }
        var matching_rows = [];
        form.find('tbody tr').each(function(){
            var row_data = format_form_array($(this).find(':input').serializeArray());
            var pass = true;
            $.each( filters, function( key, value ) {
                if(! value instanceof Array){
                    value = [value];//ensure array
                }
                if(!row_data.hasOwnProperty(key))
                    return pass = false;
                else if($.inArray(row_data[key], value) == -1) //key not in value
                    return pass = false;
            })// we have gotten through all filters with matching value == test passed
            if( pass ){
                matching_rows.push(row_data);
            }
        });
        return matching_rows
    };

    var get_consensus = function(filters){
        var matching_rows = get(filters);
        var consensus_row = matching_rows[0];//TODO: handle empty
        $.each(matching_rows, function(row_index, row_values){
            $.each(row_values, function(key, value){
                if(consensus_row[key] != value){ //inconsistency
                    consensus_row[key] = 'differs'
                }
            })
        });
        return consensus_row
    };

    //This will set all rows that meets the filters criteria.  You can pass in multiple input variables
    //to be set in that row.
    var set = function(filters, variables){
        if(typeof filters != "object" || typeof variables != "object"){
            throw new TypeError("Must be an object containing, (field, value) pairs");
        }

        $.each(get(filters), function(index, row){
            var matching_row_number = row['form_number'];
            for(var key in variables){
                var input_name = 'id_form-' + matching_row_number + '-' + key;
                $('#'+input_name).val(variables[key]);
            }
        })
        save();
    };

    var save = debounce(function() {
        $.post('', form.serialize())
    }, 500); //interval = 500 milliseconds

    return {
        'save': save,
        'get':  get,
        'set':  set,
        'get_consensus': get_consensus
    };
})($('section form'));

    
many_to_many_widget = (function(form_state){
    var my_table;
    //render
    //this queries the current state of the Disease object through JSON and sets the checkbox stats to match
    function add_checkboxes_to_headers() {
        $.get('/setup/IncludeSpreads/', function(data){
            my_table.find('tr:first-child th:nth-child(n+3)').each(function(index){
                var field_name = 'include_'+ $(this).text().replace(/ /g, '_').toLowerCase() 
                var myInput = $('<input type="checkbox" name="' + field_name + '">');
                myInput.prop('checked', data[field_name]);
                $(this).html(
                    $('<label class="checkbox">' + $(this).text() + '</label>').prepend(myInput)
                );
                
                myInput.on('change', check_disable_spread_checboxes);
            });
        });
    }
    
    function insert_select_buttons() {
        var select_buttons = '<td><button class="mtm-button select-all">Select All</button>' +
            '<button class="mtm-button deselect">Deselect All</button></td>'
        my_table.find('thead').append($('<tr>').append(select_buttons).append(select_buttons))
    }

    function insert_bulk_selectors() {
        $('section form table tbody tr:last-child td').each(function (index) {
            //headers source and destination are skipped because they are not <td>
            var form_prefix = /form-(\d+)-/g;
            var bulk_select = $(this).find('select').clone()
            bulk_select.attr('id', bulk_select.attr('id').replace(form_prefix, 'bulk-')).val("");
            bulk_select.find('option[value="data-add-new"]').remove()
            var button = $('<button>Apply</button>').addClass('bulk-apply')
            my_table.find('thead tr:nth-child(2)').append($('<td>').append(bulk_select).append(button)); //sensitive selector
        });
    }

    function extract_options(index, element){//grab each option and generate row
        var value = $(element).attr('value');
        if(value && value != 'data-add-new'){//not "-----" or "Add..."
            return [[$(element).text(), value]];
        }
    }

    function render_row(header_information, column_information, row_index){
        var row = $('<tr>')
        for(var col_index in [0,1]){ //list row headers from header_information
            var th = $('<th>').append('<span data-click-toggle="selected" data-pk="'+
                header_information[col_index][row_index][1] + '">' +
                header_information[col_index][row_index][0] + '</span>').disableSelection()
            th.addClass('relevant');
            row.append(th); //column contains row list
        }
        $.each(column_information, function(col_index, column){//for each column
            if(header_information[1][row_index]) //check if there's something in the second column (could be ragged)
                row.append($('<td>').append(column.clone())); // column contains select
            else
                row.append($('<td>'));//blank cell
        })
        return row;
    }

    function create_body_rows() {
        var tbody = $('<tbody>');
        var header_information = [];
        $('section form table tbody tr:last-child th').each(function (index) {
            header_information[index] = $(this).find('option').map(extract_options);
        })

        var column_information = [];
        $('section form table tbody tr:last-child td').each(function (index) {//copy the select
            column_information[index] = $(this).find('select').clone()
                .val('').removeAttr('id');
        });

        var num_rows = Math.max(header_information[0].length, header_information[1].length);
        for (var i = 0; i < num_rows; i++) {
            tbody.append(render_row(header_information, column_information, i));
        }
        return tbody;
    }

    function get_column_name(column_index){
        var print = $('section form table thead tr:nth-child(1) th:nth-child('+column_index+')').text()
        return print.toLowerCase().replace(/\s/g, "_")
    }

    var render = function(){
        my_table = $('<table>').append($('section form table thead').clone());
        add_checkboxes_to_headers();
        insert_select_buttons();
        insert_bulk_selectors();
        my_table.append(create_body_rows())
        update_display_inputs() //called from events normally, but we want to initialize

        $('.panel').before(my_table); //finally, insert everything into the DOM
        my_table.find('tbody select').on('change', update_state_inputs)//register event listener
    };

    /*Creates a filter using any selected items from the first column and the matching row header
    on the second column. */
    var construct_filter = function (row) {
        var filter = {};
        var sources_selected = $('tbody th:first-child .selected').map(function(){return $(this).attr('data-pk')});
        filter[get_column_name(1)] = sources_selected.length ? sources_selected :
            [$(row).find('th:first-child span').attr('data-pk')];
        filter[get_column_name(2)] = [$(row).find('th:nth-child(2) span').attr('data-pk')];
        return filter
    };

    /*Ensures that the state of the displayed widget is consistent with form_state for the appropriate
    * row / column pairs.*/
    function update_display_inputs(){
        my_table.find('tbody tr').each(function(row_index, row){
            var filter = construct_filter(row)
            var row_values = form_state.get_consensus(filter);
            $(row).find('td').each(function(column_index, column){
                var column_name = get_column_name(column_index+3);//+3 = +1 (not zero indexed) + 2 for the two row headers
                $(column).find('select option.differs').remove();
                if(row_values[column_name] == 'differs'){
                    $(column).find('select').append('<option class="differs" value="differs">- Differs -</option>');
                }
                $(column).find(':input').val(row_values[column_name]); //set the select to the matching formset select
            })
        })
    };

    function update_state_inputs(){
        var filters = construct_filter($(this).closest('tr'))
        var col_name = get_column_name($(this).closest('td').index()+1)
        var values = {} //we have to wrap it for a variable dict key
        values[col_name] = $(this).val() // variable key name
        form_state.set(filters, values)
    }

    //bulk apply
    function bulk_apply($bulk_selector){
        var column_number = $bulk_selector.closest('td').index() + 1
        var destinations_selected = $('tbody th:nth-child(2) .selected')
        if( !destinations_selected.length )//empty =>  Drop .selected criteria and treat the whole column as selected
            $bulk_selector.closest('table').find('tbody tr :nth-child('+column_number+') :input')
                .val($bulk_selector.val()).trigger('change'); //set all values in the whole column
        else{
            $bulk_selector.closest('table').find('tbody tr').each(function(){ //for each row
                if($(this).find('th:nth-child(2) .selected').length)   //if destination .selected
                    $(this).find('td:nth-child('+column_number+') :input')  //set the input value
                        .val($bulk_selector.val()).trigger('change');
            })
        }
    }

    //draw arrows

    function highlight_hints_events() {
        function highlight_source_if_blank() {
            var sources_selected = $('tbody th:first-child .selected')
            return sources_selected.length ? '' : '-n+'; //will also select the first column
        }

        $(document).on('mouseover', 'tbody td', function () {
            var row = $(this).closest('tr');
            $(row).find('th:nth-child('+highlight_source_if_blank()+'2) span').addClass('highlight');
            var second_column = my_table.find('tbody th:nth-child(2)');
            second_column.removeClass('relevant');
        });
        $(document).on('mouseout', 'tbody td', function () {
            var row = $(this).closest('tr');
            $(row).find('th:nth-child('+highlight_source_if_blank()+'2) span').removeClass('highlight')
            var second_column = my_table.find('tbody th:nth-child(2)');
            second_column.addClass('relevant');
        });
    }

    function register_event_hooks(){
        /*EVENT HOOKS*/
        var prev_click;
        $(document).on('click', '[data-click-toggle]', function(event){ //update every click
            if(event.shiftKey && prev_click) { //Shift-Click
                var col_index = $(this).closest('th').index() + 1;
                if(col_index == $(prev_click).closest('th').index() + 1){//verify they're in the same column
                    var j = $(prev_click).closest('tr').index(); //row numbers
                    var k = $(this).closest('tr').index();
                    var start_row = Math.min(j,k) + 1;
                    var end_row = Math.max(j,k) + 1;
                    /*nth-child range  nth-child(n+4):nth-child(-n+8)
                    * everything between previous click and index of current shift+click */
                    var rows = $('tbody tr:nth-child(n+'+start_row+'):nth-child(-n+'+end_row+') th:nth-child('+col_index+') span');
                    rows.addClass('selected');
                    console.log(col_index, start_row, end_row, rows);
                }
             }
            many_to_many_widget.update_display_inputs();
            prev_click = this;
        });
        $(document).on('change', 'thead select', function(){ //update every click
            many_to_many_widget.bulk_apply($(this));
        });

        $(document).on('click', 'button.select-all', function(){
            var col = $(this).closest('td').index()+1;
            $(this).closest('table').find('tbody tr :nth-child('+col+') span').addClass('selected')
            many_to_many_widget.update_display_inputs();
        })
        $(document).on('click', 'button.deselect', function(){
            var col = $(this).closest('td').index()+1;
            $(this).closest('table').find('tbody tr :nth-child('+col+') span').removeClass('selected')
            many_to_many_widget.update_display_inputs();
        })
        $(document).on('click', 'button.bulk-apply', function(){
            var selector = $(this).closest('td').find('select');
            console.log(selector);
            $(selector).trigger('change');
        })

        highlight_hints_events();
    }

    return {
        'render': render,
        'get_column_name': get_column_name,
        'update_display_inputs': update_display_inputs,
        'bulk_apply': bulk_apply,
        'update_state_inputs': update_state_inputs,
        'register_event_hooks': register_event_hooks
    }
})(form_state)

    headerify_columns1_2();
    many_to_many_widget.render();
    many_to_many_widget.register_event_hooks();

});

