/*$(document).on('click','.btn-danger',function () {
    Swal.fire({
        title: 'Estas Seguro?',
        text: "Que quieres eliminar Este Item!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, Eliminar!'
    }).then((result) => {
        if (result.value) {
            $(this).parent().parent().remove();
            Swal.fire(
                'Eliminado!',
                'Se ah Eliminado con exito.',
                'success'
            )

        }
    })

});*/

$(function () {
    $('.ProviderId').select2({
        placeholder:'Seleccione Proveedor',
        allowClear:true,
        language:langujeSearch,
        ajax:SearchAjax('/purchase/provider/')
    });

    $('#select-product').select2({
        placeholder:'Seleccione Producto',
        allowClear:true,
        language:langujeSearch,
    });
    $('span.selection').addClass('form-control');
    $('span.select2-selection.select2-selection--single').css( 'border', 'none');
    $('#select-product').change(function () {
        producto= $(this).val();
        if(producto != ''){
            $('#add-product').trigger('click');
        }
    });
    $('#add-product').click(
        function () {
            producto= $('#select-product').val();
            //console.log(producto);
            if( producto != '' ){

                if(!Verificador(producto)){
                    AgregarProducto(producto);
                }else{
                    Swal.fire(`Este producto ya esta agregado`);
                    $('#select-product').val('').trigger('change');
                }
            }else{

                Swal.fire({
                    icon: 'error',
                    title: 'Error al Agregar un Producto',
                    text: 'Debe Seleccionar  un Producto!',
                    footer: ''
                })
            }
        });

    $('table.table-bordered').change(function () {
        ActualizarTabla();
    });
    $('.Price').change(function () {
        ActualizarTabla();
    });
    $('.quantity').change(function () {
        ActualizarTabla();
    });
/*
    $('#btn-save').on('click',function (e) {
        e.preventDefault();
        var form = $(this).parents('form');
        Swal.fire({
            title: 'Estas Seguro?',
            text: "Que quieres Guardar La Orden de Compra!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si, Guardar!'
        }).then((result) => {
            if (result.value) {
                ActualizarTabla();
                form.submit();
            }
        });

    });*/

});