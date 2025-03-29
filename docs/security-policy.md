# Políticas de Seguridad - Sistema de Evaluación de Madurez en Gestión del Riesgo

## 1. Introducción

### 1.1 Propósito
Este documento establece las políticas de seguridad para el Sistema de Evaluación de Madurez en Gestión del Riesgo desarrollado para la Cruz Roja Colombiana Seccional Antioquia. Define las medidas técnicas y organizativas implementadas para proteger la confidencialidad, integridad y disponibilidad de los datos y del sistema.

### 1.2 Alcance
Estas políticas aplican a todos los componentes del sistema, incluyendo la aplicación web, la API REST, la base de datos y la infraestructura de soporte.

### 1.3 Definiciones
- **Sistema**: Sistema de Evaluación de Madurez en Gestión del Riesgo
- **API**: Interfaz de Programación de Aplicaciones
- **JWT**: JSON Web Token
- **CSRF**: Cross-Site Request Forgery
- **XSS**: Cross-Site Scripting

## 2. Arquitectura de Seguridad

### 2.1 Infraestructura
- **Servidor de Aplicación**: Alojado en Render.com, plataforma cloud con certificaciones de seguridad
- **Base de Datos**: MySQL 8.0 alojada en AlwaysData
- **Certificados SSL/TLS**: Implementados en todas las comunicaciones

### 2.2 Protocolos de Comunicación
- Todas las comunicaciones utilizan HTTPS (TLS 1.2 o superior)
- API REST con autenticación JWT para todas las operaciones
- Cabeceras de seguridad HTTP implementadas:
  - Content-Security-Policy
  - X-Content-Type-Options
  - X-Frame-Options

### 2.3 Almacenamiento de Datos
- Base de datos con encriptación en tránsito
- Respaldos automáticos diarios
- Separación lógica de datos sensibles

## 3. Políticas de Autenticación y Acceso

### 3.1 Gestión de Credenciales
- Credenciales administrativas con requisitos de complejidad
- Rotación periódica de claves de acceso
- Gestión de usuarios con privilegios mínimos necesarios

### 3.2 Política de Contraseñas
- Longitud mínima: 10 caracteres
- Requisitos de complejidad: combinación de letras, números y caracteres especiales
- Almacenamiento: Hash con algoritmo seguro y salt único por usuario

### 3.3 Autenticación API
- Autenticación basada en tokens JWT
- Claves secretas generadas con alta entropía
- Tiempo de expiración: 24 horas para limitar ventana de ataque

### 3.4 Sesiones
- Timeout de sesión tras 30 minutos de inactividad
- Invalidación de sesión tras cambios de privilegios
- Protección CSRF en todos los formularios

## 4. Protección de Datos

### 4.1 Clasificación de Datos
- **Datos públicos**: Información general no sensible
- **Datos confidenciales**: Información organizacional y resultados de evaluaciones
- **Datos sensibles**: Credenciales de acceso y tokens de autenticación

### 4.2 Protección de Datos Sensibles
- Datos sensibles nunca expuestos en logs, URLs o interfaces
- Implementación de sanitización para todos los inputs de usuario
- Validación de datos en servidor y cliente

### 4.3 Políticas de Retención
- Los datos de evaluaciones se mantienen durante la vigencia del servicio
- Logs de actividad retenidos por 90 días
- Datos de prueba eliminados tras confirmar funcionamiento correcto

### 4.4 Backups y Recuperación
- Respaldos diarios automatizados
- Pruebas de recuperación realizadas mensualmente
- Tiempo de recuperación objetivo: 4 horas

## 5. Seguridad en el Desarrollo

### 5.1 Metodología Segura
- Revisión de código previo a integración
- Testing automatizado para vulnerabilidades comunes
- Principio de mínimo privilegio en todas las operaciones

### 5.2 Protección OWASP Top 10
Medidas implementadas contra:
- Inyección (SQL, NoSQL, comandos)
- Fallos de autenticación
- Exposición de datos sensibles
- XXE y deserialización insegura
- Fallas de configuración de seguridad

### 5.3 Prácticas de Codificación Segura
- Validación de todas las entradas de usuario
- Escapado de salidas en interfaz
- Gestión segura de dependencias y bibliotecas
- Control de acceso en cada capa de la aplicación

## 6. Monitoreo y Auditoría

### 6.1 Sistema de Logs
- Registro de eventos de autenticación (éxitos y fallos)
- Logs de acceso a API con detalles de petición
- Logs de errores y excepciones
- Registro de cambios administrativos

### 6.2 Monitoreo de Actividad
- Alertas automatizadas ante patrones sospechosos
- Monitoreo de disponibilidad 24/7
- Escaneo periódico de vulnerabilidades

### 6.3 Revisión Periódica
- Auditoría trimestral de logs y eventos de seguridad
- Revisión mensual de permisos y accesos
- Actualización periódica de esta política según cambios en el sistema

## 7. Gestión de Incidentes

### 7.1 Proceso de Respuesta
1. Detección y registro del incidente
2. Clasificación por severidad
3. Contención y mitigación
4. Análisis y resolución
5. Recuperación y restauración
6. Documentación y lecciones aprendidas

### 7.2 Clasificación de Severidad
- **Crítico**: Compromiso de datos sensibles, indisponibilidad total
- **Alto**: Afectación parcial al servicio, potencial exposición de datos
- **Medio**: Degradación de funcionalidades, sin exposición de datos
- **Bajo**: Problemas menores sin impacto en seguridad o disponibilidad

### 7.3 Notificación
- Procedimiento de notificación a partes afectadas
- Plazos de comunicación según severidad
- Canales seguros para reporte de vulnerabilidades

### 7.4 Análisis Post-Incidente
- Documentación del incidente y respuesta
- Identificación de causa raíz
- Implementación de mejoras para prevenir recurrencia

## 8. Cumplimiento

### 8.1 Normativas Relevantes
- Cumplimiento con la Ley 1581 de 2012 (Protección de Datos Personales en Colombia)
- Alineación con estándares de seguridad internacionales (NIST, ISO 27001)

### 8.2 Protección de Datos Personales
- Minimización de datos recolectados
- Información clara sobre uso y propósito de los datos
- Mecanismos para ejercer derechos de acceso, rectificación y supresión

## 9. Contacto

Para reportar problemas de seguridad, contactar a:
- Email: [hectorcperez21@gmail.com](mailto:hectorcperez21@gmail.com)
- Sistema de Gestión de Incidentes: [URL del sistema]

---

Documento versión: 1.0  
Fecha última actualización: [Fecha actual]  
Aprobado por: [Tu nombre], Analista de Geomática, Cruz Roja Colombiana Seccional Antioquia
