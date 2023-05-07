$.Admin = {};

$.Admin.formset = {
  init: function() {
      var _this = this;
      var $formset_box = $('.formset-box');

      $formset_box.each(function(){
          var currentBox = $(this);
          var formsetPrefix = currentBox.find('.formset:last').prop('id');
          var nFormsets = (parseInt(formsetPrefix.substring(formsetPrefix.indexOf('-') + 1), 10) + 1).toString();

          formsetPrefix = formsetPrefix.substring(0, formsetPrefix.indexOf('-'));

          //Esconder campo DELETE do Django
          currentBox.find('.formset').each(function(){
              _this.hideDeleteField($(this))
          });

          //Esconder botao adicionar novo dos formularios, excluindo o ultimo
          currentBox.find('.formset:not(:last)').each(function(){
              $(this).find('.add-formset').hide();
          });

          //Adicionar novo formset
          currentBox.on('click', '.add-formset', function(e){
              e.preventDefault();
              var parentFormset = $(this).parents('.formset');
              _this.createNewForm(parentFormset, nFormsets);

              //Adicionar form ao manager
              nFormsets++;
              $('#id_' + formsetPrefix + '-TOTAL_FORMS').val(nFormsets);

              //Esconder add e remove do penultimo form
              $(this).hide();
              parentFormset.next().trigger('formCreated');
          });

          //Remover formset
          currentBox.on('click', '.remove-formset', function(e){
              e.preventDefault();
              var parentFormset = $(this).parents('.formset');
              var entryId = parentFormset.find('input:hidden[id $="-id"],input:hidden[id $="grupo_ptr"]');

              if(entryId.length){
                  parentFormset.find('input:checkbox[id $="-DELETE"]').prop('checked', true);
              }else{
                  parentFormset.find(':input').each(function(){
                      $(this).prop({'value': ''}).val('').prop('checked',false);
                  });
                  parentFormset.find('input:checkbox[id $="-DELETE"]').prop('checked', true);
                  parentFormset.trigger('newFormRemoved');
              }
              parentFormset.hide().change();

              var addBtn = currentBox.find('.formset:visible:last .add-formset');

              if(!addBtn.length){
                  _this.createNewForm(parentFormset, nFormsets);
                  //Adicionar form ao manager
                  nFormsets++;
                  $('#id_' + formsetPrefix + '-TOTAL_FORMS').val(nFormsets);
              }else{
                  addBtn.show();
              }

              parentFormset.trigger('formRemoved');
          });
      });
  },

  hideDeleteField: function(formset){
      var delete_input = formset.find('input:checkbox[id $="-DELETE"]');
      var delete_td = delete_input.parent('.field-td');

      delete_input.parents('.form-group:first').parent('div').hide();

      delete_td.closest('table').find('th').eq(delete_td.index()).hide();
      delete_td.hide();
  },

  createNewForm: function(parentFormset, nFormsets){
      var newForm = parentFormset.clone(true);

      //Trocar id
      var nameRegex = /-\d+-?/g;
      var newId = newForm.prop('id').replace(nameRegex, '-' + (nFormsets));
      newForm.prop({'id':newId});

      //Trocar names e ids dos inputs
      newForm.find(':input').each(function(){
          var newName = $(this).prop('name');
          if($(this).prop('type') == 'hidden'){
              $(this).remove();
          }
          //Remover mask do clone, senao nao funciona com novos inputs!
          $(this).removeData('mask');

          if(newName){
              newName = newName.replace(nameRegex, '-' + (nFormsets) + '-');
              var newId = 'id_' + newName;
              $(this).prop({'name': newName, 'id': newId, 'value': ''}).val('');

              if($(this).prop('type') == 'checkbox'){
                  $(this).prop({'checked': false}).removeProp('value').removeAttr('value');
              }
          }

      });

      //Trocar atributos for dos labels
      newForm.find('label').each(function() {
          var newFor = $(this).prop('for');
          if(newFor){
              newFor = newFor.replace(nameRegex,'-' + nFormsets + '-');
              $(this).prop({'for': newFor});
          }

          if($(this).hasClass('error')){
              $(this).remove();
          }
      });
      newForm.show();
      newForm.insertAfter(parentFormset);
  },
}