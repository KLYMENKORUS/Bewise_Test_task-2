import datetime
import uuid

from sqlalchemy import MetaData, UUID, String, TIMESTAMP, \
    ForeignKey, Table, Column, Boolean, LargeBinary

metadata = MetaData()

user = Table(
    'user',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4),
    Column('username', String(255), nullable=False),
    Column('email', String(128), nullable=False),
    Column('register_at', TIMESTAMP, default=datetime.datetime.utcnow),
    Column("hashed_password", String(128), nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

audio_file = Table(
    'audio_file',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4),
    Column('user', UUID, ForeignKey('user.id', ondelete='CASCADE')),
    Column('name_file', String(128), nullable=False, unique=True),
    Column('data', LargeBinary(), nullable=False,),
)