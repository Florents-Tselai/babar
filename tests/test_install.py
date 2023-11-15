import psycopg as pg
from subprocess import run as run_cmd


def drop_extension(extname):
    with pg.connect("dbname=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute(f"drop extension {extname}")


def test_extension_can_be_installed(install_pystring):
    with pg.connect("dbname=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute("select 1 from pg_extension where extname = 'pystring'")

            assert cur.fetchone() == (1,)

    drop_extension("pystring")
