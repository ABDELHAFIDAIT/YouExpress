from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class YouExpressException(Exception) :
    pass


class EntityNotFound(YouExpressException) :
    def __init__(self, entity: str, id: int):
        self.entity = entity
        self.id = id
        self.message = f"{entity} avec l'ID {id} est Introuvable !"
        super().__init__(self.message)


class BusinessRuleError(YouExpressException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DatabaseError(YouExpressException) :
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        
        
        


def add_exception_handlers(app:FastAPI) :
    
    @app.exception_handler(EntityNotFound)
    async def not_found_handler(request: Request, exc: EntityNotFound) :
        return JSONResponse(
            status_code=404,
            content={"error" : "Not Found", "detail" : exc.message}
        )
    
    
    @app.exception_handler(BusinessRuleError)
    async def business_rule_handler(request: Request, exc:BusinessRuleError) :
        return JSONResponse(
            status_code=400,
            content={"error" : "Business Logic Error", "detail" : exc.message}
        )
        
    
    @app.exception_handler(DatabaseError)
    async def db_error_handler(request: Request, exc:DatabaseError) :
        return JSONResponse(
            status_code=500,
            content={"error" : "Database Error", "detail" : exc.message}
        )