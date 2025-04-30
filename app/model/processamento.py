from sqlmodel import Field, SQLModel

class Processamento(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    control: str = Field(index=True)
    cultivar: str
    ano: int
    total: int | None = Field(default=None)

class ProcessaAmericanas(Processamento, table=True):
    pass

class ProcessaMesa(Processamento, table=True):
    pass

class ProcessaSemclass(Processamento, table=True):
    pass

class ProcessaViniferas(Processamento, table=True):
    pass