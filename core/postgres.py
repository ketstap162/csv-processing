from core.settings import settings, Settings


class PsqlUrl:
    name: str | None = None
    sync_url: str | None = None
    async_url: str | None = None

    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        name: str,
        port: int = 5432,
    ):
        self.name = name
        self.sync_url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"  # noqa: E231
        self.async_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"  # noqa: E231

    @classmethod
    def create_using_settings(cls, settings: Settings):
        return PsqlUrl(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            name=settings.POSTGRES_DB,
            port=settings.POSTGRES_PORT
        )


postgres_url = PsqlUrl.create_using_settings(settings=settings)