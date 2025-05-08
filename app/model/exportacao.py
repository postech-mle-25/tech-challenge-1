from sqlmodel import Field, SQLModel


class Export(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    pais: str = Field(index=True)
    ano: str
    total: int | None = Field(default=None)


class ExpEspumantes(Export, table=True):
    pass


class ExpSuco(Export, table=True):
    pass


class ExpUva(Export, table=True):
    pass


class ExpVinhos(Export, table=True):
    pass
