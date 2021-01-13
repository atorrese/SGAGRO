

    var SearchAjax = (url)=>{
        ajax = {
            url:url,
            dataType:'json',
            type:'GET',
            data:function (params) {
                var queryParameters = {
                    search : params.term
                }
                return queryParameters;
            },
            processResults: function (data) {

                return{
                    results:$.map(data.data,function (item) {
                        return{
                            text: item.value,
                            id:item.id
                        }
                    })
                }
            }
        }
        return ajax;
    }
    var langujeSearch ={
            noResults:function () {
                return "No hay resultado";
            },
            searching: function () {
                return "Buscando..";
            },

            escapeMarkup:function (markup) {
                return markup;
            }
        }
