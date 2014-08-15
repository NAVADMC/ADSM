/**
 * Created by Josiah on 8/15/14.
 */

$(function(){
    $('.zone_grid_cell').each(function(){
        var pk = $(this).find('p').text()
        var form = $(this).find('form')
        var selector = $(this).find('select')
        $(selector).change(function(event){
            $.post('/setup/ZoneEffectAssignment/'+ pk +'/', form.serialize() );  // ajax
        })
    })
});