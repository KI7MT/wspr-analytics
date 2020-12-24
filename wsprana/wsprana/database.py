from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base

from .waprana import __database__


Base = declarative_base()

class CSVFile(Base):
    """Object representing a CSV File"""
    __tablename__ = "csvfile"

    csvfile_id = Column(Integer(), primary_key=True)
    name = Column(String(30), index=True)
    year = Column(Integer)
    month = Column(String(2))
    coulmns = Column(Integer())
    records = Column(Integer())
    decompressed_size = Column(Integer())
    compressed_size = Column(Integer())
    csv_file_path = Column(String(255))
    weburl = Column(String(255))
    added_on = Column(DateTime(), default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return "CSVFile(csvfile_id={self.csvfile_id}, " \
                        "name = {self.name}, " \
                        "year = {self.year}, " \
                        "month = {self.month}, "\
                        "columns = {self.columns}, "\
                        "records={}, "\
                        "decompressed_size = {self.decompressed_size}, " \
                        "compressed_size = {self.compressed_size}, " \
                        "csv_file_path = {self.cev_file_path}, " \
                        "weburl = {self.weburl}, " \
                        "added_on =  {self.added_on})".format(self.self)


engine = create.engine(__database__)
Base.metadata.create_all(engine)