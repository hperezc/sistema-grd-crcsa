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