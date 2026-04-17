from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PublicFacility(Base):
    __tablename__ = 'public_facilities'
     # 主键 gid
    id = Column(Integer, name='gid', primary_key=True)
    
    # 设施名称（当前表仅有中文列“名称”）
    name_cn = Column(String, name='名称')
    
    # 分类信息
    category_main = Column(String, name='大类')
    category_mid = Column(String, name='中类')
    category_sub = Column(String, name='小类')
    
    # 地址与行政区划
    address = Column(String, name='地址')
    province = Column(String, name='省')
    city = Column(String, name='市')
    district = Column(String, name='区')   
    
    # 空间几何字段
    geom = Column(Geometry('POINT', srid=4490), name='geom')