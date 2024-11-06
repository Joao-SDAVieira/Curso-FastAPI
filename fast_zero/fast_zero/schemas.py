from pydantic import BaseModel

class Message(BaseModel): #A partir daí a função deve retornar esse padrão
    message : str 
    