from config import URL, CONTIGENCIAS_FILE
from parsers.html_table_parser import HTMLTableParser
from managers.contigencias_manager import ContigenciasManager
from services.sefaz_checker import SEFAZContigenciaChecker

if __name__ == "__main__":
    parser = HTMLTableParser()
    contigencias_manager = ContigenciasManager(CONTIGENCIAS_FILE)
    checker = SEFAZContigenciaChecker(URL, parser, contigencias_manager)
    checker.check_and_notify()
