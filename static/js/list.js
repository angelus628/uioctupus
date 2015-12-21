$(document).ready(function(){

$('#scripts').on('click', '.ejecutar', function(){
    script = $(this).attr('id');
    $(this).text('Ejecutando');
    $('.ejecutar').attr('disabled','disabled');
    $.get('/ejecutar?script='+script, function(data){
         $('.ejecutar').text('Ejecutar');
         $('.ejecutar').removeAttr('disabled');
    });
});

});
