# ms-competencies

Microservicio RESTful para la gestión de competencias deportivas.

## Arquitectura
- Basado en Django + Django REST Framework
- Arquitectura por capas (ver diagrama C4)
- Versionado de API, HATEOAS, paginación, manejo de errores, respuestas estandarizadas y documentación Swagger

## Instalación y ejecución

1. Crear y activar entorno virtual:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
3. Migrar base de datos:
   ```powershell
   python manage.py migrate
   ```
4. Ejecutar servidor:
   ```powershell
   python manage.py runserver
   ```

## Pruebas
```powershell
python manage.py test
```

## Documentación Swagger
Disponible en `/api/v1/docs/` una vez iniciado el servidor.

## Ejemplo de respuesta RESTful estandarizada
```json
{
  "data": [...],
  "meta": {
    "pagination": {
      "count": 100,
      "next": "...",
      "previous": "..."
    }
  },
  "message": "Recursos obtenidos correctamente"
}
```

## Códigos HTTP usados
- 200: Éxito
- 201: Creado
- 204: Sin contenido
- 400: Datos inválidos
- 401: No autenticado
- 403: Sin permisos
- 404: No encontrado
- 409: Conflicto

## Endpoints personalizados
- `/categories/{code}/items/`
- `/items/{code}/activate/`

## Diagramas
- Ver carpeta `/docs` para los diagramas UML y C4.


## Prompt de desarrollo Copilot

```
Microservicio RESTful con Django + DRF + C4 + UML + HATEOAS + Swagger

Desarrolla un microservicio backend RESTful en Django (usar venv) usando Django REST Framework, siguiendo una arquitectura por capas, versionado de API y cumpliendo estándares REST como HATEOAS, paginación, códigos HTTP adecuados y documentación Swagger.

Objetivo general
A partir de las siguientes dos imágenes:
- El proyecto se llama ms-competencies y la app competence
- Un diagrama de clases UML que define las entidades del dominio.
- Un diagrama de componentes C4 (Nivel 3) que representa la arquitectura interna del microservicio Competencia.

Genera un microservicio backend usando Django y Django REST Framework, cumpliendo con los principios de diseño RESTful (nivel 3 de Richardson), incluyendo:
- Versionado de la API,
- HATEOAS (HyperlinkedModelSerializer),
- Documentación Swagger/OpenAPI,
- Respuestas estandarizadas,
- Manejo de errores con códigos HTTP (2xx, 4xx, 5xx),
- Paginación.

Instrucciones para procesar las imágenes
Imagen 1: Diagrama de clases UML
- Contiene únicamente las clases, atributos, métodos y relaciones.
- Ignora cualquier título, leyenda o comentario fuera de las clases.
- Interpreta:
  - Los atributos como campos Django.
  - Los métodos como funciones de instancia si se requieren.
  - Las relaciones UML como ForeignKey, ManyToManyField, etc.

Relación y nombre de roles
- Interpreta los nombres de rol en los extremos de las relaciones (por ejemplo: _user, _gameState, _phaseList) como nombres obligatorios para los campos en los modelos.
- Si la relación es reflexiva (una clase relacionada consigo misma), respeta los nombres:
  parent_catalog = models.ForeignKey('self', related_name='child_catalogs', on_delete=models.CASCADE)
- No modifiques ni omitas los nombres de rol: deben usarse exactamente como están en el diagrama.

Imagen 2: Diagrama de componentes C4 (Nivel 3)
- Sigue la arquitectura mostrada:
  -  URLs → Views → Services → Models → Database
  -  Serializers como canal entre Views y Models.
- El path base será /api/v1/competencies/ (versión incluida en la URL).

Estructura y funcionalidades del microservicio
1. Modelos (models.py)
- Basados en el diagrama UML.
- Implementa herencias, relaciones uno a muchos, reflexivas, etc.
- Atributo code como identificador lógico si aplica.
- Validaciones opcionales en clean().

2. Serializadores (serializers.py)
- Usar HyperlinkedModelSerializer para exponer URLs (HATEOAS).
- Validaciones (UniqueValidator, campos requeridos).
- Soporte para relaciones anidadas si aplica.
- Incluir docstrings.

3. Vistas (views.py)
- Usar ModelViewSet.
- lookup_field = 'code' si corresponde.
- Implementar filtros, búsqueda, ordenamiento y paginación (PageNumberPagination).
- Las respuestas deben seguir este formato estandarizado:

{
  "data": [...],
  "meta": {
    "pagination": {
      "count": 100,
      "next": "...",
      "previous": "..."
    }
  },
  "message": "Recursos obtenidos correctamente"
}

4. Servicios (services.py)
- Encapsular toda la lógica de negocio (jerarquía, validaciones, acciones como activar/desactivar).
- Usar excepciones personalizadas (ValidationError, ConflictError, etc.).
- Documentar cada función.

5. URLs (urls.py)
- usar DefaultRouter con versión: /api/v1/competencies/.
- Seguir convención REST:
  - Colecciones: /categories/, /items/
  - Documentos: /categories/{code}
  - Stores: /categories/{code}/items/
  - Controladores: /items/{code}/activate/


Pruebas (tests.py)
- Usar APITestCase.
- Verificar:
  Código	Verificación
  200	GET exitoso
  201	Recurso creado con POST
  204	Eliminación exitosa sin contenido
  400	Datos inválidos
  401	Autenticación faltante
  403	Permisos insuficientes
  404	Recurso no encontrado
  409	Conflicto de duplicidad u operación ilegal
- Verificar enlaces HATEOAS (url presente).
- Validar paginación y estructura estándar de respuesta.

Documentación (README.md)
Debe incluir:
- Propósito del microservicio Catalog.
- Arquitectura (imagen C4).
- Modelo de datos (imagen UML).
- Instalación, ejecución y pruebas.
- Uso de Swagger/OpenAPI.
- Ejemplo de una respuesta RESTful estandarizada.
- Códigos HTTP usados y ejemplos.
- Endpoints personalizados expuestos.

Extras
- .gitignore para Python y Django.
- Código limpio, legible, con docstrings en todos los métodos y clases (documentación clara y profesional).
- PEP8 aplicado.
- JSON con estructura clara (camelCase opcional si aplica).
- Documentación Swagger disponible en /api/v1/docs/.
```
