from sqlmodel import Field, SQLModel

class Import(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    pais: str = Field(index=True)
    ano: str
    total: int | None = Field(default=None)

class ImpFrescas(Import, table=True):
    pass

class ImpPassas(Import, table=True):
    pass

class ImpSuco(Import, table=True):
    pass

class ImpVinhos(Import, table=True):
    pass