from pydantic import Field, BaseModel


class Register(BaseModel):
    name: str
    email: str
    username: str
    password: str = Field(exclude=True)
