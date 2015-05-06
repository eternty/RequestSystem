

$(function() {

    var engies = $("#id_engineer").find('option');
    engies.each(function(elem){
        $(this).hide();
    });

    $("#id_group").on('change', function(e, o) {

        var opt = $(this).find('option:selected')[0];

        $.ajax({
            url: '/engineers_by_group/',
            type: 'GET',
            data: {
                group_id: opt.value
            },
            success: function(response) {
                var engies = $("#id_engineer").find('option');
                engies.each(function(elem){
                    if(this.value === "") {
                        $(this).prop('selected', true);
                    }
                    else {
                        $(this).prop('selected', false);
                    }

                    if ($.inArray(parseInt(this.value), response.ids) == -1) {
                        $(this).hide();
                    }
                    else {
                        $(this).show();
                    }
                })
            },
            error: function(response) {

            },
            fail: function(response) {

            }
        })
    });

});