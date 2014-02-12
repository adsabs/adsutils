class NoReferenceDataSupplied(Exception):
    """
    For those cases where we haven't been given any data
    """
    pass
class InvalidReferenceDataSupplied(Exception):
    """
    We either accept reference stings or a list of reference strings
    """
    pass
class ResolveRequestFailed(Exception):
    """
    For some reason the reference resolver connection blew up
    """
    pass
class UnicodeDecodingError(Exception):
    """
    There was junk in the reference string that the Unicode handler did not like
    """
    pass