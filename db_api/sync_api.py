from db_api.interface_api import DataBaseApiInterface
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_api.models import Base
import subprocess
from config import settings

class DBApiSync(DataBaseApiInterface):
    def __init__(self):
        # обьект сессии для работы с базой в режиме orm
        self.session_db = None
        # движок для работы с orm (psycopg2)
        self.engine_db = None
        self._create_engine()
        self._create_session()

    def _create_engine(self):
        """Создание синхронного движка базы данных"""
        self.engine_db = create_engine(url=settings.url_connect_with_psycopg2, echo=True)

    def _create_session(self):
        """Создание синхронной сессии для работы с базой данных"""
        self.session_db = sessionmaker(self.engine_db)

    def create_tables(self):
        """Создай таблицы указанные в обьекте metadata"""
        # Base.metadata.drop_all(self.engine_db)
        # Base.metadata.create_all(self.engine_db)
        subprocess.run([f"{settings.PATH_WORK}/bash.sh"], capture_output=True, text=True)