from sqlmodel import Field, SQLModel


class Producao(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    control: str = Field(index=True)
    produto: str
    ano: int
    total: int | None = Field(default=None)


class Comercio(Producao, table=True):
    pass
