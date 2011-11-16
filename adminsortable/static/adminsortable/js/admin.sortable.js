jQuery(function($){
    $('.sortable').sortable({
        axis : 'y',
        containment : 'parent',
        tolerance : 'pointer',
        items : 'li',
        stop : function(event, ui)
        {
            var indexes = Array();
            ui.item.parent().children('li').each(function(i)
            {
                indexes.push($(this).find(':hidden[name="pk"]').val());
            });
            $.ajax({
                url: ui.item.find('a.admin_sorting_url').attr('href'),
                type: 'POST',
                data: { indexes: indexes.join(',') }
            });
        }
    });
});
