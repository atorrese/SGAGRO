
$(function () {
    $('.Province').attr('style','width: 94%;');
    $('.Ciudad').attr('style','width: 94%;');
    $('.Country').attr('style','width: 94%;');

    $('.Province').select2({
        placeholder:'Seleccione Provincia',
        allowClear:true,
        language:langujeSearch,
        ajax:SearchAjax('/location/province/')
    });
    $('.Country').select2({
        placeholder:'Seleccione Pais',
        allowClear:true,
        language:langujeSearch,
        ajax:SearchAjax('/location/country/')
    });
    $('.Ciudad').select2({
        placeholder:'Seleccione Ciudad',
        allowClear:true,
        language:langujeSearch,
        ajax:SearchAjax('/location/canton/')
    });
    $('.cls-Ciudad').select2({
        placeholder:'Seleccione Ciudad',
        allowClear:true,
        language:langujeSearch,
        ajax:SearchAjax('/location/canton/')
    });
    $('.prueba').click(function (e) {
        event = $(this)

        console.log(JSONevent.data('json'));
        console.log(event.data('json').html);
        console.log(event.data('json').route);
        //$('#form-sellers').append();
        //$('#modal-sellers').modal('show');
        console.log('hizo click en prueba');

    });

    $('#Names,#SurNames,#Ciudad,#Phone,#Email,#Address,#References,#DeapertureDate, #DateAdmission').change(function () {
        $(this).removeClass('is-invalid');
    });

    // Evento de busqueda de  Cliente
        // Evento de busqueda de  vendedor
    $('#SupervisorId').select2({
        placeholder:'Seleccione supervisor',
        allowClear:true,
        language:langujeSearch,
        ajax:SearchAjax('/sale/supervisor/')

    });



    // Evento de busqueda de  vendedor
    $('#SellerId').select2({
        placeholder:'Seleccione Vendedor',
        allowClear:true,
        language:langujeSearch,
        ajax:SearchAjax('/sale/seller/')

    });


    // Evento de busqueda de  Cliente
    $('#ClientId').select2({
        placeholder:'Seleccione Cliente',
        allowClear:true,
        language:langujeSearch,
        ajax:SearchAjax('/sale/client/')

    });
    $('#select-product').select2({
        placeholder:'Seleccione Producto',
        allowClear:true,
        language:langujeSearch,});
    //$('.btn-danger').on('click',function () {
    //console.log('Presiono el boton');
    //});

    //seleccionar producto
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

    //boton agregar producto
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
                    footer: '<a href>Why do I have this issue?</a>'
                })
            }
        }
    );
    $('table.table-bordered').change(function () {
        ActualizarTabla();
    });
    $('.Price').change(function () {
        ActualizarTabla();
    });

});
