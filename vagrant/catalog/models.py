from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """
    Registered user information is stored in db
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    Uname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Catalog(Base):
    """
    Catalog entries are stored in db
    """
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    Cname = Column(String(250), nullable=False, unique=True)
    catalog_image = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.Cname,
            'catalog_id': self.id,
            'catalog_image': self.catalog_image,
            'user_id': self.user_id,
        }


class Item(Base):
    """
    items entries are stored in db
    """
    __tablename__ = 'item'

    Iname = Column(String(80), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
    description = Column(String)
    pieces = Column(Integer)
    item_image = Column(String(250))
    created_at = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.Iname,
            'description': self.description,
            'pieces': self.pieces,
            'item_image': self.item_image,
            'catalog_id': self.catalog_id,
            'user_id': self.user_id,
        }


engine = create_engine('sqlite:///legocatalog.db')


Base.metadata.create_all(engine)
