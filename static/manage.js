function highlight_row(sender) {
    var row = sender.parents('div#row');
    return function (data) {
        var response = $(data);
        var error = response.find('.error');
        var success = response.find('.success');

        if (error.length != 0) {
            row.addClass('error');
        } else if (success.length != 0) {
            row.addClass('success');
        }
   
    }
}

function wtf(a, b, c) {
    alert('WTF?!');
    alert(a);
    alert(b);
    alert(c);
}

$(document).ready(
    function() {
        $('.form-wp').submit(
            function() {
                $.ajax({
                    url : $(this).attr('action'),
                    type : "POST",
                    data : $(this).serialize(),
                    success : highlight_row($(this)),
                    error : wtf
                });
                return false;
            }
        );
    }
);
