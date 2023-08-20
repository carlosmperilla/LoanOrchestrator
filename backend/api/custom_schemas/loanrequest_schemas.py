from drf_yasg.utils import swagger_auto_schema
from .oa_query_parameters import loanrequest_get_params

loanrequest_list_schema = swagger_auto_schema(
    operation_summary="Obtiene las Peticiones de Prestamos paginadas",
    operation_description='### Ejemplo:\n'+
                          '`GET /loanrequests/`',
    tags=['Petición de Prestamo - Visualización'],
    manual_parameters=loanrequest_get_params
)

loanrequest_retrieve_schema = swagger_auto_schema(
    operation_summary="Obtiene una Petición de Prestamo por su slug",
    operation_description='### Ejemplo:\n'+
                          '`GET /loanrequests/25/`',
    tags=['Petición de Prestamo - Visualización']
)

loanrequest_create_schema = swagger_auto_schema(
    operation_summary="Crea una Petición de Prestamo",
    operation_description='### Ejemplo:\n'+
                          '`POST /loanrequests/`',
    tags=['Petición de Prestamo - Creación']
)

loanrequest_update_schema = swagger_auto_schema(
    operation_summary="Actualiza una Petición de Prestamo por su slug",
    operation_description='### Ejemplo:\n'+
                          '`PUT /loanrequests/25/`',
    tags=['Petición de Prestamo - Actualización']
)

loanrequest_partial_update_schema = swagger_auto_schema(
    operation_summary="Actualiza una Petición de Prestamo parcialmente por su slug",
    operation_description='### Ejemplo:\n'+
                          '`PATCH /loanrequests/25/`',
    tags=['Petición de Prestamo - Actualización']
)

loanrequest_destroy_schema = swagger_auto_schema(
    operation_summary="Elimina una Petición de Prestamo por su slug",
    operation_description='### Ejemplo:\n'+
                          '`DELETE /loanrequests/25/`',
    tags=['Petición de Prestamo - Eliminación']
)