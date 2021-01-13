const btnEliminar = document.querySelectorAll('.btn-eliminar');
const ruta = document.getElementsByName('.href-eliminar');
url =""
btnEliminar.forEach(btn => {
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        Swal.fire({
            title: '¿Está usted seguro?',
            text: "¡Va a eliminar este registro!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            confirmButtonText: '¡Sí, eliminal!',
            cancelButtonText: '¡No, cancelar!',
            reverseButtons: true,
            showLoaderOnConfirm: true,
            preConfirm: () => {
                return (
                    axios.delete(`${this.href}`, {
                        headers: {
                            'X-CSRFToken': Cookies.get('csrftoken')
                        },
                    }).then(response => {
                        return response.data
                    }).catch(error => {
                        //console.log(error.response);
                        Swal.showValidationMessage(
                            `Surgió un error: ${error.response.statusText} ${error.response.status}`
                        )
                    })
                );
            },
            allowOutsideClick: () => !Swal.isLoading()
        }).then(result => {
            console.log(result);
            console.log(result.value);
            console.log(result.value.status);

            if (result.value) {
                if(result.value.status) {
                    Swal.fire({
                        title: '¡Eliminado!',
                        text: result.value.message,
                        icon: 'success',
                        preConfirm: () => {
                            //console.log(ruta);
                            return result.value;
                        }
                    }).then((result) => {

                    
                        ({href: window.location} = window.location);
                    })
                }else{
                    Swal.fire({
                        icon: 'info',
                        title: '¡Registro no se Elimino!',
                        text: result.value.message,
                        footer: ''
                    })
                }
            }
        }).catch(error=>{
            console.log(error);
        });
    })
});
