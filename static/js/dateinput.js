// I got it frde http://diariodecodigos.info/2010/01/dica-jquery-ui-dialog-e-datepicker/
// TODO format should be retrieved from Django config
// TODO localize in a better way
$.datepicker.setDefaults({dateFormat: 'dd/mm/yy', 
                          dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo'],
                          dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
                          dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
                          monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro', 'Outubro','Novembro','Dezembro'],
                          monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set', 'Out','Nov','Dez'],
                          nextText: 'Próximo',
                          prevText: 'Anterior'
                         });

$(document).ready(function() {
    $("input.date").datepicker(); 
    $("input.time").timePicker({step:15, separator:'h', show24Hours:true});
});
