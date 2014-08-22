# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class A(Base):
    __tablename__ = 'a'
    a = Column(String(250), primary_key=True)
    b = Column(String(250), nullable=True)
    c = Column(String(250), nullable=True)
    d = Column(String(250), nullable=True)

engine = create_engine('mysql://root:123456@localhost/test')
Base.metadata.create_all(engine)

