from sqlmodel import Field, SQLModel


class Exporta(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pais: str = Field(index=True)
    ano: str
    total: int | None = Field(default=None)


class Importa(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pais: str = Field(index=True)
    ano: str
    total: int | None = Field(default=None)


class Producao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    control: str = Field(index=True)
    produto: str
    ano: int
    total: int | None = Field(default=None)
    tipo: str


class Comercio(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    control: str = Field(index=True)
    produto: str
    ano: int
    total: int | None = Field(default=None)
    tipo: str


class Processamento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    control: str = Field(index=True)
    cultivar: str
    tipo: str
    ano: int
    total: int | None = Field(default=None)
