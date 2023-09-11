#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie  

DATABASE_URL = 'sqlite:///freebies.db'

# Create a database engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    # sample companies
    company1 = Company(name='TechCorp', founding_year=2000)
    company2 = Company(name='CodeTech', founding_year=2010)
    
    # sample devs
    dev1 = Dev(name='Lionel Messi')
    dev2 = Dev(name='Arling Haaland')
    
    # Add sample companies and devs to the session
    session.add_all([company1, company2, dev1, dev2])
    session.commit()
    
    # sample freebies associated with companies and devs
    freebie1 = Freebie(item_name='Laptop', value=1000, developer=dev1, company=company1)
    freebie2 = Freebie(item_name='T-shirt', value=20, developer=dev1, company=company2)
    freebie3 = Freebie(item_name='Mouse', value=30, developer=dev2, company=company1)
    
    # Add sample freebies to the session
    session.add_all([freebie1, freebie2, freebie3])
    session.commit()
    
    print("Sample data created successfully.")
