import os
from datetime import datetime, date, time
from zoneinfo import ZoneInfo

import psycopg2
from psycopg2.extras import RealDictCursor


# ==========================
# Conexión a PostgreSQL
# ==========================

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )


# ==========================
# Crear tabla si no existe
# ==========================

def crear_tabla():
    sql = """
    CREATE TABLE IF NOT EXISTS public.paciente
    (
        cedula numeric(11,0) NOT NULL,
        fechanac timestamp with time zone NOT NULL,
        primern character varying(255) NOT NULL,
        segundon character varying(255),
        primera character varying(255) NOT NULL,
        segundoa character varying(255),
        CONSTRAINT pk_paciente PRIMARY KEY (cedula)
    );
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()


# ==========================
# Utilidades
# ==========================

def convertir_fecha(fecha_texto):
    """
    Acepta:
    - YYYY-MM-DD
    - YYYY-MM-DD HH:MM
    - YYYY-MM-DDTHH:MM:SS
    """

    zona = ZoneInfo("America/Bogota")

    try:
        if len(fecha_texto.strip()) == 10:
            fecha = date.fromisoformat(fecha_texto)
            return datetime.combine(fecha, time.min, tzinfo=zona)

        fecha = datetime.fromisoformat(fecha_texto)

        if fecha.tzinfo is None:
            fecha = fecha.replace(tzinfo=zona)

        return fecha

    except ValueError:
        raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD o YYYY-MM-DD HH:MM")


def validar_cedula(cedula):
    cedula = str(cedula).strip()

    if not cedula.isdigit():
        raise ValueError("La cédula debe contener solo números.")

    if len(cedula) > 11:
        raise ValueError("La cédula no puede tener más de 11 dígitos.")

    return int(cedula)


def texto_opcional(valor):
    valor = valor.strip()
    return valor if valor else None


# ==========================
# CRUD Paciente
# ==========================

def crear_paciente(cedula, fechanac, primern, segundon, primera, segundoa):
    sql = """
    INSERT INTO public.paciente
    (
        cedula,
        fechanac,
        primern,
        segundon,
        primera,
        segundoa
    )
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                cedula,
                fechanac,
                primern,
                segundon,
                primera,
                segundoa
            ))
            conn.commit()


def obtener_paciente_por_cedula(cedula):
    sql = """
    SELECT
        cedula,
        fechanac,
        primern,
        segundon,
        primera,
        segundoa
    FROM public.paciente
    WHERE cedula = %s;
    """

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (cedula,))
            return cur.fetchone()


def listar_pacientes():
    sql = """
    SELECT
        cedula,
        fechanac,
        primern,
        segundon,
        primera,
        segundoa
    FROM public.paciente
    ORDER BY cedula;
    """

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            return cur.fetchall()


def actualizar_paciente(cedula, fechanac, primern, segundon, primera, segundoa):
    sql = """
    UPDATE public.paciente
    SET
        fechanac = %s,
        primern = %s,
        segundon = %s,
        primera = %s,
        segundoa = %s
    WHERE cedula = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                fechanac,
                primern,
                segundon,
                primera,
                segundoa,
                cedula
            ))
            conn.commit()
            return cur.rowcount


def eliminar_paciente(cedula):
    sql = """
    DELETE FROM public.paciente
    WHERE cedula = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (cedula,))
            conn.commit()
            return cur.rowcount


# ==========================
# Interfaz por consola
# ==========================

def pedir_datos_paciente():
    cedula = validar_cedula(input("Cédula: "))
    fechanac = convertir_fecha(input("Fecha de nacimiento YYYY-MM-DD: "))

    primern = input("Primer nombre: ").strip()
    if not primern:
        raise ValueError("El primer nombre es obligatorio.")

    segundon = texto_opcional(input("Segundo nombre, opcional: "))

    primera = input("Primer apellido: ").strip()
    if not primera:
        raise ValueError("El primer apellido es obligatorio.")

    segundoa = texto_opcional(input("Segundo apellido, opcional: "))

    return cedula, fechanac, primern, segundon, primera, segundoa


def imprimir_paciente(paciente):
    if not paciente:
        print("No se encontró el paciente.")
        return

    print("-" * 40)
    print(f"Cédula: {paciente['cedula']}")
    print(f"Fecha nacimiento: {paciente['fechanac']}")
    print(f"Primer nombre: {paciente['primern']}")
    print(f"Segundo nombre: {paciente['segundon'] or ''}")
    print(f"Primer apellido: {paciente['primera']}")
    print(f"Segundo apellido: {paciente['segundoa'] or ''}")
    print("-" * 40)


def menu():
    crear_tabla()

    while True:
        print("\n===== CRUD PACIENTE =====")
        print("1. Crear paciente")
        print("2. Consultar paciente por cédula")
        print("3. Listar pacientes")
        print("4. Actualizar paciente")
        print("5. Eliminar paciente")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                datos = pedir_datos_paciente()
                crear_paciente(*datos)
                print("Paciente creado correctamente.")

            elif opcion == "2":
                cedula = validar_cedula(input("Ingrese la cédula: "))
                paciente = obtener_paciente_por_cedula(cedula)
                imprimir_paciente(paciente)

            elif opcion == "3":
                pacientes = listar_pacientes()

                if not pacientes:
                    print("No hay pacientes registrados.")
                else:
                    for paciente in pacientes:
                        imprimir_paciente(paciente)

            elif opcion == "4":
                cedula = validar_cedula(input("Cédula del paciente a actualizar: "))

                paciente = obtener_paciente_por_cedula(cedula)
                if not paciente:
                    print("No existe un paciente con esa cédula.")
                    continue

                print("Ingrese los nuevos datos del paciente.")
                fechanac = convertir_fecha(input("Fecha de nacimiento YYYY-MM-DD: "))

                primern = input("Primer nombre: ").strip()
                if not primern:
                    raise ValueError("El primer nombre es obligatorio.")

                segundon = texto_opcional(input("Segundo nombre, opcional: "))

                primera = input("Primer apellido: ").strip()
                if not primera:
                    raise ValueError("El primer apellido es obligatorio.")

                segundoa = texto_opcional(input("Segundo apellido, opcional: "))

                filas = actualizar_paciente(
                    cedula,
                    fechanac,
                    primern,
                    segundon,
                    primera,
                    segundoa
                )

                if filas > 0:
                    print("Paciente actualizado correctamente.")
                else:
                    print("No se pudo actualizar el paciente.")

            elif opcion == "5":
                cedula = validar_cedula(input("Cédula del paciente a eliminar: "))
                filas = eliminar_paciente(cedula)

                if filas > 0:
                    print("Paciente eliminado correctamente.")
                else:
                    print("No existe un paciente con esa cédula.")

            elif opcion == "0":
                print("Saliendo...")
                break

            else:
                print("Opción no válida.")

        except psycopg2.IntegrityError as e:
            print("Error de integridad en la base de datos.")
            print("Detalle:", e)

        except psycopg2.Error as e:
            print("Error de PostgreSQL.")
            print("Detalle:", e)

        except ValueError as e:
            print("Error de validación:", e)

        except Exception as e:
            print("Error inesperado:", e)


if __name__ == "__main__":
    menu()
