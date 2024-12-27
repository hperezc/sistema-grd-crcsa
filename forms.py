from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email

class EvaluacionForm(FlaskForm):
    empresa = StringField('Nombre de la Empresa', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    sector = SelectField('Sector', choices=[
        ('', 'Seleccione un sector'),
        ('industrial', 'Industrial'),
        ('comercial', 'Comercial'),
        ('servicios', 'Servicios'),
        ('salud', 'Salud'),
        ('educacion', 'Educación'),
        ('tecnologia', 'Tecnología'),
        ('otro', 'Otro')
    ], validators=[DataRequired()])
    submit = SubmitField('Comenzar Evaluación')

class ProcesosGestionForm(FlaskForm):
    empresa = StringField('Empresa', render_kw={'readonly': True})
    p1_identificacion_amenazas = RadioField('Identificación de Amenazas', choices=[(str(i), '') for i in range(5)])
    p2_identificacion_vulnerabilidades = RadioField('Identificación de Vulnerabilidades', choices=[(str(i), '') for i in range(5)])
    p3_analisis_riesgos = RadioField('Análisis de Riesgos', choices=[(str(i), '') for i in range(5)])
    p4_valoracion_riesgos = RadioField('Valoración de Riesgos', choices=[(str(i), '') for i in range(5)])
    p5_reduccion_riesgos = RadioField('Reducción de Riesgos', choices=[(str(i), '') for i in range(5)])
    p6_monitoreo_revision = RadioField('Monitoreo y Revisión', choices=[(str(i), '') for i in range(5)])
    p7_seguimiento_estrategias = RadioField('Seguimiento a Estrategias', choices=[(str(i), '') for i in range(5)])
    p8_comunicacion = RadioField('Comunicación', choices=[(str(i), '') for i in range(5)]) 

class IniciarEvaluacionForm(FlaskForm):
    # ... otros campos ...
    
    sector = SelectField('Sector Económico', choices=[
        ('', 'Seleccione un sector'),
        ('agricultura', 'Agricultura, ganadería, silvicultura y pesca'),
        ('mineria', 'Explotación de minas y canteras'),
        ('manufactura', 'Industrias manufactureras'),
        ('energia', 'Suministro de electricidad, gas, vapor y aire acondicionado'),
        ('agua', 'Distribución de agua y saneamiento ambiental'),
        ('construccion', 'Construcción'),
        ('comercio', 'Comercio al por mayor y al por menor'),
        ('transporte', 'Transporte y almacenamiento'),
        ('alojamiento', 'Alojamiento y servicios de comida'),
        ('informacion', 'Información y comunicaciones'),
        ('financiero', 'Actividades financieras y de seguros'),
        ('inmobiliario', 'Actividades inmobiliarias'),
        ('profesional', 'Actividades profesionales, científicas y técnicas'),
        ('administrativo', 'Actividades de servicios administrativos y de apoyo'),
        ('publica', 'Administración pública y defensa'),
        ('educacion', 'Educación'),
        ('salud', 'Atención de la salud humana y asistencia social'),
        ('arte', 'Actividades artísticas y de entretenimiento'),
        ('otros_servicios', 'Otras actividades de servicios'),
        ('hogar', 'Actividades de los hogares como empleadores'),
        ('extraterritoriales', 'Actividades de organizaciones extraterritoriales'),
        ('tecnologia', 'Tecnología y desarrollo de software'),
        ('consultoria', 'Consultoría empresarial'),
        ('investigacion', 'Investigación y desarrollo'),
        ('ong', 'Organizaciones sin ánimo de lucro'),
        ('deportes', 'Deportes y recreación'),
        ('medios', 'Medios de comunicación'),
        ('farmaceutica', 'Industria farmacéutica'),
        ('biotecnologia', 'Biotecnología'),
        ('seguridad', 'Seguridad y vigilancia'),
        ('ambiental', 'Servicios ambientales y reciclaje'),
        ('logistica', 'Logística y cadena de suministro'),
        ('telecomunicaciones', 'Telecomunicaciones'),
        ('otro', 'Otro sector')
    ], validators=[DataRequired()]) 