# LoanOrchestrator

LoanOrchestrator es una aplicación de préstamos que utiliza tecnologías como Django, Docker, Celery, RabbitMQ, Redis y Nuxt 3. Los servicios están dockerizados y se incluyen instrucciones para el despliegue en local.

## Características

- Cache para consultas repetidas.
- Invalidación de caché asíncrona con Celery.
- Postgres como base de datos.
- Whitenoise para los archivos estáticos de la API Browseable.
- JWT para la autenticación.
- Test unitarios para los modelos y para las vistas (ViewSet).
- Honey-pot para reemplazar el admin por defecto y capturar ingresos indebidos.
- Documentación automática con Swagger y ReDoc.

## Despliegue en local

Para desplegar la aplicación en local, sigue estos pasos:

1. Ejecuta `docker compose up db -d` para iniciar el servicio de base de datos.
2. Ejecuta `docker compose up` para iniciar el resto de los servicios.
3. Ejecuta `docker compose exec backend python manage.py makemigrations` para crear las migraciones de la base de datos.
4. Ejecuta `docker compose exec backend python manage.py migrate` para aplicar las migraciones a la base de datos.
5. Ejecuta `docker compose exec backend python manage.py createsuperuser` para crear un superusuario.
6. Ejecuta `docker compose exec backend python manage.py test` para ejecutar los tests unitarios.

## Admin

La aplicación cuenta con un admin-trampa (honeypot) de prueba en `http://localhost:8000/admin` y un admin real en `http://localhost:8000/loan-secret-admin`.

## Documentación

La documentación automática de la API está organizada por tags y se puede acceder a través de Swagger en `http://localhost:8000/api/swagger` y ReDoc en `http://localhost:8000/api/redoc`.

## API

La API cuenta con filtros de ordenamiento y búsqueda. Desde el Browser API de DRF no se puede hacer POST directamente, porque sin credenciales no se puede acceder al GET. El POST sin credenciales se puede probar en el frontend en `http://localhost:3000`.

## Admin custom en frontend

El admin custom en frontend está incompleto debido a decisiones técnicas que implican validaciones de seguridad, consistencia de datos y reactividad. Sin embargo, permite ingresar un JWT válido para realizar peticiones. El JWT se puede obtener en `http://localhost:8000/api/authentication/login/` y el tiempo de vida del token es de 5 minutos.

El admin custom en frontend se encuentra en `http://localhost:3000/admin`. Aunque está incompleto, la presentación para que los usuarios no autenticados registren los pedidos y revisen si son aceptados o rechazados está funcional.

## Contribuciones

Si deseas contribuir al proyecto, puedes hacerlo mediante pull requests. Asegúrate de seguir las guías de estilo y documentación del proyecto. ¡Gracias por tu interés! 😊
