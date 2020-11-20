$(function () {

   
    $('#MarkId').select2({
        placeholder:'Seleccione Marca',
        language:langujeSearch,
        ajax:SearchAjax('/catalog/mark/')
    });
    $('#CategoryId').select2({
        placeholder:'Seleccione Categoria',
        language:langujeSearch,
        ajax:SearchAjax('/catalog/category/')
    });
    $('span.selection').addClass('form-control');
    $('span.select2-selection.select2-selection--single').css( 'border', 'none');
});