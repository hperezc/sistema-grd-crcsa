# Documentación de la API REST
# Sistema de Evaluación de Madurez en Gestión del Riesgo

## Índice
1. [Introducción](#introducción)
2. [Autenticación](#autenticación)
3. [Estructura de la API](#estructura-de-la-api)
4. [Endpoints](#endpoints)
5. [Respuestas y Formatos](#respuestas-y-formatos)
6. [Manejo de Errores](#manejo-de-errores)
7. [Límites y Consideraciones](#límites-y-consideraciones)
8. [Ejemplos de Integración](#ejemplos-de-integración)
9. [Soporte y Contacto](#soporte-y-contacto)

## Introducción

La API REST del Sistema de Evaluación de Madurez en Gestión del Riesgo permite acceder a los datos y funcionalidades del sistema de forma programática. Esta API está diseñada para facilitar la integración con otros sistemas, como Zoho CRM, permitiendo consultar evaluaciones, resultados y puntajes de manera segura y eficiente.

### Versión de la API

La versión actual de la API es `v1`. Todas las rutas comienzan con el prefijo `/api/v1/`.

### URL Base

https://sistema-grd-crcsa.onrender.com/api/v1

## Autenticación

La API utiliza autenticación basada en tokens JWT (JSON Web Token) para garantizar la seguridad de las comunicaciones. Todos los endpoints, excepto el de obtención de token, requieren un token de acceso válido.

### Obtener un token de acceso

Para interactuar con la API, primero debe obtener un token de acceso válido.

**Endpoint:**
```
POST /api/v1/token
```

**Headers:**
```
Authorization: Basic base64(username:password)
```

Donde `base64(username:password)` es la codificación en base64 de `username:password`.

**Ejemplo de solicitud con curl:**
```bash
curl -X POST https://sistema-grd-crcsa.onrender.com/api/v1/token \
  -u admin:grdcrcsa24
```

**Ejemplo de solicitud con PowerShell:**
```powershell
$credentials = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:grdcrcsa24"))
$headers = @{ Authorization = "Basic $credentials" }
Invoke-RestMethod -Uri "https://sistema-grd-crcsa.onrender.com/api/v1/token" -Method POST -Headers $headers
```

**Respuesta exitosa:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE3NDMzNTIwMDh9.rQFvDGzVGOjgjqXo2rn7gz6pblF23MsBf7vOrwWCJz4"
}
```

### Usar el token para solicitudes autenticadas

Una vez que tenga el token, debe incluirlo en el encabezado `Authorization` de todas las solicitudes posteriores.

**Headers para solicitudes autenticadas:**
```
Authorization: Bearer {token}
```

**Validez del token:**
El token tiene una validez de 24 horas desde su emisión. Después de este período, deberá solicitar un nuevo token.

## Estructura de la API

La API sigue los principios de diseño RESTful:

- Utiliza métodos HTTP estándar (GET, POST)
- Devuelve respuestas en formato JSON
- Utiliza códigos de estado HTTP para indicar el resultado de las operaciones
- Incluye URLs para vinculación de recursos relacionados

## Endpoints

### 1. Listar todas las evaluaciones

Devuelve un listado de todas las evaluaciones registradas en el sistema con información básica.

**Endpoint:**
```
GET /api/v1/evaluaciones
```

**Headers:**
```
Authorization: Bearer {token}
```

**Parámetros de consulta opcionales:**
- `estado`: Filtrar por estado ('completo', 'incompleto', 'en_proceso')
- `sector`: Filtrar por sector

**Ejemplo de solicitud con curl:**
```bash
curl -X GET https://sistema-grd-crcsa.onrender.com/api/v1/evaluaciones \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE3NDMzNTIwMDh9.rQFvDGzVGOjgjqXo2rn7gz6pblF23MsBf7vOrwWCJz4"
```

**Ejemplo de solicitud con PowerShell:**
```powershell
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE3NDMzNTIwMDh9.rQFvDGzVGOjgjqXo2rn7gz6pblF23MsBf7vOrwWCJz4"
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Uri "https://sistema-grd-crcsa.onrender.com/api/v1/evaluaciones" -Method GET -Headers $headers
```

**Ejemplo de respuesta:**
```json
[
  {
    "id": 328,
    "empresa": "Empresa ABC",
    "nit": "900123456",
    "email": "contacto@empresaabc.com",
    "sector": "Industrial",
    "fecha": "2023-05-15T14:30:22",
    "estado": "completo",
    "puntaje_total": 78.5
  },
  {
    "id": 329,
    "empresa": "Compañía XYZ",
    "nit": "800987654",
    "email": "info@companiaxyz.com",
    "sector": "Servicios",
    "fecha": "2023-05-16T10:15:43",
    "estado": "completo",
    "puntaje_total": 65.2
  }
]
```

### 2. Obtener detalles de una evaluación específica

Devuelve información completa sobre una evaluación específica, incluyendo todas las respuestas y puntajes.

**Endpoint:**
```
GET /api/v1/evaluaciones/{id}
```

**Headers:**
```
Authorization: Bearer {token}
```

**Ejemplo de solicitud con curl:**
```bash
curl -X GET https://sistema-grd-crcsa.onrender.com/api/v1/evaluaciones/328 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE3NDMzNTIwMDh9.rQFvDGzVGOjgjqXo2rn7gz6pblF23MsBf7vOrwWCJz4"
```

**Ejemplo de solicitud con PowerShell:**
```powershell
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE3NDMzNTIwMDh9.rQFvDGzVGOjgjqXo2rn7gz6pblF23MsBf7vOrwWCJz4"
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Uri "https://sistema-grd-crcsa.onrender.com/api/v1/evaluaciones/328" -Method GET -Headers $headers
```

**Ejemplo de respuesta:**
```json
{
  "id": 328,
  "empresa": "Empresa ABC",
  "nit": "900123456",
  "departamento": "Antioquia",
  "ciudad": "Medellín",
  "cantidad_empleados": 250,
  "responsable": "Juan Pérez",
  "rol": "Gerente de Riesgos",
  "telefono_fijo": "6042123456",
  "celular": "3001234567",
  "email": "contacto@empresaabc.com",
  "sector": "Industrial",
  "fecha": "2023-05-15T14:30:22",
  "estado": "completo",
  "ultima_dimension": "organizacion",
  
  "puntajes": {
    "puntaje_total": 78.5,
    "puntaje_procesos": 85.0,
    "puntaje_regulaciones": 72.5,
    "puntaje_equipamiento": 80.0,
    "puntaje_integracion": 75.0,
    "puntaje_organizacion": 80.0
  },
  
  "procesos": {
    "p1_identificacion_amenazas": "3",
    "p2_identificacion_vulnerabilidades": "4",
    "p3_analisis_riesgos": "3",
    "p4_valoracion_riesgos": "4",
    "p5_reduccion_riesgos": "3",
    "p6_monitoreo_revision": "4",
    "p7_seguimiento_estrategias": "3",
    "p8_comunicacion": "3"
  },
  
  "regulaciones": {
    "pt1_adopcion_certificaciones": "3",
    "pt2_regulaciones_nacionales": "2",
    "pt3_plan_gestion_riesgo": "3",
    "pt4_politica_gestion_riesgo": "4",
    "pt5_politica_seguridad": "3",
    "pt6_sistema_sarlaft": "2",
    "pt7_memoria_emergencias": "3",
    "pt8_planes_emergencia": "4",
    "pt9_seguros_polizas": "3"
  },
  
  "equipamiento": {
    "eq1_control_acceso": "4",
    "eq2_controles_seguridad": "3",
    "eq3_controles_ciberseguridad": "3",
    "eq4_redes_deteccion": "4",
    "eq5_brigadas_respuesta": "3",
    "eq6_formacion_capacitacion": "4"
  },
  
  "integracion": {
    "it1_transversalizacion": "3",
    "it2_protocolos_comunicacion": "4",
    "it3_planes_ayuda": "3",
    "it5_retroalimentacion": "3",
    "it6_mecanismos_articulacion": "4"
  },
  
  "organizacion": {
    "or1_area_gestion": "4",
    "or2_presupuesto": "3",
    "or3_personal_dedicacion": "4",
    "or4_proyectos_gestion": "4",
    "or5_inclusion_gestion": "3"
  },
  
  "url_resultados": "https://sistema-grd-crcsa.onrender.com/resultados/328"
}
```

### 3. Obtener solo resultados de una evaluación

Este endpoint devuelve únicamente los puntajes y resultados de una evaluación, sin incluir todas las respuestas detalladas.

**Endpoint:**
```
GET /api/v1/evaluaciones/{id}/resultados
```

**Headers:**
```
Authorization: Bearer {token}
```

**Ejemplo de solicitud con curl:**
```bash
curl -X GET https://sistema-grd-crcsa.onrender.com/api/v1/evaluaciones/328/resultados \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE3NDMzNTIwMDh9.rQFvDGzVGOjgjqXo2rn7gz6pblF23MsBf7vOrwWCJz4"
```

**Ejemplo de solicitud con PowerShell:**
```powershell
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE3NDMzNTIwMDh9.rQFvDGzVGOjgjqXo2rn7gz6pblF23MsBf7vOrwWCJz4"
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Uri "https://sistema-grd-crcsa.onrender.com/api/v1/evaluaciones/328/resultados" -Method GET -Headers $headers
```

**Ejemplo de respuesta:**
```json
{
  "id": 328,
  "empresa": "Empresa ABC",
  "puntajes": {
    "puntaje_total": 78.5,
    "puntaje_procesos": 85.0,
    "puntaje_regulaciones": 72.5,
    "puntaje_equipamiento": 80.0,
    "puntaje_integracion": 75.0,
    "puntaje_organizacion": 80.0
  },
  "fecha": "2023-05-15T14:30:22",
  "url_resultados": "https://sistema-grd-crcsa.onrender.com/resultados/328"
}
```

## Respuestas y Formatos

Todas las respuestas de la API se devuelven en formato JSON. Los campos numéricos utilizan punto como separador decimal.

### Formato de fechas

Las fechas se presentan en formato ISO 8601 (YYYY-MM-DDThh:mm:ss).

### Tipos de datos comunes

- `id`: Número entero
- `empresa`, `nit`, `email`: Cadenas de texto
- `fecha`: Cadena de texto en formato ISO 8601
- `puntaje_total` y otros puntajes: Números decimales
- `estado`: Cadena de texto ("completo", "incompleto", "en_proceso")

### Valores de respuesta en evaluaciones

Las respuestas a preguntas de evaluación se codifican como cadenas de texto del "0" al "4", donde:
- "0": Nivel mínimo o nulo
- "1": Nivel básico
- "2": Nivel intermedio
- "3": Nivel avanzado
- "4": Nivel sobresaliente

## Manejo de Errores

La API utiliza códigos de estado HTTP estándar para indicar el éxito o fracaso de una solicitud.

| Código | Descripción |
|--------|-------------|
| 200 | Éxito - La solicitud se completó correctamente |
| 400 | Solicitud incorrecta - El servidor no pudo entender la solicitud |
| 401 | No autorizado - Es necesaria autenticación |
| 403 | Prohibido - El servidor entiende la solicitud pero se niega a autorizarla |
| 404 | No encontrado - El recurso solicitado no existe |
| 500 | Error del servidor - Error interno del servidor |

### Ejemplos de respuestas de error

**Error de autenticación (401):**
```json
{
  "message": "Token faltante"
}
```

**Error de autenticación (401):**
```json
{
  "message": "Token inválido"
}
```

**Recurso no encontrado (404):**
```json
{
  "message": "La evaluación solicitada no existe"
}
```

**Error del servidor (500):**
```json
{
  "message": "Error al procesar la solicitud, inténtelo nuevamente"
}
```

## Límites y Consideraciones

### Límites de tasa

La API actualmente no impone límites estrictos de tasa, pero se recomienda no exceder las 300 solicitudes por minuto para garantizar un rendimiento óptimo. Esta restricción podría cambiar en el futuro para proteger la disponibilidad del servicio.

### Tamaño de la respuesta

Las respuestas que incluyen detalles completos de evaluaciones pueden ser extensas, especialmente para evaluaciones con muchas respuestas. Considere utilizar el endpoint de resultados resumidos (`/evaluaciones/{id}/resultados`) cuando no necesite todos los detalles.

### Caché

Para mejorar el rendimiento, se recomienda implementar caché en el lado del cliente para las respuestas que no cambian frecuentemente, como los detalles de evaluaciones completadas.

### Disponibilidad

El sistema está alojado en Render.com con una disponibilidad objetivo del 99.5%. Los mantenimientos programados serán anunciados con antelación siempre que sea posible.

## Ejemplos de Integración

### Integración con Zoho CRM

Para integrar esta API con Zoho CRM, puede seguir estos pasos generales:

1. **Obtener un token de acceso:**
   ```javascript
   // Ejemplo en JavaScript
   async function getToken() {
     const response = await fetch('https://sistema-grd-crcsa.onrender.com/api/v1/token', {
       method: 'POST',
       headers: {
         'Authorization': 'Basic ' + btoa('admin:grdcrcsa24')
       }
     });
     const data = await response.json();
     return data.token;
   }
   ```

2. **Obtener lista de evaluaciones:**
   ```javascript
   async function getEvaluaciones(token) {
     const response = await fetch('https://sistema-grd-crcsa.onrender.com/api/v1/evaluaciones', {
       method: 'GET',
       headers: {
         'Authorization': 'Bearer ' + token
       }
     });
     return await response.json();
   }
   ```

3. **Obtener detalles de una evaluación específica:**
   ```javascript
   async function getEvaluacionDetalle(token, id) {
     const response = await fetch(`https://sistema-grd-crcsa.onrender.com/api/v1/evaluaciones/${id}`, {
       method: 'GET',
       headers: {
         'Authorization': 'Bearer ' + token
       }
     });
     return await response.json();
   }
   ```

4. **Actualizar registros en Zoho CRM:**
   ```javascript
   async function actualizarZohoConResultados(evaluacionId) {
     // 1. Obtener token de API
     const token = await getToken();
     
     // 2. Obtener detalles de la evaluación
     const evaluacion = await getEvaluacionDetalle(token, evaluacionId);
     
     // 3. Preparar datos para Zoho
     const zohoData = {
       "data": [
         {
           "Company": evaluacion.empresa,
           "NIT": evaluacion.nit,
           "Email": evaluacion.email,
           "Score": evaluacion.puntajes.puntaje_total,
           "ProcessScore": evaluacion.puntajes.puntaje_procesos,
           "RegulationsScore": evaluacion.puntajes.puntaje_regulaciones,
           "EquipmentScore": evaluacion.puntajes.puntaje_equipamiento,
           "IntegrationScore": evaluacion.puntajes.puntaje_integracion,
           "OrganizationScore": evaluacion.puntajes.puntaje_organizacion,
           "ResultsURL": evaluacion.url_resultados
         }
       ]
     };
     
     // 4. Enviar a Zoho CRM (ejemplo)
     const zohoResponse = await fetch('https://www.zohoapis.com/crm/v2/Evaluaciones', {
       method: 'POST',
       headers: {
         'Authorization': 'Zoho-oauthtoken YOUR_ZOHO_TOKEN',
         'Content-Type': 'application/json'
       },
       body: JSON.stringify(zohoData)
     });
     
     return await zohoResponse.json();
   }
   ```

### Ejemplo con PowerShell (para automatizaciones)

```powershell
# Obtener token
$credentials = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:grdcrcsa24"))
$headers = @{ Authorization = "Basic $credentials" }
$tokenResponse = Invoke-RestMethod -Uri "https://sistema-grd-crcsa.onrender.com/api/v1/token" -Method POST -Headers $headers
$token = $tokenResponse.token

# Usar el token para obtener evaluaciones
$authHeaders = @{ Authorization = "Bearer $token" }
$evaluaciones = Invoke-RestMethod -Uri "https://sistema-grd-crcsa.onrender.com/api/v1/evaluaciones" -Method GET -Headers $authHeaders

# Procesar resultados y exportar a CSV
$resultados = @()
foreach ($evaluacion in $evaluaciones) {
    # Obtener detalles completos
    $detalle = Invoke-RestMethod -Uri "https://sistema-grd-crcsa.onrender.com/api/v1/evaluaciones/$($evaluacion.id)/resultados" -Method GET -Headers $authHeaders
    
    # Crear objeto para exportación
    $resultado = [PSCustomObject]@{
        ID = $evaluacion.id
        Empresa = $evaluacion.empresa
        NIT = $evaluacion.nit
        Sector = $evaluacion.sector
        Fecha = $evaluacion.fecha
        PuntajeTotal = $detalle.puntajes.puntaje_total
        PuntajeProcesos = $detalle.puntajes.puntaje_procesos
        PuntajeRegulaciones = $detalle.puntajes.puntaje_regulaciones
        PuntajeEquipamiento = $detalle.puntajes.puntaje_equipamiento
        PuntajeIntegracion = $detalle.puntajes.puntaje_integracion
        PuntajeOrganizacion = $detalle.puntajes.puntaje_organizacion
        URLResultados = $detalle.url_resultados
    }
    $resultados += $resultado
}

# Exportar a CSV
$resultados | Export-Csv -Path "Evaluaciones_$(Get-Date -Format 'yyyyMMdd').csv" -NoTypeInformation
```

## Soporte y Contacto

Para soporte técnico relacionado con la API o para reportar problemas, contáctenos a través de:

- **Email de Soporte:** hectorcperez21@gmail.com
- **Horario de Soporte:** Lunes a viernes, 7:00 AM - 5:00 PM (hora colombiana)

Al reportar problemas, incluya:
- Descripción detallada del problema
- Endpoint que está utilizando
- Ejemplos de solicitudes y respuestas recibidas
- Timestamp aproximado del problema

---

**Versión de la documentación:** 1.0  
**Última actualización:** Marzo de 2025
