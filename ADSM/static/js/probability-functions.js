/** Created by Josiah on 6/13/14. */

function hide_unneeded_probability_fields() {
    var $idEquationType = $('#id_equation_type');
    var equation_type = $idEquationType.val()
    var fields = $idEquationType.closest('.control-group').nextAll('.control-group');
    fields.each(function (index, control_group) {
        var help_text = $(control_group).find('.help-block').first().text();
        var functions = help_text.toLowerCase().match(/(\w[\w\s]*)(?=[,\.])/g);
        if (functions.indexOf(equation_type.toLowerCase()) >= 0) {
            $(control_group).show();
            $(control_group).find(':input').attr('required', 'required');
        }
        else {
            $(control_group).hide();
            $(control_group).find(':input').removeAttr('required');
        }
    });
}

$(document).ready( function(){

    $(document).on('change', '#id_equation_type', function(){
        hide_unneeded_probability_fields();
    });
    hide_unneeded_probability_fields();


    $(document).on('click', '.edit-button', function(){
        $('#functions_panel .buttonHolder').removeAttr('hidden')
        $('.edit-button-holder a, .edit-button-holder button').addClass('reveal')
        //$('#population_grid_wraper').css('height', 'calc(100vh - 123px')
        //$('#edit-mask').css('visibility', 'visible')
        //$('#farm_list tbody').css('height', 'calc(100vh - 214px)')
        //$('.edit-button').css('display', 'none') //TODO: fold out transition
        $('#functions_panel, #functions_panel input').addClass('editable')
        $('#functions_panel :input').addClass('editable')
        //$('#tb_mask').css('visibility', 'visible')
        $('#functions_panel').css('pointer-events','all') //TODO: necessary?
    })
});
