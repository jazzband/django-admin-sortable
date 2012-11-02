jQuery(function($){
    if ($(':hidden[name="admin_sorting_url"]').length > 0)
    {
        var sortable_inline_rows = $('.inline-group .inline-related');
        sortable_inline_rows.addClass('sortable');
        $('.inline-group').sortable({
            axis : 'y',
            containment : 'parent',
            tolerance : 'pointer',
            items : '.inline-related',
            stop : function(event, ui)
            {
                var indexes = Array();
                ui.item.parent().children('.inline-related').each(function(i)
                {
                    index_value = $(this).find(':hidden[name$="-id"]').val();
                    if (index_value != "" && index_value != undefined)
                        indexes.push(index_value);
                });
                    
                $.ajax({
                    url: ui.item.parent().find(':hidden[name="admin_sorting_url"]').val(),
                    type: 'POST',
                    data: { indexes : indexes.join(',') },
                    success: function()
                    {
                        ui.item.effect('highlight', {}, 1000);
                    }
                });
            }
        });
    }
});
