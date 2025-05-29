from sqlmodel import Field, SQLModel


class Exporta(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pais: str = Field(index=True)
    tipo: str
    ano: int
    quantidade: int | None = Field(default=None)
    valor: int | None = Field(default=None)


class Importa(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pais: str = Field(index=True)
    tipo: str
    ano: int
    quantidade: int | None = Field(default=None)
    valor: int | None = Field(default=None)


class Producao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    control: str
    produto: str = Field(index=True)
    ano: int
    quantidade: int | None = Field(default=None)


class Comercio(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    control: str
    produto: str = Field(index=True)
    ano: int
    quantidade: int | None = Field(default=None)


class Processamento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    control: str
    cultivar: str = Field(index=True)
    tipo: str
    ano: int
    quantidade: int | None = Field(default=None)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    hashed_password: str