(function($){

    $(function() {
        var sorting_urls = $(':hidden[name="admin_sorting_url"]');
        if (sorting_urls.length)
        {
            var sortable_inline_group = sorting_urls.closest('.inline-group');
            var tabular_inline_rows = sortable_inline_group.find('.tabular table tbody tr');

            tabular_inline_rows.addClass('sortable');

            sortable_inline_group.find('.tabular.inline-related').sortable({
                axis : 'y',
                containment : 'parent',
                create: function(event, ui) {
                    $('td.delete :checkbox').unbind();
                },
                tolerance : 'pointer',
                items : 'tr:not(.add-row)',
                stop : function(event, ui) {
                    if ($('.inline-deletelink').length > 0) {
                        $(ui.sender).sortable('cancel');
                        alert($('#localized_save_before_reorder_message').val());
                        return false;
                    }

                    var indexes = [];
                    ui.item.parent().children('tr').each(function(i)
                    {
                        var index_value = $(this).find('.original :input:first').val();
                        if (index_value !== '' && index_value !== undefined) {
                            indexes.push(index_value);
                        }
                    });

                    $.ajax({
                        url: ui.item.parent().find(':hidden[name="admin_sorting_url"]').val(),
                        type: 'POST',
                        data: { indexes : indexes.join(',') },
                        success: function() {
                            // set icons based on position
                            var icons = ui.item.parent().find('.fa');
                            icons.removeClass('fa-sort-desc fa-sort-asc fa-sort');
                            icons.each(function(index, element) {
                                var icon = $(element);
                                if (index === 0) {
                                    icon.addClass('fa fa-sort-desc');
                                }
                                else if (index == icons.length - 1) {
                                    icon.addClass('fa fa-sort-asc');
                                }
                                else  {
                                    icon.addClass('fa fa-sort');
                                }
                            });

                            // highlight sorted row, then re-stripe table
                            ui.item.effect('highlight', {}, 1000);
                            tabular_inline_rows.removeClass('row1 row2');
                            $('.tabular table tbody tr:odd').addClass('row2');
                            $('.tabular table tbody tr:even').addClass('row1');
                        }
                    });
                }
            });
        }
    });

})(django.jQuery);
