from psycopg2.extras import RealDictCursor

from app.db import get_connection


class PacienteDAO:
    def crear_tabla(self):
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

    def crear(self, paciente):
        sql = """
        INSERT INTO public.paciente (cedula, fechanac, primern, segundon, primera, segundoa)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        paciente.cedula,
                        paciente.fechanac,
                        paciente.primern,
                        paciente.segundon,
                        paciente.primera,
                        paciente.segundoa,
                    ),
                )
                conn.commit()

    def obtener_por_cedula(self, cedula):
        sql = """
        SELECT cedula, fechanac, primern, segundon, primera, segundoa
        FROM public.paciente
        WHERE cedula = %s;
        """
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, (cedula,))
                return cur.fetchone()

    def listar(self):
        sql = """
        SELECT cedula, fechanac, primern, segundon, primera, segundoa
        FROM public.paciente
        ORDER BY cedula;
        """
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql)
                return cur.fetchall()

    def actualizar(self, paciente):
        sql = """
        UPDATE public.paciente
        SET fechanac = %s, primern = %s, segundon = %s, primera = %s, segundoa = %s
        WHERE cedula = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        paciente.fechanac,
                        paciente.primern,
                        paciente.segundon,
                        paciente.primera,
                        paciente.segundoa,
                        paciente.cedula,
                    ),
                )
                conn.commit()
                return cur.rowcount

    def eliminar(self, cedula):
        sql = """
        DELETE FROM public.paciente
        WHERE cedula = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (cedula,))
                conn.commit()
                return cur.rowcount
