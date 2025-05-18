from sqlmodel import Field, SQLModel


class Exporta(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pais: str = Field(index=True)
    arquivo: str
    pasta: str
    ano: str
    quantidade: int | None = Field(default=None)
    valor: int | None = Field(default=None)


class Importa(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pais: str = Field(index=True)
    arquivo: str
    pasta: str
    ano: str
    quantidade: int | None = Field(default=None)
    valor: int | None = Field(default=None)


class Producao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    control: str = Field(index=True)
    arquivo: str
    pasta: str
    ano: int
    quantidade: int | None = Field(default=None)



class Comercio(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    control: str = Field(index=True)
    arquivo: str
    pasta: str
    ano: int
    quantidade: int | None = Field(default=None)


class Processamento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    control: str = Field(index=True)
    arquivo: str
    pasta: str
    ano: int
    quantidade: int | None = Field(default=None)
