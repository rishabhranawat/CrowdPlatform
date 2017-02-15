
/* $('.item-bon').click(function(){
        alert("clicked")
      }
        );
      function deleteItem(itemType, itemId, lessonId, itemGroup) {
        $.ajax({
          type:"POST",
          url:'http://{{ request.get_host }}/create_lesson_plan/remove_from_lp/',
          data: {
            'itemType':itemType,
            'itemId':itemId,
            'lessonId':lessonId,
            'itemGroup':itemGroup
          },
          success: function(msg) {
            alert('yes ' + msg)
            if (itemType == 'url') {
              $('#' + itemGroup + '_' + itemId + '_row').remove()
            } else if (itemType == 'img') {
              $('#' + itemGroup + '_' + itemId + '_imgrow').remove()
            }
          }

        })
      }*/
     
        $('.item-delete').click(function() {
          alert('Hello world')
        var lessonId = $('.lesson_plan_id').attr('id')
        var itemId = ""
        var itemType = ""
        var itemGroup = ""
        console.log(lessonId)
        if ($(this).attr('id').indexOf('engage') > -1) {
          itemGroup = 'engage'
          itemId = $(this).attr('id').replace('engage_','').replace('_img','')
        } else if ($(this).attr('id').indexOf('explain') > -1) {
          itemGroup = 'explain'
          itemId = $(this).attr('id').replace('explain_','').replace('_img','')
        } else if ($(this).attr('id').indexOf('evaluate') > -1) {
          itemGroup = 'evaluate'
          itemId = $(this).attr('id').replace('evaluate_','').replace('_img','')
        } else if ($(this).attr('id').indexOf('document') > -1) {
          itemGroup = 'document'
          itemId = $(this).attr('id').replace('document_','').replace('_img','')
        } else if ($(this).attr('id').indexOf('pic') > -1) {
          itemGroup = 'pic'
          itemId = $(this).attr('id').replace('pic_','').replace('_img','')
        } 

        if ($(this).hasClass('link_item')) {
          itemType = "url"
        } else if ($(this).hasClass('img_item')) {
          itemType = "img"
        }

        alert('lesson_plan_id is ' + lessonId + '\nitem type is ' + itemType + '\nitem group is ' + itemGroup + '\nitem id is ' + itemId)
        
        var name_url = itemGroup+'url_'+itemId
        var name_desc = itemGroup+'desc_'+itemId
        console.log(name_url," ",name_desc)
      
        $('#'+name_url).val("none")
        $('#'+name_url).val("none")
        $('#'+name_desc).val("none")
        $('#'+name_desc).val("none")
         var url =  $('#'+name_desc).val()
        //console.log($('input[name= name_url]').attr("name"))
        alert('sure ')       
        $('#' + itemGroup + '_' + itemId + '_row').remove()
       // var delete_existing = deleteItem(itemType, itemId, lessonId, itemGroup)
        /*$(this).attr('name','none')
        $(this).attr('id','none')*/
        /*if (~deleteItem(itemType, itemId, lessonId, itemGroup)) {
           $('#' + itemGroup + '_' + itemId + '_row').remove()
        }*/
        
        return false
      });
      $('.item-up').click(function(){
         
        var itemGroup=""
        var itemId=0

         if ($(this).attr('id').indexOf('engage') > -1) {
          itemGroup = 'engage'
          itemId = parseInt($(this).attr('id').replace('engage_','').replace('_up',''))
        } else if ($(this).attr('id').indexOf('explain') > -1) {
          itemGroup = 'explain'
          itemId = parseInt($(this).attr('id').replace('explain_','').replace('_up',''))
        } else if ($(this).attr('id').indexOf('evaluate') > -1) {
          itemGroup = 'evaluate'
          itemId = parseInt($(this).attr('id').replace('evaluate_','').replace('_up',''))
        }
        alert('check '+itemId) 
        up=itemId-1
        url_up = itemGroup+'url_'+(up).toString()
          while($( up>=0 && "#"+url_up).val()=="none" ){
            up=up-1
            url_up = itemGroup+'url_'+(up).toString()
          }
        alert("not none"+up)
        if(itemId>0 && up>=0){
          var name_row=itemGroup+'_'+itemId.toString()+'_row'
          
          var name_row_up=itemGroup+'_'+(up).toString()+'_row'
          $('#'+name_row).after($('#'+name_row_up))
          var name_url = itemGroup+'url_'+itemId.toString()
          var name_desc = itemGroup+'desc_'+itemId.toString()
          var name_url_up = itemGroup+'url_'+(up).toString()
          var name_desc_up = itemGroup+'desc_'+(up).toString()
          var name_delete= name_row.replace('_row','')
          var name_delete_up = name_row_up.replace('_row','')
          var name_up=name_row.replace('row','up')
          var name_up_up=name_row_up.replace('row','up')
          var name_down=name_row.replace('row','down')
          var name_down_up=name_row_up.replace('row','down')
          var row=$('#'+name_row)
          var row_up =$('#'+name_row_up)
          var url=$('#'+name_url)
          var desc=$('#'+name_desc)
          var url_up=$('#'+name_url_up)
          var desc_up=$('#'+name_desc_up)
          var delete_img=$('#'+name_delete)
          var delete_img_up=$('#'+name_delete_up)
          var up=$('#'+name_up)
          var up_up=$('#'+name_up_up)
          var down=$('#'+name_down)
          var down_up=$('#'+name_down_up)
          //row id changed
          row.attr('id',name_row_up)
          row_up.attr('id',name_row)
          //url id changed
          url.attr('id',name_url_up)
          url.attr('name',name_url_up)
          url_up.attr('id',name_url)
          url_up.attr('name',name_url)
          //desc id changed
          desc.attr('id',name_desc_up)
          desc.attr('name',name_desc_up)
          desc_up.attr('id',name_desc)
          desc_up.attr('name',name_desc)
          //delete image id changed
          delete_img.attr('id',name_delete_up)
          delete_img_up.attr('id',name_delete)
          //up image id changed
          up.attr('id',name_up_up)
          up_up.attr('id',name_up)
          //down image id changed
          down.attr('id',name_down_up)
          down_up.attr('id',name_down)
          alert(row.attr('id'))
        }

      })
       $('.item-down').click(function(){
         
        var itemGroup=""
        var itemId=0
        var myTable=""
        alert('down')
         if ($(this).attr('id').indexOf('engage') > -1) {
          myTable="table1"
          itemGroup = 'engage'
          itemId = parseInt($(this).attr('id').replace('engage_','').replace('_down',''))
        } else if ($(this).attr('id').indexOf('explain') > -1) {
          myTable="table2"
          itemGroup = 'explain'
          itemId = parseInt($(this).attr('id').replace('explain_','').replace('_down',''))
        } else if ($(this).attr('id').indexOf('evaluate') > -1) {
          myTable="table3"
          itemGroup = 'evaluate'
          itemId = parseInt($(this).attr('id').replace('evaluate_','').replace('_down',''))
        }
        alert('check '+itemId) 
        down=itemId+1
        url_down = itemGroup+'url_'+(down).toString()
          while($( down>=$('#'+myTable +'>tbody >tr').length) && "#"+url_down).val()=="none" ){
            down=down+1
            url_down = itemGroup+'url_'+(down).toString()
          }
        if(itemId< $('#'+myTable +'>tbody >tr').length && down<=$('#'+myTable +'>tbody >tr').length){
          alert($('#'+myTable +'>tbody >tr').length)
          var name_row=itemGroup+'_'+itemId.toString()+'_row'
          var name_row_down=itemGroup+'_'+(down).toString()+'_row'
          $('#'+name_row).before($('#'+name_row_down))
          var name_url = itemGroup+'url_'+itemId.toString()
          var name_desc = itemGroup+'desc_'+itemId.toString()
          var name_url_down = itemGroup+'url_'+(down).toString()
          var name_desc_down = itemGroup+'desc_'+(down).toString()
          var name_delete= name_row.replace('_row','')
          var name_delete_down = name_row_down.replace('_row','')
          var name_up=name_row.replace('row','up')
          var name_up_down=name_row_down.replace('row','up')
          alert(name_up_down)
          var name_down=name_row.replace('row','down')
          var name_down_down=name_row_down.replace('row','down')
          var row=$('#'+name_row)
          var row_down =$('#'+name_row_down)
          var url=$('#'+name_url)
          var desc=$('#'+name_desc)
          var url_down=$('#'+name_url_down)
          var desc_down=$('#'+name_desc_down)
          var delete_img=$('#'+name_delete)
          var delete_img_down=$('#'+name_delete_down)
          var up=$('#'+name_up)
          var up_down=$('#'+name_up_down)
          var down=$('#'+name_down)
          var down_down=$('#'+name_down_down)
          //row id changed
          row.attr('id',name_row_down)
          row_down.attr('id',name_row)
          //url id changed
          url.attr('id',name_url_down)
          url.attr('name',name_url_down)
          url_down.attr('id',name_url)
          url_down.attr('name',name_url)
          //desc id changed
          desc.attr('id',name_desc_down)
          desc.attr('name',name_desc_down)
          desc_down.attr('id',name_desc)
          desc_down.attr('name',name_desc)
          //delete image id changed
          delete_img.attr('id',name_delete_down)
          delete_img_down.attr('id',name_delete)
          //up image id changed
          up.attr('id',name_up_down)
          up_down.attr('id',name_up)
          //down image id changed
          down.attr('id',name_down_down)
          down_down.attr('id',name_down)
          alert(up.attr('id'))
        }

      })

