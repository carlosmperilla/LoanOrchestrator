from drf_yasg import openapi

search_param = openapi.Parameter('search', openapi.IN_QUERY, description="Un término de búsqueda", type=openapi.TYPE_STRING)
page_param = openapi.Parameter('page', openapi.IN_QUERY, description="Un número de página dentro del conjunto de resultados paginado.", type=openapi.TYPE_INTEGER)

applicant_ordering_param = openapi.Parameter('ordering', openapi.IN_QUERY, 
                                        description="Qué campo utilizar al ordenar los resultados",
                                        type=openapi.TYPE_STRING, 
                                        enum=[
                                                'dni',
                                                '-dni',
                                                'last_name',
                                                '-last_name',
                                                'first_name',
                                                '-first_name',
                                                'email',
                                                '-email',
                                                'gender',
                                                '-gender',
                                                'slug',
                                                '-slug',
                                                ])

applicant_dni_param = openapi.Parameter('dni', openapi.IN_QUERY, description="DNI", type=openapi.TYPE_STRING)
applicant_first_name_param = openapi.Parameter('first_name', openapi.IN_QUERY, description="Nombre", type=openapi.TYPE_STRING)
applicant_last_name_param = openapi.Parameter('last_name', openapi.IN_QUERY, description="Apellido", type=openapi.TYPE_STRING)
applicant_email_param = openapi.Parameter('email', openapi.IN_QUERY, description="e-mail", type=openapi.TYPE_STRING)
applicant_gender_param = openapi.Parameter('gender', openapi.IN_QUERY, description="Género", type=openapi.TYPE_STRING)

loanrequest_ordering_param = openapi.Parameter('ordering', openapi.IN_QUERY, 
                                        description="Qué campo utilizar al ordenar los resultados",
                                        type=openapi.TYPE_STRING, 
                                        enum=[
                                                'amount',
                                                '-amount',
                                                'approved',
                                                '-approved',
                                                'slug',
                                                '-slug'
                                                ])

loanrequest_approved_param = openapi.Parameter('approved', openapi.IN_QUERY, description="Estado Aprobado o no", type=openapi.TYPE_BOOLEAN)
loanrequest_amount_param = openapi.Parameter('amount', openapi.IN_QUERY, description="Monto", type=openapi.TYPE_NUMBER)
loanrequest_minamount_param = openapi.Parameter('min_amount', openapi.IN_QUERY, description="Mínimo monto", type=openapi.TYPE_NUMBER)
loanrequest_maxamount_param = openapi.Parameter('max_amount', openapi.IN_QUERY, description="Máxima monto", type=openapi.TYPE_NUMBER)

applicant_get_params = [
                    applicant_dni_param,
                    applicant_first_name_param,
                    applicant_last_name_param,
                    applicant_email_param,
                    applicant_gender_param,
                    search_param,
                    page_param,
                        ]

loanrequest_get_params = [
                    loanrequest_ordering_param,
                    loanrequest_approved_param,
                    loanrequest_amount_param,
                    loanrequest_minamount_param,
                    loanrequest_maxamount_param,
                    search_param,
                    page_param,
                        ]