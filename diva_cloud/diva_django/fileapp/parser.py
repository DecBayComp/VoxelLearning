from rest_framework import parsers

class ByteParser(parsers.BaseParser):
    """
    octet-stream parser.
    """
    media_type = 'application/octet-stream'

    def parse(self, stream, media_type=None, parser_context=None):
        content = stream.read()
        return content

