# Acuerdo de Nivel de Servicio (SLA)
# Sistema de Evaluación de Madurez en Gestión del Riesgo

## 1. Definición del Servicio

### 1.1 Descripción del Sistema
Este SLA cubre el Sistema de Evaluación de Madurez en Gestión del Riesgo, una plataforma web desarrollada para la Cruz Roja Colombiana Seccional Antioquia, destinada a evaluar y analizar el nivel de madurez en gestión del riesgo empresarial.

### 1.2 Componentes Cubiertos
Este SLA aplica a:
- Aplicación web principal
- API REST para integraciones
- Base de datos y almacenamiento
- Infraestructura de alojamiento
- Servicios de autenticación y autorización

### 1.3 Usuarios y Stakeholders
- **Usuario Final**: Organizaciones que realizan evaluaciones de riesgo
- **Administradores**: Personal de Cruz Roja que gestiona evaluaciones
- **Integrador**: Proveedor de Zoho CRM que consume la API

## 2. Disponibilidad del Servicio

### 2.1 Porcentaje de Disponibilidad
El sistema garantiza una disponibilidad del 99.5% durante las horas operativas, lo que equivale a un tiempo de inactividad máximo de 3.65 horas mensuales.

### 2.2 Horario de Servicio
- **Horario Operativo**: 24 horas, 7 días a la semana
- **Soporte Técnico**: Lunes a viernes, 8:00 AM - 6:00 PM (hora colombiana)

### 2.3 Mantenimiento Planificado
- Notificación con mínimo 48 horas de anticipación
- Programado preferentemente en horarios de baja actividad
- No contabilizado dentro del tiempo de inactividad para el cálculo de disponibilidad

### 2.4 Exclusiones
- Interrupciones debidas a factores fuera de nuestro control (desastres naturales, ataques DDoS)
- Problemas originados en sistemas de terceros (proveedor de hosting, DNS)
- Indisponibilidad durante ventanas de mantenimiento programado

## 3. Soporte y Tiempos de Respuesta

### 3.1 Canales de Soporte
- Email: [hectorcperez21@gmail.com](mailto:hectorcperez21@gmail.com)
- Teléfono: [Tu número de contacto]
- Sistema de tickets: [Si existe]

### 3.2 Categorización de Incidentes

| Severidad | Descripción | Tiempo de Respuesta | Tiempo de Resolución |
|-----------|-------------|---------------------|----------------------|
| Crítico | Sistema completamente caído, datos en riesgo | 2 horas | 8 horas |
| Alto | Funcionalidad principal afectada, pero sistema operativo | 4 horas | 24 horas |
| Medio | Funcionalidad secundaria afectada, existen alternativas | 8 horas | 48 horas |
| Bajo | Consultas, mejoras, problemas menores | 24 horas | Según planificación |

*Nota: Los tiempos se consideran dentro del horario de soporte técnico.

### 3.3 Proceso de Soporte
1. Recepción y registro del incidente
2. Clasificación de severidad
3. Asignación de recursos
4. Investigación y diagnóstico
5. Resolución y verificación
6. Cierre y documentación

## 4. Rendimiento del Sistema

### 4.1 Tiempo de Respuesta
- Carga de página inicial: < 3 segundos
- Operaciones de navegación: < 2 segundos
- Respuestas de API: < 1 segundo

### 4.2 Capacidad
- Usuarios concurrentes soportados: 100
- Evaluaciones simultáneas: 50
- Peticiones API por minuto: 300

### 4.3 Indicadores Clave (KPIs)
- Disponibilidad mensual
- Tiempo medio de respuesta
- Tasa de errores
- Tiempo de resolución de incidentes

## 5. Gestión de Cambios

### 5.1 Notificación de Cambios
- Cambios mayores: Notificación con 7 días de anticipación
- Cambios menores: Notificación con 48 horas de anticipación
- Cambios de emergencia: Lo antes posible, mínimo 2 horas antes

### 5.2 Tipos de Cambios
- **Mayor**: Modificaciones estructurales, nuevas funcionalidades
- **Menor**: Corrección de errores, mejoras de rendimiento
- **Emergencia**: Parches críticos de seguridad

### 5.3 Proceso de Aprobación
- Presentación de cambios planificados
- Evaluación de impacto
- Aprobación por parte de stakeholders designados
- Implementación según cronograma acordado

## 6. Monitoreo y Reportes

### 6.1 Monitoreo Continuo
- Disponibilidad del sistema (uptime)
- Rendimiento y tiempos de respuesta
- Errores y excepciones
- Uso de recursos (CPU, memoria, almacenamiento)

### 6.2 Reportes Periódicos
- Informe mensual de disponibilidad
- Resumen de incidentes y resoluciones
- Métricas de rendimiento
- Recomendaciones de mejora

### 6.3 Acceso a Estado
- Estado actual del sistema visible a través de [dashboard/página de estado]
- Notificaciones automáticas ante incidentes críticos
- Histórico de incidentes y mantenimientos

## 7. Responsabilidades

### 7.1 Responsabilidades del Proveedor (Sistema de Evaluación)
- Mantener el sistema operativo según los niveles de servicio acordados
- Implementar y mantener medidas de seguridad
- Realizar copias de seguridad periódicas
- Proporcionar soporte técnico según lo establecido
- Notificar oportunamente sobre mantenimientos e incidentes

### 7.2 Responsabilidades del Cliente (Zoho/Cruz Roja)
- Reportar incidentes de manera oportuna y detallada
- Proporcionar información suficiente para la resolución de problemas
- Mantener seguras las credenciales de acceso
- Usar el sistema dentro de los límites de capacidad acordados
- Designar personal de contacto y autorizado para solicitudes de cambios

### 7.3 Límites de Responsabilidad
- No nos responsabilizamos por usos indebidos del sistema
- No garantizamos la precisión absoluta de los datos ingresados por usuarios
- No asumimos responsabilidad por indisponibilidad debida a factores externos

## 8. Procedimiento de Escalado

### 8.1 Niveles de Escalado

| Nivel | Contacto | Tiempo sin resolución |
|-------|----------|------------------------|
| 1 | Soporte Técnico: [Email/Teléfono] | Inicial |
| 2 | Coordinador Técnico: [Email/Teléfono] | Después de 50% del tiempo de resolución |
| 3 | Director de Proyecto: [Email/Teléfono] | Después de 75% del tiempo de resolución |

### 8.2 Proceso de Escalamiento
1. Documentar acciones tomadas hasta el momento
2. Notificar al siguiente nivel según la tabla anterior
3. Proporcionar toda la información relevante
4. Continuar seguimiento hasta resolución

## 9. Gestión del SLA

### 9.1 Revisión Periódica
Este SLA será revisado trimestralmente para asegurar que continúa satisfaciendo las necesidades de todas las partes.

### 9.2 Modificaciones
Cualquier modificación a este SLA debe ser acordada por escrito entre las partes.

### 9.3 Medición y Reportes
El cumplimiento de este SLA será medido y reportado mensualmente.

---

Documento versión: 1.0  
Fecha última actualización: [Fecha actual]  
Aprobado por: [Tu nombre], Analista de Geomática, Cruz Roja Colombiana Seccional Antioquia
