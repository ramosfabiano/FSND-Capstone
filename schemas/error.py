from pydantic import BaseModel

class ErrorSchema(BaseModel):
    """ Error message schema.
    """
    message: str

def ErrorRepresentation(message='Request failed.'):
    """ Returns the representation of an error.
    """
    return {
        "message": message
    }