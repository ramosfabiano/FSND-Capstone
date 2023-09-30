from pydantic import BaseModel

class ErrorSchema(BaseModel):
    """ Error message schema.
    """
    message: str

def ErrorRepresentation(error: str):
    """ Returns the representation of an error.
    """
    return {
        "message": error
    }
