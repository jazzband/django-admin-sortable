(function($){

    $(function() {
        jQuery('.sortable').sortable({
            axis : 'y',
            containment : 'parent',
            tolerance : 'pointer',
            items : 'li',
            stop : function(event, ui) {
                var indexes = [],
                    lineItems = ui.item.parent().find('> li');

                lineItems.each(function(i) {
                    indexes.push($(this).find(':hidden[name="pk"]').val());
                });

                $.ajax({
                    url: ui.item.find('a.admin_sorting_url').attr('href'),
                    type: 'POST',
                    data: { indexes: indexes.join(',') },
                    success: function() {
                        // set icons based on position
                        lineItems.each(function(index, element) {
                            var icon = $(element).find('a.admin_sorting_url .fa');
                            icon.removeClass('fa-sort-desc fa-sort-asc fa-sort');

                            if (index === 0) {
                                icon.addClass('fa fa-sort-desc');
                            }
                            else if (index == lineItems.length - 1) {
                                icon.addClass('fa fa-sort-asc');
                            }
                            else  {
                                icon.addClass('fa fa-sort');
                            }
                        });

                        ui.item.effect('highlight', {}, 1000);
                    }
                });
            }
        }).click(function(e){
            e.preventDefault();
        });
    });

})(django.jQuery);
