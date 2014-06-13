/** Created by Josiah on 6/13/14. */

$(document).ready( function(){

    $(document).on('change', '#id_equation_type', function(){
        var equation_type = $(this).val()
        var fields = $(this).closest('.control-group').nextAll('.control-group');
        fields.each(function(index, control_group){
            var help_text = $(control_group).find('.help-block').first().text();
            if(help_text.toLowerCase().match(equation_type.toLowerCase())){
                $(control_group).show();
            }
            else {
                $(control_group).hide();
            }
        });
    });
    $('#id_equation_type').trigger('change');

});
