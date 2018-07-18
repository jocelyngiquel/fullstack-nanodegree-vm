from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    Uname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Catalog(Base):
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    Cname = Column(String(250), nullable=False)
    catalog_image = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.Cname,
            'id': self.id,
            'catalog_image': self.catalog_image,
        }


class Item(Base):
    __tablename__ = 'item'

    Iname = Column(String(80), nullable=False)
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
        }


engine = create_engine('sqlite:///legocatalog.db')


Base.metadata.create_all(engine)
