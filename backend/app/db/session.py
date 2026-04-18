from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()
# Keep DB connection attempts short so fallback mode can start quickly without Postgres.
engine = create_engine(
	settings.database_url,
	pool_pre_ping=True,
	connect_args={"connect_timeout": 3},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
