import pathlib
import platform
import subprocess

from typing import List

from . import Printer


class PrintTool:
    """Generic PrintTool"""

    def __init__(
            self,
            printer: Printer,
            app_path: pathlib.Path,
            args: List[str] = None,
            name: str = 'Generic PrintTool',
            timeout: int = 60,
    ):
        self.printer = printer
        self.app_path = app_path
        self.args = args
        self.name = name
        self.timeout = timeout

        if not self.exists():
            raise FileNotFoundError(f'PrintTool "{app_path}" does not exist')

    def __str__(self):
        return str(f'{self.__class__.__name__}(printer={self.printer}, app_path="{self.app_path}", '
                   f'args={self.args}, name="{self.name}", timeout={self.timeout})')

    def exists(self) -> bool:
        if not self.app_path.is_dir():
            return self.app_path.exists()
        return False

    def get_args(self) -> List[str]:
        return self.args

    def set_args(self, args: List[str]) -> List[str]:
        self.args = args
        return self.args

    def add_args(self, args: List[str]) -> List[str]:
        self.args.extend(args)
        return self.args

    def run(self) -> subprocess.CompletedProcess:
        pltfrm = platform.system()
        if pltfrm == 'Windows':
            shell = False
        elif pltfrm == 'Darwin':
            shell = True
        else:
            raise NotImplementedError

        args = [self.app_path.absolute()]
        if self.args:
            args.extend(self.args)

        proc = subprocess.run(
            args=args,
            capture_output=True,
            encoding='utf-8',
            text=True,
            shell=shell,
            timeout=self.timeout,
        )

        return proc

    def print_file(self, file: pathlib.Path, copies: int = 1, **kwargs):
        pass
