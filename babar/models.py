from dataclasses import dataclass, field, asdict
from typing import Callable, Iterator, Union, Optional, List
import tarfile
from pathlib import Path
from tarfile import TarFile
from abc import ABC, abstractmethod
from .pg import PgObject
from pydantic import BaseModel
from textwrap import wrap
from .pg import PgFunction
from abc import ABC


@dataclass(init=True)
class ControlParams:
    """https://www.postgresql.org/docs/current/extend-extensions.html#EXTEND-EXTENSIONS-FILES"""

    directory: Optional[str] = None
    default_version: Optional[str] = None
    comment: Optional[str] = None
    encoding: Optional[str] = None
    module_pathname: Optional[str] = None
    no_relocate: Optional[str] = None
    schema: Optional[str] = None

    superuser: Optional[bool] = True
    trusted: Optional[bool] = False
    relocatable: Optional[bool] = False
    requires: list = field(default_factory=lambda: ["plpython3u"])


class ExtensionFile:
    _name: str
    _prefix: str

    def __init__(self, name: str, prefix: str):
        self._name = name
        self._prefix = prefix

    @property
    def name_prefix(self):
        return self._name + "." + self._prefix if self._prefix else self._name

    def full_path(self, workpath: Path):
        return workpath / self.name_prefix

    @property
    @abstractmethod
    def payload(self):
        pass

    def write(self, workpath: Path):
        with open(self.full_path(workpath), "w") as f:
            f.write(self.payload)


class Makefile(ExtensionFile):
    _name = "Makefile"
    _prefix = ""
    _ext_name = None
    _ext_version = None

    def __init__(self, ext_name: str, ext_version: str, name="Makefile", prefix=""):
        super().__init__(name, prefix)
        self._ext_name = ext_name
        self._ext_version = ext_version

    @property
    def payload(self):
        return "\n".join(
            [
                f"EXTENSION = {self._ext_name}",
                f"DATA = {self._ext_name}--{self._ext_version}.sql",
                "PG_CONFIG = pg_config",
                "PGXS := $(shell $(PG_CONFIG) --pgxs)",
                "include $(PGXS)",
            ]
        )


class ControlFile(ExtensionFile):
    _prefix = "control"
    _params: ControlParams

    def __init__(
        self, name: str, params: ControlParams = None, prefix: str = "control"
    ):
        super().__init__(name, prefix)
        self._params = params

    @property
    def payload(self) -> str:
        """Iterate over control params and print only non-Nones
        Bools should be lowercase
        """

        def gen_str_params():
            for k, v in asdict(self._params).items():
                if v:
                    if type(v) == str:
                        yield f"{k} = '{v}'"
                    elif type(v) == bool:
                        yield k + " = " + str(v).lower()

                    elif type(v) == list:
                        yield k + " = '" + ",".join(v) + "'"

        return "\n".join(gen_str_params())


class SQLFile(ExtensionFile):
    _prefix = "sql"
    _components = []

    def __init__(self, ext_name: str, ext_version: str, prefix="sql"):
        super().__init__(f"{ext_name}--{ext_version}", prefix)
        self._ext_name = ext_name
        self._ext_version = ext_version

    def add(self, obj: PgObject):
        self._components.append(obj)

    @property
    def payload(self) -> str:
        def gen_str_components():
            for c in self._components:
                yield c.sql

        return "\n".join(gen_str_components())


@dataclass(repr=False, init=False)
class Extension:
    name: str
    control: ControlParams
    workdir: Path
    components = []

    ext_tar: TarFile = None

    def __init__(
        self,
        name: str,
        *components,
        workdir: Path = Path.cwd(),
        **control_params,
    ):
        for c in components:
            self.components.append(PgFunction(c))
        self.name = name
        self.workdir = workdir
        self.control = ControlParams()
        for k, v in control_params.items():
            setattr(self.control, k, v)

        self.control_file.write(self.workdir)
        self.makefile.write(self.workdir)
        self.sql_file.write(self.workdir)

    @property
    def control_file(self) -> ControlFile:
        return ControlFile(self.name, self.control)

    @property
    def makefile(self) -> Makefile:
        return Makefile(self.name, self.control.default_version)

    @property
    def sql_file(self) -> SQLFile:
        f = SQLFile(self.name, self.control.default_version)
        for c in self.components:
            f.add(c)
        return f

    @property
    def control_filename(self):
        return self.name + ".control"

    @property
    def control_filepath(self):
        return self.workdir / self.control_filename

    @property
    def control_payload(self) -> str:
        return ""

    @property
    def sql_filename(self) -> str:
        return f"{self.name}--{self.control.default_version}.sql"

    @property
    def sql_filepath(self):
        return self.workdir / self.sql_filename

    @property
    def sql_payload(self) -> str:
        return "\n".join([str(c.sql) for c in self.components])

    @property
    def makefile_filename(self) -> str:
        return "Makefile"

    @property
    def makefile_filepath(self):
        return self.workdir / self.makefile_filename

    @property
    def tar_filename(self) -> str:
        return f"{self.name}--{self.control.default_version}.tar"

    @property
    def tar_filepath(self):
        return self.workdir / f"{self.name}--{self.control.default_version}.tar"

    @property
    def tarfile(self) -> TarFile:
        with tarfile.open(self.tar_filepath, "a") as ret:
            ret.add(self.control_filepath)
            ret.add(self.sql_filepath)
            ret.add(self.makefile_filepath)
            return ret

    def __len__(self):
        return len(self.components)

    def __iter__(self):
        return self.components.__iter__()
