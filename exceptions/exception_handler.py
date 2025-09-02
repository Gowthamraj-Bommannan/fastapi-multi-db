from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not Found"):
        super().__init__(
            status_code=404,
            detail=detail
            )
        
class AlreadyExistsException(HTTPException):
    def __init__(self, detail: str = "Already Exists"):
        super().__init__(
            status_code=409,
            detail=detail
            )
        
class InvalidInputException(HTTPException):
    def __init__(self, detail: str = "Invalid Input"):
        super().__init__(
            status_code=400,
            detail=detail
            )

async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
            )
        
async def already_exists_exception_handler(request: Request, exc: AlreadyExistsException):
    return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
            )

async def invalid_input_exception_handler(request: Request, exc: InvalidInputException):
    return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
            )

def handle_exception(app):
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(AlreadyExistsException, already_exists_exception_handler)
    app.add_exception_handler(InvalidInputException, invalid_input_exception_handler)
