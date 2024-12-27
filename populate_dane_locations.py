import requests
import json
from descriptores_app import db, app
from models import Departamento, Municipio

def get_dane_data():
    """Obtiene datos de departamentos y municipios del DANE con paginación"""
    base_url = "https://www.datos.gov.co/resource/xdk5-pm3f.json"
    limit = 2000  # Aumentamos el límite por petición
    offset = 0
    all_data = []

    while True:
        url = f"{base_url}?$limit={limit}&$offset={offset}"
        try:
            print(f"Obteniendo datos con offset {offset}...")
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if not data:  # Si no hay más datos, salimos del bucle
                    break
                all_data.extend(data)
                offset += limit
                print(f"Registros obtenidos hasta ahora: {len(all_data)}")
            else:
                print(f"Error al obtener datos: Status code {response.status_code}")
                break
        except Exception as e:
            print(f"Error en la solicitud: {str(e)}")
            break

    print(f"Total final de registros obtenidos: {len(all_data)}")
    return all_data

def clean_codigo(codigo):
    """Limpia y formatea el código para asegurar consistencia"""
    if codigo:
        return str(codigo).strip()
    return None

def populate_locations():
    with app.app_context():
        try:
            # Limpiar datos existentes
            print("Limpiando datos existentes...")
            Municipio.query.delete()
            Departamento.query.delete()
            db.session.commit()

            # Obtener datos del DANE
            print("Obteniendo datos del DANE...")
            data = get_dane_data()
            if not data:
                print("No se pudieron obtener datos del DANE")
                return

            # Procesar departamentos primero
            print("Procesando departamentos...")
            departamentos = {}
            dept_ids = {}

            for item in data:
                dept_code = clean_codigo(item.get('c_digo_dane_del_departamento'))
                dept_name = item.get('departamento')
                
                if dept_code and dept_name and dept_code not in departamentos:
                    departamentos[dept_code] = dept_name
                    try:
                        departamento = Departamento(
                            codigo=dept_code,
                            nombre=dept_name
                        )
                        db.session.add(departamento)
                        db.session.flush()  # Para obtener el ID generado
                        dept_ids[dept_code] = departamento.id
                        print(f"Departamento agregado: {dept_name} (ID: {departamento.id})")
                    except Exception as e:
                        print(f"Error al insertar departamento {dept_name}: {str(e)}")
                        continue

            db.session.commit()
            print(f"Departamentos insertados: {len(departamentos)}")

            # Procesar municipios
            print("Procesando municipios...")
            municipios_count = 0
            municipios_por_departamento = {}

            for item in data:
                mun_code = clean_codigo(item.get('c_digo_dane_del_municipio'))
                mun_name = item.get('municipio')
                dept_code = clean_codigo(item.get('c_digo_dane_del_departamento'))

                if mun_code and mun_name and dept_code in dept_ids:
                    if dept_code not in municipios_por_departamento:
                        municipios_por_departamento[dept_code] = set()
                    
                    if mun_name not in municipios_por_departamento[dept_code]:
                        municipios_por_departamento[dept_code].add(mun_name)
                        try:
                            municipio = Municipio(
                                codigo=mun_code,
                                nombre=mun_name,
                                departamento_id=dept_ids[dept_code]
                            )
                            db.session.add(municipio)
                            municipios_count += 1
                            
                            if municipios_count % 100 == 0:
                                print(f"Procesados {municipios_count} municipios...")
                                db.session.commit()

                        except Exception as e:
                            print(f"Error al insertar municipio {mun_name} ({mun_code}): {str(e)}")
                            continue

            # Commit final
            db.session.commit()

            # Imprimir resumen
            print("\nResumen de municipios por departamento:")
            for dept_code, municipios in municipios_por_departamento.items():
                dept_name = departamentos.get(dept_code, "Desconocido")
                print(f"{dept_name}: {len(municipios)} municipios")

            print(f"\nTotal final: {len(departamentos)} departamentos y {municipios_count} municipios")

        except Exception as e:
            db.session.rollback()
            print(f"Error al insertar datos: {str(e)}")
            import traceback
            print(traceback.format_exc())

if __name__ == '__main__':
    populate_locations() 