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

class SuccessSchema(BaseModel):
    """ Success message schema.
    """
    message: str

def SuccessRepresentation(message='Request succeeded.'):
    """ Returns the representation of a succesful request.
    """
    return {
        "message": message
    }
