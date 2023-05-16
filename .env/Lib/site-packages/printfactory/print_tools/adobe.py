import pathlib
import platform

from typing import List

from .. import Printer, PrintTool


class AdobeReader(PrintTool):
    """
    Adobe Reader specific model

    !!! Windows only !!!

    Using Adobe Reader (AcroRd32.exe) or Adobe Acrobat (Acrobat.exe)

    AcroRd32.exe [OPTIONS] PATHNAME
        /n  Start a separate instance of Acrobat or Adobe Reader, even if one is currently open.
        /s  Suppress the splash screen.
        /o  Suppress the open file dialog box.
        /h  Start Acrobat or Adobe Reader in a minimized window.
        /p  Start Adobe Reader and display the Print dialog box.

    AcroRd32.exe /t PATH [PRINTERNAME] [DRIVERNAME] [PORTNAME]
        Start Adobe Reader and print a file while suppressing the Print dialog box. The PATH must be fully specified.
        PRINTERNAME     The name of your printer. If not specified, the systems default printer is used.
        DRIVERNAME      Your printer driver’s name, as it appears in your printer’s properties.
        PORTNAME        The printer’s port. PORTNAME cannot contain any "/" characters;
                        if it does, output is routed to the default port for that printer.
    """
    def __init__(
            self,
            printer: Printer,
            app_path: pathlib.Path = pathlib.Path(r'C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe'),
            **kwargs,
    ):
        pltfrm = platform.system()
        if pltfrm != 'Windows':
            raise NotImplementedError
        super(AdobeReader, self).__init__(
            printer=printer,
            app_path=app_path,
            **kwargs,
        )
        self.name = kwargs.get('name', 'Adobe Reader')

    def _set_args(self, print_file: pathlib.Path) -> List[str]:
        reader_args = [
            '/n',  # Start a separate instance of Acrobat or Adobe Reader, even if one is currently open
            '/t',
            print_file
        ]
        if self.printer.name:
            reader_args.append(self.printer.name)
            if self.printer.driver:
                reader_args.append(self.printer.driver)
                if self.printer.port:
                    reader_args.append(self.printer.port)

        args = self.set_args(
            reader_args
        )
        return args

    def print_file(self, file: pathlib.Path, copies: int = 1, **kwargs) -> bool:
        if not file.absolute().exists():
            raise FileNotFoundError(f'"{file.absolute()}" does not exist')

        if type(copies) is not int or copies < 1:
            raise ValueError(f'{copies} is not a valid number of copies')

        self._set_args(print_file=file.absolute())

        success = True
        for i in range(copies):
            proc = self.run()
            if proc.returncode > 1:
                success = False

        return success


class AdobeAcrobat(AdobeReader):
    """
    Adobe Acrobat specific model

    !!! Windows only !!!

    Implementation details see :class:`AdobeReader`

    **Known issues**

    - Currently files could only be printed to the systems default printer.
      This is due to a problem with the command line arguments sent to Adobe Acrobat Pro.
    """
    def __init__(
            self,
            printer: Printer,
            app_path: pathlib.Path = pathlib.Path(r'C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe'),
            **kwargs,
    ):
        super(AdobeAcrobat, self).__init__(
            printer=printer,
            app_path=app_path,
            **kwargs
        )
        self.name = kwargs.get('name', 'Adobe Acrobat')

    def _set_args(self, print_file: pathlib.Path) -> List[str]:
        reader_args = [
            '/n',  # Start a separate instance of Acrobat or Adobe Reader, even if one is currently open
            '/t',
            print_file
        ]
        args = self.set_args(
            reader_args
        )
        return args
