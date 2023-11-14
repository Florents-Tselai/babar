import os.path


"Tests extension files (.control, .sql, Makefile) are created and populated properly"


def test_control_file(ext, user_path):
    assert ext.name == "pystring"
    # control params are passed correctly
    assert ext.control.comment == "this is the pystring extension"
    assert ext.control.default_version == "0.1.0"

    # defaults are set properly
    assert ext.control.superuser
    assert not ext.control.trusted
    assert not ext.control.relocatable

    assert ext.control_filename == "pystring.control"
    assert ext.control_file.payload.splitlines() == [
        "default_version = '0.1.0'",
        "comment = 'this is the pystring extension'",
        "superuser = true",
        "requires = 'plpython3u'",
    ]

    assert os.path.exists(user_path / "pystring.control")


def test_makefile_file(ext, user_path):
    assert ext.makefile.name_prefix == "Makefile"

    assert ext.makefile.payload.splitlines() == [
        "EXTENSION = pystring",
        "DATA = pystring--0.1.0.sql",
        "PG_CONFIG = pg_config",
        "PGXS := $(shell $(PG_CONFIG) --pgxs)",
        "include $(PGXS)",
    ]

    assert os.path.exists(user_path / ext.makefile_filename)


def test_sql_file(ext, user_path):
    assert ext.sql_file.name_prefix == "pystring--0.1.0.sql"
    assert ext.sql_file._components[0].sql.startswith("create function")
    assert ext.sql_file.payload.startswith("create function")
    assert os.path.exists(user_path / "pystring--0.1.0.sql")


def test_ext_tarfile(ext, user_path):
    pass
    # assert os.path.exists(user_path / ext.tar_filename)
