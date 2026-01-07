from pydantic import BaseModel , EmailStr

class UserBase(BaseModel):
    nom : str
    prenom : str
    telephone : str
    
    class Config:
        from_attributes = True
        
        
        
class LivreurCreate(UserBase):
    vehicule : str
    zone_assigne : str
    
class LivreurRead(UserBase):
    id : int
    vehicule : str
    zone_assigne : str
    
    

class ExpediteurCreate(UserBase):
    adresse : str
    email : EmailStr
    
class ExpediteurRead(UserBase):
    id: int
    adresse : str
    email : EmailStr
    
    

class AdminCreate(UserBase):
    pass

class AdminRead(UserBase):
    id : int
    
    
    
class DestinataireCreate(UserBase):
    adresse : str
    email : EmailStr
    
class DestinataireRead(UserBase):
    id : int
    adresse : str
    email : EmailStr
    

    