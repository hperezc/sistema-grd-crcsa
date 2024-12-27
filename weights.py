# Pesos de las dimensiones (debe sumar 100%)
DIMENSION_WEIGHTS = {
    'procesos': 30,
    'regulaciones': 20,
    'equipamiento': 30,
    'integracion': 10,
    'organizacion': 10
}

# Pesos de los componentes dentro de cada dimensión (debe sumar 100% por dimensión)
COMPONENT_WEIGHTS = {
    'procesos': {
        'p1_identificacion_amenazas': 17,
        'p2_identificacion_vulnerabilidades': 17,
        'p3_analisis_riesgos': 10,
        'p4_valoracion_riesgos': 10,
        'p5_reduccion_riesgos': 20,
        'p6_monitoreo_revision': 8,
        'p7_seguimiento_estrategias': 8,
        'p8_comunicacion': 10
    },
    'regulaciones': {
        'pt1_adopcion_certificaciones': 5,
        'pt2_regulaciones_nacionales': 10,
        'pt3_plan_gestion_riesgo': 20,
        'pt4_politica_gestion_riesgo': 5,
        'pt5_politica_seguridad': 10,
        'pt6_sistema_sarlaft': 5,
        'pt7_memoria_emergencias': 10,
        'pt8_planes_emergencia': 15,
        'pt9_seguros_polizas': 20
    },
    'equipamiento': {
        'eq1_control_acceso': 13.4,
        'eq2_controles_seguridad': 13.3,
        'eq3_controles_ciberseguridad': 20,
        'eq4_redes_deteccion': 13.3,
        'eq5_brigadas_respuesta': 20,
        'eq6_formacion_capacitacion': 20
    },
    'integracion': {
        'it1_transversalizacion': 20,
        'it2_protocolos_comunicacion': 25,
        'it3_planes_ayuda': 10,
        'it5_retroalimentacion': 25,
        'it6_mecanismos_articulacion': 20
    },
    'organizacion': {
        'or1_area_gestion': 20,
        'or2_presupuesto': 30,
        'or3_personal_dedicacion': 15,
        'or4_proyectos_gestion': 15,
        'or5_inclusion_gestion': 20
    }
}

# Diagnósticos por rango de calificación para cada dimensión
DIAGNOSTICS = {
    'procesos': {
        (0, 40): "La organización cuenta con una base establecida para los procesos de gestión del riesgo, sin embargo, se debe fortalecer su construcción en diversos componentes con el fin de apalancar su avance.",
        (40.01, 80): "La organización ha fortalecido los procesos de la gestión del riesgo en un nivel significativo y es posible seguir avanzando, para que la gestión del riesgo abarque gran parte de las áreas de la empresa y mejore su operación.",
        (80.01, 100): "La organización cuenta con una estructura de procesos para la gestión del riesgo sólida que le permite operar de manera más segura en el tiempo. Es importante seguir trabajando por el mantenimiento de los componentes ya consolidados, con actividades de seguimiento y mejora constantes.",
    },

    'regulaciones': {
        (0, 40): "Si bien existe una base establecida que permita proteger a la organización en caso de manifestación del riesgo, existe mucho por mejorar para evitar grandes impactos en diferentes áreas de la empresa de orden legal, financiero y físico.",
        (40.01, 80): "Se cuenta con un avance significativo en cumplimiento de las regulaciones y políticas, sin embargo, aún existen componentes que deben ser abordados de manera puntual con el fin de reducir los impactos y efectos de eventos adversos.",
        (80.01, 100): "Se cumplen y adoptan certificaciones nacionales e internacionales para la gestión del riesgo, con planes y políticas internos que permiten minimizar los impactos y efectos de eventos adversos. Existen componentes puntuales por mejorar, sumado a actividades de seguimiento y monitoreo de lo construido.",
    },

    'equipamiento': {
        (0, 40): "Existe una base definida para la respuesta ante eventos adversos, sin embargo, muchos componentes están en un nivel mínimo. Hay mucho por mejorar para evitar los impactos y efectos de situaciones de emergencia y contingencia.",
        (40.01, 80): "Se cuenta con un avance significativo en los equipamientos, conocimientos técnicos y capacidades para dar respuesta a eventos adversos y mejorar la seguridad, sin embargo, hay ciertos componentes que aún pueden mejorarse para fortalecer la organización.",
        (80.01, 100): "La organización cuenta con unas capacidades robustas para la respuesta ante eventos adversos presentados, realiza seguimiento y monitoreo además de capacitarse constantemente. Existen componentes puntuales que es posible mejorar para alcanzar un nivel más avanzado.",
    },

    'integracion': {
        (0, 40): "La transversalidad de la gestión del riesgo aún puede mejorarse de manera significativa. Otras áreas de la organización deben involucrarse en los procesos de planeación y divulgación de la gestión del riesgo. Aún es posible vincularse con actores externos para fortalecer la respuesta y conocimiento.",
        (40.01, 80): "Existe una base consolidada en la integración y transversalidad de la gestión del riesgo a nivel organizacional, sin embargo, aún queda camino para fortalecer algunos componentes en esta dimensión e involucrar actores internos y externos en su construcción.",
        (80.01, 100): "La organización lleva a cabo la integración y transversalización de la gestión del riesgo con actores internos y externos, que le permiten responder, planear y evolucionar en el tiempo. Se recomienda continuar con actividades de seguimiento y mantenimiento, además de mejorar componentes puntuales.",
    },

    'organizacion': {
        (0, 40): "Se cuenta con una base incipiente en términos organizativos para la gestión del riesgo a nivel organizacional. Existe un camino largo para el fortalecimiento de la estructura organizacional con el fin de dar respuesta y planeación en el tiempo.",
        (40.01, 80): "A nivel organizacional se cuenta con un área de gestión del riesgo consolidada, para identificar, planear y monitorear los riesgos a los cuales se encuentra expuesta. Aún es posible fortalecer diversos componentes y la inclusión para permitir una mejor planeación, respuesta y evolución ante eventos adversos.",
        (80.01, 100): "La organización cuenta con un área definida, estructurada y con capacidades presupuestales, para identificar, analizar y dar respuesta, a los riesgos a los cuales se encuentra expuesta. Se debe seguir manteniendo y fortaleciendo en el tiempo para alcanzar un nivel avanzado. Existen componentes puntuales aún por mejorar.",
    }
} 