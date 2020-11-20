$(function() {
    $('.btn-new').click(function (e) {
        data = $(this).data('json');
        modal =  $(data.modal);
        modal.modal('show');
    });
    $('.btn-s').click(function(e){
        e.preventDefault();
        even= $(this);
        SaveObjeto(even)
    });
    SaveObjeto = (event)=>{
        form =event.parent().parent().serializeArray()
            .reduce((a,z)=>{
                a[z.name]=z.value;
                return a;
            },{});
        console.log(event.data('json'));
        $.post(event.data('json').route,form)
            .catch((error)=>{
                Swal.fire(error);
            })
            .then((data)=>{
                if(data.status){
                    //Swal.fire(data.message);
                    const Toast = Swal.mixin({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 3000,
                        timerProgressBar: true,
                        onOpen: (toast) => {
                            toast.addEventListener('mouseenter', Swal.stopTimer)
                            toast.addEventListener('mouseleave', Swal.resumeTimer)
                        }
                    });
                    Toast.fire({
                        icon: 'success',
                        title: 'Guardando Registro'
                    });
                    $(`${event.data('json').modal} .close`).click();
                }else{
                    error = JSON.parse(data.form_errors);
                    console.log(data);
                    $.each(error,(k,v)=>{
                        objeto = event.parent().parent().find('div').find('div').find('div').find(`[name=${k}]`);
                        console.log(objeto);
                        objeto.addClass('is-invalid');
                        texto='';
                        $.each(v,(i,o)=>{
                            texto +=`${o.message }<br>`
                        });
                        objeto.parent().find('div.invalid-feedback').html(texto);
                    })
                }
            })

    }
});