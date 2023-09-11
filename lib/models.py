from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, dev, item_name, value, session):
        new_freebie = Freebie(item_name=item_name, value=value, developer=dev, company=self)
        session.add(new_freebie)
        session.commit()
        return new_freebie

    @classmethod
    def oldest_company(cls, session):
        oldest = session.query(cls).order_by(cls.founding_year).first()
        return oldest


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        for freebie in self.freebies:
            if freebie.item_name == item_name:
                return True
        return False

    def give_away(self, other_dev, freebie, session):

        if freebie.developer == self:
            freebie.developer = other_dev
            session.commit()


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)

    dev_id = Column(Integer, ForeignKey('devs.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)

    developer = relationship('Dev', backref='freebies')
    company = relationship('Company', backref='freebies')

    @classmethod
    def create_freebie(cls, item_name, value, developer, company, session):
        new_freebie = cls(item_name=item_name, value=value, developer=developer, company=company)
        session.add(new_freebie)
        session.commit()
        return new_freebie

    def get_dev_and_company(self):
        return self.developer, self.company
    
    def print_details(self):
        return f'{self.developer.name} owns a {self.item_name} from {self.company.name}'

engine = create_engine('sqlite:///freebies.db')  
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
