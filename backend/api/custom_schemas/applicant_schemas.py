from drf_yasg.utils import swagger_auto_schema
from .oa_query_parameters import applicant_get_params

applicant_list_schema = swagger_auto_schema(
    operation_summary="Obtiene los Solicitantes",
    operation_description='### Ejemplo:\n'+
                          '`GET /applicants/`',
    tags=['Solicitantes - Visualización'],
    manual_parameters=applicant_get_params
)

applicant_retrieve_schema = swagger_auto_schema(
    operation_summary="Obtiene un Solicitante por su slug",
    operation_description='### Ejemplo:\n'+
                          '`GET /applicants/c1396015-6d8b-4215-9096-9bd9136072d9/`',
    tags=['Solicitantes - Visualización'],
)

applicant_create_schema = swagger_auto_schema(
    operation_summary="Crea un Solicitante",
    operation_description='### Ejemplo:\n'+
                          '`POST /applicants/`',
    tags=['Solicitantes - Creación']
)

applicant_update_schema = swagger_auto_schema(
    operation_summary="Actualiza un Solicitante por su slug",
    operation_description='### Ejemplo:\n'+
                          '`PUT /applicants/c1396015-6d8b-4215-9096-9bd9136072d9/`',
    tags=['Solicitantes - Actualización']
)

applicant_partial_update_schema = swagger_auto_schema(
    operation_summary="Actualiza un Solicitante parcialmente por su slug",
    operation_description='### Ejemplo:\n'+
                          '`PATCH /applicants/c1396015-6d8b-4215-9096-9bd9136072d9/`',
    tags=['Solicitantes - Actualización']
)

applicant_destroy_schema = swagger_auto_schema(
    operation_summary="Elimina un Solicitante por su slug",
    operation_description='### Ejemplo:\n'+
                          '`DELETE /applicants/c1396015-6d8b-4215-9096-9bd9136072d9/`',
    tags=['Solicitantes - Eliminación']
)