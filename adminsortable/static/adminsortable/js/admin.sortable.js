(function($){

    $(function() {
        jQuery('.sortable').sortable({
            axis : 'y',
            containment : 'parent',
            tolerance : 'pointer',
            items : 'li',
            stop : function(event, ui)
            {
                var indexes = [];
                ui.item.parent().children('li').each(function(i)
                {
                    indexes.push($(this).find(':hidden[name="pk"]').val());
                });
                $.ajax({
                    url: ui.item.find('a.admin_sorting_url').attr('href'),
                    type: 'POST',
                    data: { indexes: indexes.join(',') },
                    success: function()
                    {
                        ui.item.effect('highlight', {}, 1000);
                    }
                });
            }
        }).click(function(e){
            e.preventDefault();
        });
    });

})(django.jQuery);
