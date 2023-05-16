import platform
import re
import subprocess

from typing import List


class Printer:
    """Main printer class"""

    def __init__(
            self,
            printer_name: str = None,
            driver_name: str = None,
            port_name: str = None,
            _default: bool = False
    ):
        """
        Initialize Printer class

        :param printer_name: Name of the printer, use systems default printer if not given
        :param driver_name: Driver name that should be used
        :param port_name: Port of the printer
        :param _default: True if printer is the systems default printer, else False
        """
        self.name: str = printer_name
        self.driver: str = driver_name
        self.port: str = port_name
        self._default: bool = _default

        if not self.name and (self.driver or self.port):
            raise TypeError('Missing printer')
        elif not self.driver and self.port:
            raise TypeError('Missing driver')

    def __repr__(self):
        return f'{self.__class__.__name__}(printer_name="{self.name}", driver_name="{self.driver}", port_name="{self.port}", default="{self._default}")'

    def is_default(self):
        return self._default

    @staticmethod
    def get_list() -> List['Printer']:
        """Get a list of installed printers

        :return: List of printers
        """
        # @todo: Return default system printer name at position 0
        args = None
        shell = False
        pltfrm = platform.system()
        if pltfrm == 'Windows':
            args = ['wmic', 'printer', 'get', 'Default,DriverName,Name,PortName']
        # elif pltfrm == 'Darwin':
        #     args = ["lpstat -p | awk '{print $2}'"]
        #     shell = True
        else:
            raise NotImplementedError

        proc = subprocess.run(
            args=args,
            capture_output=True,
            encoding='utf-8',
            text=True,
            shell=shell,
        )

        lines = proc.stdout.splitlines()
        printers = []
        for line in lines:
            line = line.strip()
            if line not in [None, '', '\n'] and not line.startswith('Default'):
                # values in a line as defined above in the args (alphabetical order):
                # Default, DriverName, Name, PortName
                # Windows only implementation
                values = re.split(r'\s{2,}', line)
                printer = Printer(
                    printer_name=values[2],
                    driver_name=values[1],
                    port_name=values[3],
                    _default=True if values[0].lower() in ['true', '1', 't', 'y', 'yes'] else False,
                )
                printers.append(printer)

        return printers

    @classmethod
    def get_default(cls) -> 'Printer':
        """Get the default printer

        :return: Printer
        """
        printers = Printer.get_list()
        for printer in printers:
            if printer._default:
                return printer
