$(function(){
    $('body').on('click', '.btn-add', function(){
        var $selector = $($(this).attr('rel'));
        var model = $selector.attr('name'); // field name
        modelModal.show(model, $selector);
    })
})

var modelModal = {

    ajax_submit: function($form, url, callback){
        console.log($form, url, callback);
        return $.post(url, $form.serialize(), callback);
    },

    update_contents: function(data){
        console.log(data);
    },

    show: function(model, selectInput) {
        var self = this;
        var modal = this.template.clone();
        modal.attr('id', model+'_modal');
        var url = selectInput.attr('data-new-item-url');
        $.get(url, function(newForm){
            var $newForm = $($.parseHTML(newForm));
            modal.find('.modal-title').html($newForm.find('h1:not(.filename)').html());
            var $form = $newForm.find('form');
            $form.find('button[type=submit]').remove();
            modal.find('.modal-body').html($form);
            $('body').append(modal);
            modal.find('.modal-footer .btn-primary').on('click', function() {
                self.ajax_submit($form, url, self.update_contents)});
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
                      </div>\
                      <div class="modal-footer">\
                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\
                        <button type="button" class="btn btn-primary">Save changes</button>\
                      </div>\
                    </div>\
                  </div>\
                </div>')
}