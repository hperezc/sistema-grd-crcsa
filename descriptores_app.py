from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from models import db, Evaluacion, Admin
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dashboard import init_dashboard
import pdfkit
import io
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://hperezc97:geoHCP97@mysql-hperezc97.alwaysdata.net/hperezc97_nivelesmadurez')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

class ProcesosGestionForm(FlaskForm):
    empresa = StringField('Nombre de la Empresa', validators=[DataRequired()])
    
    p1_identificacion_amenazas = RadioField(
        'P1. Identificación de amenazas',
        choices=[
            ('0', 'No se conocen las amenazas en la organización'),
            ('1', 'Las amenazas están identificadas sin metodología definida (inspeccion visual, experiencia, informalmente)'),
            ('2', 'Las amenazas se encuentran identificadas a traves de metodologia definida y adoptada en la organización'),
            ('3', 'Las amenazas se identifican a traves un analisis detallado, con una metodologia cuantitativa y se actualizan según los cambios en el tiempo de esta.'),
            ('4', 'La metodologia definida y adoptada por la organización, se aplica a otras a areas de la organización con las modificaciones respectivas.')
        ],
        validators=[DataRequired()]
    )
    
    p2_identificacion_vulnerabilidades = RadioField(
        'P2. Identificación de vulnerabilidades',
        choices=[
            ('0', 'No se conoce las vulnerabilidades de la organización.'),
            ('1', 'Las vulnerabildiades estan identificadas de manera experiencial sin una metodologia definida.'),
            ('2', 'Las vulnerabilidades se encuentran identificadas a través de una metodologia definida y adoptada en la organización.'),
            ('3', 'Las vulnerabilidades se identifican mediante una metodologia especifica para la organización y esta se encuentra adoptada a nivel organizacional de manera formal.'),
            ('4', 'La metodologia definida y adoptada se aplica a otras a areas de la organización con las modificaciones respectivas.')
        ],
        validators=[DataRequired()]
    )

    p3_analisis_riesgos = RadioField(
        'P3. Análisis de riesgos',
        choices=[
            ('0', 'No existe un analisis de los riesgos en la organización.'),
            ('1', 'Los riesgos de analizan de manera informal sin una metodologia definida.'),
            ('2', 'Se realiza el analisis de los riesgos traves de una metodologia definida.'),
            ('3', 'Los riesgos se analizan a traves de una metodologia especifica para la organización y adoptada formalmente.'),
            ('4', 'Los riesgos se analizan a traves de una metodologia,  esta se aplica a otras a areas de la organización, con las modificaciones respectivas.')
        ],
        validators=[DataRequired()]
    )

    p4_valoracion_riesgos = RadioField(
        'P4. Valoración de riesgos',
        choices=[
            ('0', 'No se lleva a cabo una valoracion de los riesgos en la organización.'),
            ('1', 'Los riesgos se valoran de manera informal sin metodologia definida/estructurada.'),
            ('2', 'Se realiza la valoracion a traves de una metodologia definida y adoptada pro la organización.'),
            ('3', 'Se realiza la valoracion de los riesgo a traves de una metodologia especifica, adaptada y reconocida internacionalmente..'),
            ('4', 'La metodologia se aplica a otras a areas de la organización con sus modificaciones especificas adaptadas.')
        ],
        validators=[DataRequired()]
    )

    p5_reduccion_riesgos = RadioField(
        'P5. Reducción de riesgos',
        choices=[
            ('0', 'No existen proyectos, planes, obras o actividades en ejecucion y/o proyectados, para reducir los riesgos valorados'),
            ('1', 'Existe al menos un proyecto, obra o actividad informal en ejecucion con el objetivo de reducir un riesgo identificado'),
            ('2', 'Existe mas de un proyecto, obra o actividad propiamente estructurados, en ejecucion con cronograma, presupuesto e indicadores definidos'),
            ('3', 'Cada riesgo identificado cuenta con proyecto, obra o actividad, estructurada, con cronograma, prespuesto proyectado, indicadores y al menos uno en ejecucion '),
            ('4', 'Otras areas de la organización llevan a cabo proyectos de reduccion del riesgo bajo metodologia definida.')
        ],
        validators=[DataRequired()]
    )

    p6_monitoreo_revision = RadioField(
        'P6. Monitoreo y revisión',
        choices=[
            ('0', 'No se lleva a cabo monitoreo y revision de las amenazas existentes y las vulnerabilidades.'),
            ('1', 'El monitoreo y revision se realiza de manera informal sin formatos, registros o equipos definidos.'),
            ('2', 'Se realiza el monitoreo y revision de ameanazas con formatos, registros y equipos definidos.'),
            ('3', 'EL monitoreo y revision se realiza de manera periodica, se analizan los resultados y retroalimentacion para cada amenaza identificada.'),
            ('4', 'Otras areas de la organización realizan el monitoreo y revision periodicos para sus amenazas con instrumentos definidos, con sus respectivas.')
        ],
        validators=[DataRequired()]
    )

    p7_seguimiento_estrategias = RadioField(
        'P7. Seguimiento estrategias de reducción',
        choices=[
            ('0', 'No se realiza seguimiento a los Proyectos, Obras o Actividades(POAs) ejecutadas'),
            ('1', 'Se realiza seguimiento de manera informal a los POAS sin indicadores'),
            ('2', 'Ser realiza el seguimiento con indicadores de desempeño (KPI)'),
            ('3', 'Se lleva a cabo el seguimiento a traves de los indicadores y se ajustan los Proyectos, obras o actividades en funcion'),
            ('4', 'Otras areas de la organización llevan a cabo el seguimiento, con sus propios indicadores y metodologias especificos.')
        ],
        validators=[DataRequired()]
    )

    p8_comunicacion = RadioField(
        'P8. Comunicación y retroalimentación',
        choices=[
            ('0', 'No se comunican de manera interna las amenazas, vulnerabilidades o riesgos de la organización'),
            ('1', 'Solo las figuras clave de la organización conocen las amenazas, vulnerabilidades y riesgos'),
            ('2', 'Se realiza la divulgacion de las amenazas, vulnerabilidades y riesgos al interior de la organización'),
            ('3', 'Todos los integrantes de la organización conocen los riesgos, son participes en la construccion de POAS y retroalimentan su ejecucion.'),
            ('4', 'Otras areas de la organización comunican sus riesgos al interior esta. La organización divulga al publico sus riesgos y brinda espacios de retroalimentacion.')
        ],
        validators=[DataRequired()]
    )
    
    submit = SubmitField('Siguiente')

class RegulacionesResilienciaForm(FlaskForm):
    empresa = StringField('Nombre de la Empresa', validators=[DataRequired()])
    
    pt1_adopcion_certificaciones = RadioField(
        'PT1. Adopción de certificaciones internacionales',
        choices=[
            ('0', 'No se adoptan certificaciones, estandares o buenas practicas de carácter internacional (ISO 31000, 31010, OSHAS, PIARC, SPANCOLD, ICOLD)'),
            ('1', 'Existen POAs proyectados a nivel organizaciónal para la adopcion de certificaciones, estandares o buenas practicas de carácter internacional.'),
            ('2', 'Se estan ejecutando POAs con miras a adoptar certificaciones, estandares o buenas practicas de carácter internacional'),
            ('3', 'Se cuenta con al menos una certificacion, estandar o buena practica de carácter internacional a nivel organizacional.'),
            ('4', 'Se cuenta con varias certificaciones, estandares o buenas practicas de carácter internacional en varias areas de la organización.')
        ],
        validators=[DataRequired()]
    )
    
    pt2_regulaciones_nacionales = RadioField(
        'PT2. Regulaciones nacionales',
        choices=[
            ('0', 'No se conocen  las regulaciones nacionales en materia de gestion del riesgo, ni cuales aplican para la organización'),
            ('1', 'Se conocen alungas regulaciones nacionales en gestion del riesgo y se realiza su aplicación a la organización.'),
            ('2', 'Se conocen las regulaciones nacionales en gestión del riesgo y cuales aplican para la organización. Existe una matriz regulatoria peor no se realiza un seguimiento juicioso.'),
            ('3', 'Existe una matriz regulatoria, se aplican las regulaciones respectivas. Se realiza el seguimiento y actualizacion de esta.'),
            ('4', 'La matriz soporta las deciones organizacionales en materia de gestion del riesgo. Se monitorea constantemente los cambio regulatorios  nacionales y se planean las modificaciones de los instrumentos, planes, programas y tecnologias respectivas.')
        ],
        validators=[DataRequired()]
    )
    
    pt3_plan_gestion_riesgo = RadioField(
        'PT3. Plan de Gestión del Riesgo',
        choices=[
            ('0', 'No existe un Plan de Gestion del Riesgo en la organización'),
            ('1', 'Existen Proyecyos, Obras o Actividades proyectados para la elaboracion de un PGRD'),
            ('2', 'Se esta construyendo un Plan de gestion del riesgo en la organización'),
            ('3', 'La organizacion  cuenta con un Plan de Gestion del Riesgo y este se actualiza de manera periodica (anual)'),
            ('4', 'Se cuenta con un Plan de Gestion del Riesgo, incluye todas las areas de la organizcacion y se actualiza minimo cada año')
        ],
        validators=[DataRequired()]
    )
    
    pt4_politica_gestion_riesgo = RadioField(
        'PT4. Política de Gestión del Riesgo',
        choices=[
            ('0', 'No se cuenta con una politica de Gestion del Riesgo'),
            ('1', 'Se conoce la orientacion de la organización a la Gestion del riesgo, pero no hay politica adoptada'),
            ('2', 'Se cuenta con una politica de gestion del riesgo definida y adoptada a nivel organizacional'),
            ('3', 'La politica se aplica a externos y contratistas mediante formacion al ingreso, o como requisitos de contratacion.'),
            ('4', 'La politica se actualiza en funcion de los estandares y/o tendencias nacionales e internacionales')
        ],
        validators=[DataRequired()]
    )
    
    pt5_politica_seguridad = RadioField(
        'PT5. Política de seguridad operacional/SST',
        choices=[
            ('0', 'No se cuenta con una Politica de seguridad operaciónal /sst ni se conoce su orientacion'),
            ('1', 'Se conoce la orientacion de la organización a la seguridad operacional pero no hay politica'),
            ('2', 'Se cuenta con una politica definida'),
            ('3', 'La politica se aplica a externos y contratistas'),
            ('4', 'La politica se actualiza en funcion de los estandares y/o tendencias internacionales')
        ],
        validators=[DataRequired()]
    )
    
    pt6_sistema_sarlaft = RadioField(
        'PT6. Sistema de Administración de Riesgo de Lavado de Activos y Financiacion del Terrorismo (SARLAFT)',
        choices=[
            ('0', 'La organización no cuenta con un instrumento o mecanismo orientado a la prevencion de riesgos SARLAFT'),
            ('1', 'Se conoce la orientacion de la organización a la mitigacion del riesgo de lavado de activos/sarlaft pero no hay politica o instrumento'),
            ('2', 'Se cuenta con una politica definida SARLAFT definida y adoptada que permite'),
            ('3', 'Se cuenta con una politica SARLAFT y/o sistema que la administra y la politica se aplica a externos y contratistas'),
            ('4', 'La politica SARLAFT y el sistema que la administra se actualiza en funcion de los estandares y/o tendencias nacionales e internacionales')
        ],
        validators=[DataRequired()]
    )

    pt7_memoria_emergencias = RadioField(
        'PT7. Memoria de emergencias y aprendizajes de eventos.',
        choices=[
            ('0', 'No se lleva a cabo un registro de los accidentes, eventos y/o contingencias presentados.'),
            ('1', 'Los eventos son registrados con datos generales (fecha, ubicación y tipo de evento)'),
            ('2', 'Los eventos son registrados con datos puntuales y detallados (Ubicación,  impactos especificos, personas involucrada, efectos economicos y operacionales)'),
            ('3', 'Si se presenta un evento de emergencia o contingencia, se realiza una investigacion del evento presentado con registros especificos e informes diseñados para tal fin. El resultado de estos informes se utiliza para la toma de decisiones.'),
            ('4', 'Los eventos se registran bajo una metodologia especifica, se emiten informes, recomendaciones, se actualizan los instrumentos, proyectos, obras o actividades en gestion del riesgo en consecuencia.')
        ],
        validators=[DataRequired()]
    )

    pt8_planes_emergencia = RadioField(
        'PT8. Planes de emergencia y contigencia (PEC)',
        choices=[
            ('0', 'No existen planes de emergencia y contingencia.'),
            ('1', 'Se realiza la respuesta a eventos de emergencia de manera informal, con personal y conocimientos basicos, no hay un instrumento que guie el accionar o personas ni su formacion para su atencion especifica.'),
            ('2', 'Se cuenta con un plan de emergencia y contingencia con protocolos generales para la respuesta a emergencias, pero no hay un financiamiento especifico o personal especializado para ejecutarlo. No se realiza formacion del personal en tematicas relacionadas'),
            ('3', 'Existe un PEC, con protocolos generales y especificos de respuesta para cada escenario de riesgo identificado, al igual que financiamiento para su operatividad y personas con conocimeintos especificos para su ejecución'),
            ('4', 'Otras areas de la organización cuentan con planes para situaciones de emergencia y/o eventos adversos, según su area de desempeño y necesidades especificas.')
        ],
        validators=[DataRequired()]
    )

    pt9_seguros_polizas = RadioField(
        'PT9. Seguros y polizas',
        choices=[
            ('0', 'La organización no cuenta con seguros o polizas en nigun area.'),
            ('1', 'Solo existe un monto destinado para emergencias y contingencias; pero sin poliza o seguro.'),
            ('2', 'Se cuenta con al menos una poliza y/o seguro que cubre al menos alguno de los riesgos identificados en la organización.'),
            ('3', 'Se cuenta con seguros o polizas y estos cubren todos los riesgos identificados a nivel organizacional. La poliza/seguro cubre al personal que labora y sus bienes personales.'),
            ('4', 'Las polizas o seguros existentes ademas de cubrir los riesgos de la organización, toma en cuenta el cese de operaciones de la empresa y las cadenas de suministro de esta, es exigida para proveedores en la ejecucion de sus labores.')
        ],
        validators=[DataRequired()]
    )
    
    
    submit = SubmitField('Siguiente')

class EquipamientoMaterialesForm(FlaskForm):
    empresa = StringField('Nombre de la Empresa', validators=[DataRequired()])
    
    eq1_control_acceso = RadioField(
        'EQ1. Control de acceso',
        choices=[
            ('0', 'No existe controles de acceso a los lugares o recursos de la organización'),
            ('1', 'Existen solo controles fisicos de acceso (Vallas, Rejas, Bolardos, Letreros, capas fisicas de seguridad).'),
            ('2', 'Existen controles de acceso fisicos y administrativos (Procedimientos de registro de usuarios, rotaciones de personal, credenciales acceso)'),
            ('3', 'Existen controles de acceso fisico, administrativos y tecnicos (Credenciales digitales, identificadores, contraseñas, tokens, CCTV, control de conexiones IP/ISD, auditoria de accesos'),
            ('4', 'Otras areas de la organización cuentan con controles de acceso especificamente diseñados para su area operativa. Se realizan auditorias de acceso periodicas.')
        ],
        validators=[DataRequired()]
    )
    
    eq2_controles_seguridad = RadioField(
        'EQ2. Controles de seguridad operacional',
        choices=[
            ('0', 'Las operaciones se realizan solo con la experiencia del personal. Sin procedimientos operativos especificos, ni controles estructurales'),
            ('1', 'Solo existen procedimientos para actividades criticas en la organización, pero son informales, no estandarizados y sin controles estructurales'),
            ('2', 'Se llevan a cabo procedimientos especificos puntuales para diferentes areas de la organización, estan estandarizados, adoptados y algunos de estos cuentan con controles estructurales'),
            ('3', 'Un porcentaje mayor al 80 de las actividades  cuentan con procedimientos operativos estandarizados de ejecucion en su gran mayoria con controles estructurales. Se realizan auditorias de implementación.'),
            ('4', 'Existe una politica de seguridad operaciónal, se actualiza, se llevan a cabo auditorias con controles determinados para los procesos y estos se actualizan en consecuencia.')
        ],
        validators=[DataRequired()]
    )
    
    eq3_controles_ciberseguridad = RadioField(
        'EQ3. Controles de ciberseguridad',
        choices=[
            ('0', 'No existen controles de ciberseguridad'),
            ('1', 'Se realiza la identificacion y gestion de activos en la organización (inventarios de dispositivos y plaformas de softwares)'),
            ('2', 'Se implementa restricciones de acceso a los recursos digitales y sus plataformas fisicas'),
            ('3', 'Se realiza el monitoreo de acceso, de flujos de datos, actualizaciones constantes, control de endpoints, redundancia de proveedores, backcups, segmentacion de la red'),
            ('4', 'Existe una politica de ciberseguridad y personal con dedicacion 100% a la tarea, ademas de auditorias de software y proveedores.')
        ],
        validators=[DataRequired()]
    )
    
    eq4_redes_deteccion = RadioField(
        'EQ4. Redes internas o externas de deteccion Alerta / Alarma / comunicación / monitoreo',
        choices=[
            ('0', 'No existen redes internas o externas de alerta, alarma o monitoreo y estas, no toman en cuenta la diversidad de la poblacion para ser inclusivas'),
            ('1', 'Se identifican las instalaciones, procesos o actividades que requieren la implementacion de al menos una red de Alerta/Alarma/comunicación o monitoreo. No se toma en cuenta la diversidad del personal para generar inclusión.'),
            ('2', 'Se cuentan con al menos una red o sistema de Alerta /Alarma /comunicación/monitoreo en las areas y/o procesos criticos, y esta cuenta con mecanismos alternativos para generar inclusividad teniendo en cuenta la diversidad.'),
            ('3', 'Las redes de Alerta /Alarma /comunicación/monitoreo cubren todas las ubicaciones operativas de la empresa. Ademas existen mecanismos alternativos para las areas donde laboran personal con necesidades diferenciadas. Se toman en cuenta la comunidad de el area de influencia de la empresa.'),
            ('4', 'Las redes cubren toda la organización y ubicaciones geograficas adicional, las areas criticas cuentan con redes especializadas y especificas, para alertar al personal con necesidades diferenciadas. El personal con necesidades diferenciadas toma parte en el proceso de diseño de estos sistemas, al igual que la comunidad circundante a la organizacion.')
        ],
        validators=[DataRequired()]
    )
    
    eq5_brigadas_respuesta = RadioField(
        'EQ5. Brigadas para respuesta a eventos de emergencia, roles y responsabilidades',
        choices=[
            ('0', 'No existe una brigada para la respuesta a emergencias'),
            ('1', 'Existen personas con conocimientos basicos en atencion de eventos de emergencias, pero no estan agrupados ni estructurados'),
            ('2', 'Se cuenta con brigada de emergencias al interior de la organización, con estructura definida, responsabilidades y recursos operativos, y esta esta compuesta por al menos 20% de mujeres'),
            ('3', 'La brigadase encuentra estructurada y con roles especifico realiza formacion constante para actualizar, adquirir y refrescar capacidades de atencion de emergencias. Se encuentra compuesta por al menos 40% de mujeres'),
            ('4', 'Cada ubicación operativa cuenta con una brigada de emegencias, programa de formacion continua, equipamiento disponible y compuesta al menos de un 50% de mujeres.')
        ],
        validators=[DataRequired()]
    )
    
    eq6_formacion_capacitacion = RadioField(
        'EQ6. Formacion, capacitacion y practicas en gestion del riesgo',
        choices=[
            ('0', 'No se identifican los conocimientos actuales del personal, las necesidades de formacion y no exiten planes de formacion y/o capacitacion del personal de la organización en gestion del riesgo'),
            ('1', 'Se conoce que algunos integrantes del personal cuentan con conocimientos y experiencia en gestion del riesgo, pero no existen planes de formacion, capacitacion o practicas en gestion del riesgo'),
            ('2', 'Se identifican los conocimientos y brechas actuales del personal en gestion del riesgo y, con base en esto, se formulan planes de formacion y/o capacitacion.'),
            ('3', 'La formacion y capacitacion en Gestion del Riesgo hace parte de los requisitos ingreso a la organización y se llevan a cabo al menos una vez al año. Las simulaciones y simulacros son constanes con base en los escenarios de riesgo y la formacion impartida'),
            ('4', 'Existe personal interno o externo que periodicamente forma o capacita el personal, se realizan ejercios de aplicación. Las simulaciones y simulacros se evaluan y retroalimentan.')
        ],
        validators=[DataRequired()]
    )
    
    submit = SubmitField('Siguiente')

class IntegracionTransversalidadForm(FlaskForm):
    empresa = StringField('Nombre de la Empresa', validators=[DataRequired()])
    
    it1_transversalizacion = RadioField(
        'IT1. Transversalización de la gestión del riesgo',
        choices=[
            ('0', 'Otras áreas de la empresa no cuentan con procesos en gestión del riesgo'),
            ('1', 'Solo las áreas críticas de la organización realizan algún proceso de la gestión del riesgo de manera informal, sin una metodología definida'),
            ('2', 'Se lleva a cabo alguno de los procesos de la gestión del riesgo en otras áreas de la empresa, con una metodología establecida'),
            ('3', 'Otras áreas de la organización implementan procedimientos y metodologías específicas para los procesos de gestión del riesgo'),
            ('4', 'Todas las áreas de la organización llevan a cabo la gestión del riesgo con procedimientos y metodologías adaptadas')
        ],
        validators=[DataRequired()]
    )
    
    it2_protocolos_comunicacion = RadioField(
        'IT2. Protocolos de comunicación y divulgación del riesgo',
        choices=[
            ('0', 'No existen protocolos de comunicación en la organización para la gestión del riesgo, ni estos cuentan con un componentes de inclusividad y diversidad en su elaboración'),
            ('1', 'Solo se realiza momentos de comunicación y divulgación, con enfoque de seguridad y gestión del riesgo una vez suceden eventos de emergencia. No se toma en cuenta la diversidad e inclusión para divulgar estos momentos.'),
            ('2', 'Existen medios y canales definidos para la comunicación de emergencia-gestión del riesgo, interna y externa de la organización y estos son utilizados para transmitir mensajes de seguridad o gestión del riesgo. Se toma en cuenta algunas poblaciones con necesidades especiales.'),
            ('3', 'Existen protocolos de comunicación de emergencia o gestión del riesgo a nivel interno y externo. Existe un área dedicada a su elaboración, redacción, emisión interna y externa con enfoque inclusivo. Gran parte de los receptores de esta comunicación son tenidos en cuenta para la elaboración de los contenidos y su difusión'),
            ('4', 'El área dedicada cuenta con protocolos de comunicaciones para eventos de emergencia en cada situación presentados, se encuentra formada en la terminología específica y se articula con las entidades además de comunidad. Se utilizan estrategias específicas inclusivas donde se toma en cuenta la diversidad de la población objetivo')
        ],
        validators=[DataRequired()]
    )
    
    it3_planes_ayuda = RadioField(
        'IT3. Planes de ayuda mutua',
        choices=[
            ('0', 'La organización no hace parte ni cuenta con ningún plan de ayuda mutua'),
            ('1', 'Se han presentado eventos donde se ha brindado apoyo a otras organizaciones o personas, sin un plan específico'),
            ('2', 'Se han realizado acercamientos formales para la construcción de un plan de ayuda mutua o se encuentra en construcción'),
            ('3', 'Existe mínimo un plan de ayuda mutua y existen mecanismos de articulación que permiten el la operatividad del mismo'),
            ('4', 'Existe un plan de ayuda mutua mediante convenio interinstitucional, se a aplicado, se actualiza y se divulga al personal')
        ],
        validators=[DataRequired()]
    )
    
    it5_retroalimentacion = RadioField(
        'IT5. Retroalimentación de la gestión del riesgo',
        choices=[
            ('0', 'No se llevan a cabo encuestas de percepción u opinión en la organización'),
            ('1', 'La retroalimentación se realiza de manera verbal e informal, sin registros claros o toma de acciones'),
            ('2', 'Se lleva a cabo la retroalimentación a través de encuestas sencillas relacionadas con la gestión del riesgo y/o sus procesos'),
            ('3', 'Existe una práctica extendida de retroalimentación a nivel organizacional, sistema de PQRS, lecciones aprendidas en proyectos, obras o actividades'),
            ('4', 'Todas las áreas llevan a cabo retroalimentación de sus actividades organizacionales y estas, son tomadas en cuenta para la mejora de los procesos')
        ],
        validators=[DataRequired()]
    )
    
    it6_mecanismos_articulacion = RadioField(
        'IT6. Mecanismos de articulación interinstitucional',
        choices=[
            ('0', 'No se realiza articulación con otras instituciones u organizaciones en materia de gestión del riesgo y emergencias'),
            ('1', 'Se ha llevado a cabo acercamiento con instituciones y/o organizaciones pero no existe nada formal'),
            ('2', 'Existe al menos un mecanismo establecido para la articulación con instituciones y/o organismos de respuesta'),
            ('3', 'Existen más de un mecanismo de articulación con otras entidades y organizaciones. Formalmente definido que es utilizado periódicamente'),
            ('4', 'Los mecanismos de articulación institucional se definen para cada actividad, proyecto u obra en gestión del riesgo y emergencias')
        ],
        validators=[DataRequired()]
    )
    
    submit = SubmitField('Siguiente')

class OrganizacionForm(FlaskForm):
    empresa = StringField('Nombre de la Empresa', validators=[DataRequired()])
    
    or1_area_gestion = RadioField(
        'OR1. Área de gestión del riesgo',
        choices=[
            ('0', 'No existe un área de gestión del riesgo'),
            ('1', 'Existe una persona encargada de la gestión del riesgo pero no hay un cargo formal'),
            ('2', 'Existe cargo de gestión del riesgo y una persona contratada'),
            ('3', 'Existe un área de gestión del riesgo, y más de una persona en el área'),
            ('4', 'Existe un área de gestión del riesgo, estructura de funcionamiento y personal disponible 24/7')
        ],
        validators=[DataRequired()]
    )
    
    or2_presupuesto = RadioField(
        'OR2. Presupuesto para gestión del riesgo',
        choices=[
            ('0', 'No se asigna presupuesto para la gestión del riesgo'),
            ('1', 'Se asigna presupuesto esporádico no correspondiente a un plan de inversión o proyecto específico'),
            ('2', 'Se destina presupuesto para gestión del riesgo con base en necesidades, diagnósticos, proyectos, obras o actividades específicas'),
            ('3', 'El presupuesto se reserva anualmente según los proyectos obras o actividades proyectados'),
            ('4', 'El presupuesto para gestión del riesgo contempla intervenciones en diferentes áreas de la organización y se reserva anualmente')
        ],
        validators=[DataRequired()]
    )
    
    or3_personal_dedicacion = RadioField(
        'OR3. Personal con dedicación 100% a la gestión del riesgo',
        choices=[
            ('0', 'No existe personal para gestión del riesgo'),
            ('1', 'Existe una persona encargada pero su dedicación no es completa'),
            ('2', 'Existe una persona con dedicación completa para la gestión del riesgo'),
            ('3', 'Existe más de una persona con dedicación completa'),
            ('4', 'Cada área cuenta con alguien dedicado a la gestión del riesgo especfica')
        ],
        validators=[DataRequired()]
    )
    
    or4_proyectos_gestion = RadioField(
        'OR4. Se formulan y ejecutan proyectos en gestión del riesgo',
        choices=[
            ('0', 'No existen ni se plantean proyectos en gestión del riesgo'),
            ('1', 'Las intervenciones realizadas en gestión del riesgo no corresponden a proyectos, obras o actividades puntuales. Informales sin estructura'),
            ('2', 'Se formulan proyectos básicos en gestión del riesgo, con presupuesto destinado y horizonte de ejecución'),
            ('3', 'Los proyectos en gestión del riesgo son habituales en la organización y se encuentran varios en ejecución'),
            ('4', 'Cada área cuenta con proyectos en gestión del riesgo')
        ],
        validators=[DataRequired()]
    )
    
    or5_inclusion_gestion = RadioField(
        'OR5. Inclusión en la Gestión de Riesgo',
        choices=[
            ('0', 'No se cuenta con diversidad en el reclutamiento de personal ni en el talento humano, no hay equilibrio en el porcentaje de hombres y mujeres de la organización y, un bajo porcentaje de estas esta en puestos directivos'),
            ('1', 'No se cuenta con diversidad de reclutamiento de personal pero el porcentaje de mujeres es mayor al 30%, sin embargo el porcentaje de estas, en puestos directivos, es baja'),
            ('2', 'Se cuenta con diversidad en el reclutamiento y en el talento humano. El porcentaje de mujeres es cercano al 50% y el porcentaje de estas en puestos directivos es mas del 30%'),
            ('3', 'Se cuenta con diversidad en el reclutamiento y en el talento humano. El porcentaje de mujeres es del 50% y el porcentaje de estas en puestos directivos es del 30%'),
            ('4', 'Existe una política de diversidad e inclusión adoptada en la organización y se utiliza para dar soporte a las decisiones')
        ],
        validators=[DataRequired()]
    )
    
    submit = SubmitField('Siguiente')

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html', title='Sistema de Evaluación de Gestión del Riesgo')

@app.route('/procesos-gestion/<int:evaluacion_id>', methods=['GET', 'POST'])
def procesos_gestion(evaluacion_id):
    evaluacion = Evaluacion.query.get_or_404(evaluacion_id)
    form = ProcesosGestionForm(obj=evaluacion)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(evaluacion)
            evaluacion.ultima_dimension = 'procesos_gestion'
            
            # Verificar solo la sección actual
            if verificar_evaluacion_completa(evaluacion, 'procesos'):
                evaluacion.estado = 'en_proceso'
            else:
                evaluacion.estado = 'incompleto'
            
            db.session.commit()
            flash('Datos guardados correctamente', 'success')
            
            if 'guardar_salir' in request.form:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('regulaciones_resiliencia', evaluacion_id=evaluacion_id))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al guardar los datos: ' + str(e), 'danger')
    
    return render_template('procesos_gestion.html', form=form, evaluacion=evaluacion)

@app.route('/resultados/<int:evaluacion_id>')
def resultados(evaluacion_id):
    empresa_seleccionada = request.args.get('empresa')
    
    if empresa_seleccionada:
        return redirect(url_for('resultados', evaluacion_id=empresa_seleccionada))
    
    evaluacion = Evaluacion.query.get_or_404(evaluacion_id)
    
    empresas = Evaluacion.query.with_entities(
        Evaluacion.id, 
        Evaluacion.empresa
    ).distinct().all()
    
    return render_template('resultados.html', 
                         evaluacion=evaluacion, 
                         empresas=empresas)

@app.route('/exportar-pdf/<int:evaluacion_id>')
def exportar_pdf(evaluacion_id):
    evaluacion = Evaluacion.query.get_or_404(evaluacion_id)
    
    html = render_template('resultados_pdf.html', evaluacion=evaluacion)
    
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,
        'disable-external-links': None
    }
    
    try:
        pdf = pdfkit.from_string(html, False, options=options, configuration=config)
        
        return send_file(
            io.BytesIO(pdf),
            download_name=f'resultados_{evaluacion.empresa}.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f'Error al generar PDF: {str(e)}', 'error')
        return redirect(url_for('resultados', evaluacion_id=evaluacion_id))

@app.route('/regulaciones_resiliencia/<int:evaluacion_id>', methods=['GET', 'POST'])
def regulaciones_resiliencia(evaluacion_id):
    evaluacion = Evaluacion.query.get_or_404(evaluacion_id)
    form = RegulacionesResilienciaForm(obj=evaluacion)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(evaluacion)
            evaluacion.ultima_dimension = 'regulaciones_resiliencia'
            
            # Verificar estado después de cada paso
            if verificar_evaluacion_completa(evaluacion):
                evaluacion.estado = 'completo'
            else:
                evaluacion.estado = 'incompleto'
            
            db.session.commit()
            flash('Datos guardados correctamente', 'success')
            
            if 'guardar_salir' in request.form:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('equipamiento_materiales', evaluacion_id=evaluacion_id))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al guardar los datos: ' + str(e), 'danger')
    
    return render_template('regulaciones_resiliencia.html', form=form, evaluacion=evaluacion)

@app.route('/equipamiento_materiales/<int:evaluacion_id>', methods=['GET', 'POST'])
def equipamiento_materiales(evaluacion_id):
    evaluacion = Evaluacion.query.get_or_404(evaluacion_id)
    form = EquipamientoMaterialesForm(obj=evaluacion)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(evaluacion)
            evaluacion.ultima_dimension = 'equipamiento_materiales'
            
            # Verificar estado después de cada paso
            if verificar_evaluacion_completa(evaluacion):
                evaluacion.estado = 'completo'
            else:
                evaluacion.estado = 'incompleto'
            
            db.session.commit()
            flash('Datos guardados correctamente', 'success')
            
            if 'guardar_salir' in request.form:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('integracion_transversalidad', evaluacion_id=evaluacion_id))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al guardar los datos: ' + str(e), 'danger')
    
    return render_template('equipamiento_materiales.html', form=form, evaluacion=evaluacion)

@app.route('/integracion_transversalidad/<int:evaluacion_id>', methods=['GET', 'POST'])
def integracion_transversalidad(evaluacion_id):
    evaluacion = Evaluacion.query.get_or_404(evaluacion_id)
    form = IntegracionTransversalidadForm(obj=evaluacion)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(evaluacion)
            evaluacion.ultima_dimension = 'integracion_transversalidad'
            
            # Verificar estado después de cada paso
            if verificar_evaluacion_completa(evaluacion):
                evaluacion.estado = 'completo'
            else:
                evaluacion.estado = 'incompleto'
            
            db.session.commit()
            flash('Datos guardados correctamente', 'success')
            
            if 'guardar_salir' in request.form:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('organizacion', evaluacion_id=evaluacion_id))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al guardar los datos: ' + str(e), 'danger')
    
    return render_template('integracion_transversalidad.html', form=form, evaluacion=evaluacion)

@app.route('/organizacion/<int:evaluacion_id>', methods=['GET', 'POST'])
def organizacion(evaluacion_id):
    evaluacion = Evaluacion.query.get_or_404(evaluacion_id)
    form = OrganizacionForm(obj=evaluacion)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(evaluacion)
            evaluacion.ultima_dimension = 'organizacion'
            
            # Verificar si la evaluación está completa
            if verificar_evaluacion_completa(evaluacion):
                evaluacion.estado = 'completo'
                flash('Evaluación completada exitosamente', 'success')
            
            db.session.commit()
            
            if 'guardar_salir' in request.form:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('resultados', evaluacion_id=evaluacion_id))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al guardar los datos: ' + str(e), 'danger')
    
    return render_template('organizacion.html', form=form, evaluacion=evaluacion)

@app.route('/resultados')
def resultados_lista():
    evaluaciones = Evaluacion.query.order_by(Evaluacion.fecha.desc()).all()
    if not evaluaciones:
        flash('No hay evaluaciones registradas todavía. Por favor, realice una evaluación primero.', 'info')
        return redirect(url_for('index'))
    return render_template('resultados_lista.html', evaluaciones=evaluaciones)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        flash('Usuario o contraseña incorrectos', 'error')
    return render_template('admin/login.html', form=form)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    evaluaciones = Evaluacion.query.order_by(Evaluacion.fecha.desc()).all()
    return render_template('admin/dashboard.html', evaluaciones=evaluaciones)

@app.route('/admin/evaluacion/<int:id>/delete', methods=['POST'])
@login_required
def delete_evaluacion(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    db.session.delete(evaluacion)
    db.session.commit()
    flash('Evaluación eliminada exitosamente', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/iniciar-evaluacion', methods=['GET', 'POST'])
def iniciar_evaluacion():
    form = IniciarEvaluacionForm()
    if form.validate_on_submit():
        try:
            evaluacion = Evaluacion(
                empresa=form.empresa.data,
                estado='parcial',
                ultima_dimension='inicio'
            )
            db.session.add(evaluacion)
            db.session.commit()
            flash('Evaluación iniciada correctamente', 'success')
            return redirect(url_for('procesos_gestion', evaluacion_id=evaluacion.id))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la evaluación: ' + str(e), 'danger')
            return redirect(url_for('iniciar_evaluacion'))
    return render_template('iniciar_evaluacion.html', form=form)

class IniciarEvaluacionForm(FlaskForm):
    empresa = StringField('Nombre de la Empresa', validators=[DataRequired()])
    submit = SubmitField('Comenzar Evaluación')

@app.route('/continuar_evaluacion/<int:evaluacion_id>')
def continuar_evaluacion(evaluacion_id):
    evaluacion = Evaluacion.query.get_or_404(evaluacion_id)
    ultima_dimension = evaluacion.ultima_dimension
    
    if ultima_dimension == 'procesos_gestion':
        return redirect(url_for('regulaciones_resiliencia', evaluacion_id=evaluacion_id))
    elif ultima_dimension == 'regulaciones_resiliencia':
        return redirect(url_for('equipamiento_materiales', evaluacion_id=evaluacion_id))
    elif ultima_dimension == 'equipamiento_materiales':
        return redirect(url_for('integracion_transversalidad', evaluacion_id=evaluacion_id))
    elif ultima_dimension == 'integracion_transversalidad':
        return redirect(url_for('organizacion', evaluacion_id=evaluacion_id))
    else:
        return redirect(url_for('procesos_gestion', evaluacion_id=evaluacion_id))

@app.route('/editar_evaluacion/<int:evaluacion_id>', methods=['GET', 'POST'])
@login_required
def editar_evaluacion(evaluacion_id):
    evaluacion = Evaluacion.query.get_or_404(evaluacion_id)
    
    if evaluacion.ultima_dimension == 'procesos_gestion':
        return redirect(url_for('procesos_gestion', evaluacion_id=evaluacion_id))
    elif evaluacion.ultima_dimension == 'regulaciones_resiliencia':
        return redirect(url_for('regulaciones_resiliencia', evaluacion_id=evaluacion_id))
    elif evaluacion.ultima_dimension == 'equipamiento_materiales':
        return redirect(url_for('equipamiento_materiales', evaluacion_id=evaluacion_id))
    elif evaluacion.ultima_dimension == 'integracion_transversalidad':
        return redirect(url_for('integracion_transversalidad', evaluacion_id=evaluacion_id))
    elif evaluacion.ultima_dimension == 'organizacion':
        return redirect(url_for('organizacion', evaluacion_id=evaluacion_id))
    else:
        # Si no hay última dimensión, comenzar desde el principio
        return redirect(url_for('procesos_gestion', evaluacion_id=evaluacion_id))

@app.route('/dashboard-analitico')
def dashboard_analitico():
    return redirect('/dashboard')

# Inicializar el dashboard
init_dashboard(app)

def verificar_evaluacion_completa(evaluacion, seccion=None):
    campos_por_seccion = {
        'procesos': [
            evaluacion.p1_identificacion_amenazas,
            evaluacion.p2_identificacion_vulnerabilidades,
            evaluacion.p3_analisis_riesgos,
            evaluacion.p4_valoracion_riesgos,
            evaluacion.p5_reduccion_riesgos,
            evaluacion.p6_monitoreo_revision,
            evaluacion.p7_seguimiento_estrategias,
            evaluacion.p8_comunicacion
        ],
        'regulaciones': [
            evaluacion.pt1_adopcion_certificaciones,
            evaluacion.pt2_regulaciones_nacionales,
            evaluacion.pt3_plan_gestion_riesgo,
            evaluacion.pt4_politica_gestion_riesgo,
            evaluacion.pt5_politica_seguridad,
            evaluacion.pt6_sistema_sarlaft,
            evaluacion.pt7_memoria_emergencias,
            evaluacion.pt8_planes_emergencia,
            evaluacion.pt9_seguros_polizas
        ],
        'equipamiento': [
            evaluacion.eq1_control_acceso,
            evaluacion.eq2_controles_seguridad,
            evaluacion.eq3_controles_ciberseguridad,
            evaluacion.eq4_redes_deteccion,
            evaluacion.eq5_brigadas_respuesta,
            evaluacion.eq6_formacion_capacitacion
        ],
        'integracion': [
            evaluacion.it1_transversalizacion,
            evaluacion.it2_protocolos_comunicacion,
            evaluacion.it3_planes_ayuda,
            evaluacion.it5_retroalimentacion,
            evaluacion.it6_mecanismos_articulacion
        ],
        'organizacion': [
            evaluacion.or1_area_gestion,
            evaluacion.or2_presupuesto,
            evaluacion.or3_personal_dedicacion,
            evaluacion.or4_proyectos_gestion,
            evaluacion.or5_inclusion_gestion
        ]
    }
    
    if seccion:
        # Solo verificar los campos de la sección actual
        campos_a_verificar = campos_por_seccion.get(seccion, [])
        return all(campo is not None and campo != '' for campo in campos_a_verificar)
    else:
        # Verificar todos los campos cuando no se especifica sección
        return all(
            campo is not None and campo != '' 
            for campos in campos_por_seccion.values() 
            for campo in campos
        )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Crear usuario admin si no existe
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(username='admin')
            admin.set_password('grdcrcsa24')
            db.session.add(admin)
            db.session.commit()
            
    app.run(debug=True)
