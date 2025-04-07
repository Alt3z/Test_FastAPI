from pydantic import BaseModel, Field

class RegUser(BaseModel):
    #id: int = Field(description="ID пользователя")
    user_name: str = Field(min_length=4, max_length=25, description="Имя пользователя")
    password: str = Field(min_length=8, max_length=32, description="Пароль пользователя")

class LogUser(BaseModel):
    user_name: str = Field(min_length=4, max_length=25, description="Имя пользователя")
    password: str = Field(min_length=8, max_length=32, description="Пароль пользователя")