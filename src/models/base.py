from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData


metadata_obj = MetaData(schema='ai_consult')

Base = declarative_base(metadata=metadata_obj)
