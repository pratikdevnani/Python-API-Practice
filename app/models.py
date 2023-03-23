from database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

# due to the limitations of sqlalchemy, if we make changes to the model, we need to delete the old table and then a new model will be created
# this occurs cause if "posts" is already present, what happens is sql driver skips the model based on name
class Post(Base):
    # give the tablename that should be there in postgres
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
