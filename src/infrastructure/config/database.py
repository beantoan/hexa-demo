from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str
    port: int
    username: str
    password: str
    database: str

    @property
    def url(self) -> str:
        return f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"