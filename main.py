import sys
from config import URL, CONTIGENCIAS_FILE
from parsers.html_table_parser import HTMLTableParser
from managers.contigencias_manager import ContigenciasManager
from services.sefaz_checker import SEFAZContigenciaChecker
from notifiers.manager import NotificationManager

if __name__ == "__main__":
    # Escolher plataforma via argumento
    platform = sys.argv[1] if len(sys.argv) > 1 else "discord"
    
    parser = HTMLTableParser()
    contigencias_manager = ContigenciasManager(CONTIGENCIAS_FILE)
    checker = SEFAZContigenciaChecker(URL, parser, contigencias_manager)
    notification_manager = NotificationManager(platform)
    
    checker.check()
    checker.notify(notification_manager)