/** Created by Josiah on 6/13/14. */

$(document).ready( function(){

    $(document).on('change', '#id_equation_type', function(){
        var equation_type = $(this).val()
        var fields = $(this).closest('.control-group').nextAll('.control-group');
        fields.each(function(index, control_group){
            var help_text = $(control_group).find('.help-block').first().text();
            var functions = help_text.toLowerCase().match(/(\w[\w\s]*)(?=[,\.])/g);
            if(functions.indexOf(equation_type.toLowerCase()) >= 0){
                $(control_group).show();
                $(control_group).find(':input').attr('required', 'required');
            }
            else {
                $(control_group).hide();
                $(control_group).find(':input').removeAttr('required');
            }
        });
    });
    $('#id_equation_type').trigger('change');

});