function highlight_row(sender) {
    var submit = sender.find('.delete-submit');
    if (submit.length == 0)  submit = sender.find('.update-submit');
    var row = submit.parents('div.row');
    return function (data) {
        var response = $(data);
        var error = response.find('.error');
        var success = response.find('.success');
        var ok = error.length == 0 && success.length != 0;

        // Row was removed
        if (ok && response.find('#'+row.attr('id')).length == 0) {
            row.remove();
            return;
        }
        // updated
        var class_to_add = '';
        if (error.length != 0) {
            class_to_add = 'error';
        } else if (success.length != 0) {
            class_to_add = 'success';
        }
        row.addClass(class_to_add);
        window.setTimeout(
            function() {
                row.removeClass(class_to_add);
            },
            500
        );
    }
}

function wtf(a, b, c) {
    alert('Opertion failed: '+ a.message + ' ' + b.message + ' ' + c);
}

function set_operation(sender) {
    var submit_button = $(sender.target);
    var form = submit_button.parents('form.form-wp');
    var mask = '<input id="operation" type="hidden" value="<v>" name="<n>" />';
    var input = mask.replace('<v>', submit_button.attr('value'))
            .replace('<n>', submit_button.attr('name'));
    var operation = $(input);
    form.append(operation);
}

$(document).ready(
    function() {
        $('.form-wp').submit(
            function() {
                var data = $(this).serialize();
                if (data.indexOf("&print=") != -1) return;
                $.ajax({
                    url : $(this).attr('action'),
                    type : "POST",
                    data : data,
                    success : highlight_row($(this)),
                    error : wtf
                });
                $(this).find('input#operation').remove();
                return false;
            }
        );
        $(':submit').click(
            set_operation
        );
        $('.delete-submit').click(
            function() {
                return confirm($(this).attr("alt"));
            }
        );
    }
);
