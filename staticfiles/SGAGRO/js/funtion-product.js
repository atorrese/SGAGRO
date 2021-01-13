$(document).on('click','.btn-danger',function () {
    data=$(this).data('json');
    Swal.fire({
        title: 'Estas Seguro?',
        text: data.title,
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

});
$(function () {
    $('#btn-save').on('click',function (e) {
        e.preventDefault();
        var form = $(this).parents('form');
        data = $(this).data('json')
        Swal.fire({
            title: 'Estas Seguro?',
            text: data.title,
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

    });
});


    function AgregarProducto(pk){
        if ( pk != null ){
            $.ajax({
                url: `/catalog/product/show/${pk}`,
                method: 'GET',
                data:{
                    item_html:$('#html-item').val(),
                    tipo:$('#tipo').val()
                },
                dataType: 'json',
                async: false
            }).done(function(data){
                if(data.resp = 'ok'){
                    producto = data.item;
                    if((data.product.Stock != 0) || (data.tipo == 'orden')){
                         console.log(data);
                        $('#table-product').append(data.item);
                        $('#select-product').val('').trigger('change');
                        $('table.table-bordered').change();
                    }else{
                        Swal.fire(`El Producto que Seleccionaste Esta Agotado`);
                    }
                }
            }).fail(function(error){
                // console.log('error',error);
            });

        }
    }

    //verificar si producto esta en tabla
    function Verificador(pk){
        respuesta= false;
        id=0;
        $('table.table-bordered tbody tr').each(
            function () {
                id=$(this).find('a').attr('pk');

                if(pk == id){
                    respuesta =true
                }
            }
        );
        return respuesta;
    }

    function ActualizarTabla() {
        valorTotal = 0;
        valorDescuento = 0;
        detalle = [];
        $('table.table-bordered tbody tr ').each(function () {
            producto = $(this).find('a').attr('pk');
            precio = $(this).find('td.td-precio').find('div').find('input').val();
            cantidad = $(this).find('td.td-cantidad').find('input').val();
            total = cantidad * precio;
            valorTotal += total;
            $(this).find('td.td-total').text('$' + `${total.toFixed(2)}`);
            detalle.push({
                producto: producto,
                cantidad: cantidad,
                precio: precio,
                total: total.toFixed(2),
            });
        });
        $('.sub-total').text('$ ' + `${valorTotal.toFixed(2)}`);
        $('.total-pagar').text('$ ' + `${valorTotal.toFixed(2)}`);
        det = JSON.stringify(detalle);
        $('.details').val(det);
        totalPagar = valorTotal.toFixed(2);
        $('.TotalPay').val(totalPagar);
    }