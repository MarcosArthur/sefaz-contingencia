from html.parser import HTMLParser

class HTMLTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.table_data = []
        self.current_row = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            for attr, value in attrs:
                if attr == "class" and value == "tabelaResultado":
                    self.in_table = True
        elif tag == "tr" and self.in_table:
            self.current_row = []

    def handle_data(self, data):
        if self.in_table and self.current_row is not None:
            self.current_row.append(data.strip())

    def handle_endtag(self, tag):
        if tag == "table" and self.in_table:
            self.in_table = False
        elif tag == "tr" and self.in_table and self.current_row:
            self.table_data.append(self.current_row)
