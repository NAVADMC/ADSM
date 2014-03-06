$(function(){
    $('.btn-add').on('click', function(){
        var $selector = $($(this).attr('rel'));
        var model = $selector.attr('name'); // field name
        modelModal.show(model, $selector);
    })
})

var modelModal = {
    show: function(model, selectInput) {
        var modal = this.template.clone();
        modal.attr('id', model+'_modal');
        $.get(selectInput.attr('data-new-item-url'), function(newForm){
            $newForm = $($.parseHTML(newForm));
            modal.find('.modal-title').html($newForm.find('h1:not(.filename)').html());
            modal.find('.modal-body').html($newForm.find('form'));
            $('body').append(modal);
            modal.modal('show');
        })

        },
    template: $('<div class="modal fade">\
                  <div class="modal-dialog">\
                    <div class="modal-content">\
                      <div class="modal-header">\
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
                        <h4 class="modal-title">Modal title</h4>\
                      </div>\
                      <div class="modal-body">\
                        <p>One fine body&hellip;</p>\
                      </div>\
                      <div class="modal-footer">\
                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\
                        <button type="button" class="btn btn-primary">Save changes</button>\
                      </div>\
                    </div>\
                  </div>\
                </div>')
}