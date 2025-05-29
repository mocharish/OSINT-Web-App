from .core import HarvesterScanner, AmassScanner

class ScannerFactory:
    @staticmethod
    def create_scanner(name: str):
        if name == "theHarvester":
            return HarvesterScanner("theHarvester")  # CLI tool is in PATH
        elif name == "amass":
            return AmassScanner("amass")  # CLI tool is in PATH
        else:
            raise ValueError(f"Unsupported scanner: {name}")
