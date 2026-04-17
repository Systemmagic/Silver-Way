# backend/services/poi_service.py
import json
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from geojson import Feature, Point, FeatureCollection
from models.poi_models import PublicFacility
from config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)

def get_pois_in_bbox(bbox_str):
    """空间范围查询，bbox格式：minLon,minLat,maxLon,maxLat (EPSG:4326)"""
    session = SessionLocal()
    try:
        minLon, minLat, maxLon, maxLat = map(float, bbox_str.split(','))
        query = session.query(PublicFacility).filter(
            func.ST_Intersects(
                PublicFacility.geom,
                func.ST_Transform(
                    func.ST_MakeEnvelope(minLon, minLat, maxLon, maxLat, 4326),
                    4490
                )
            )
        )
        facilities = query.all()
        features = []
        for fac in facilities:
            # 获取转换后的 GeoJSON 几何
            geom_transformed = session.query(
                func.ST_AsGeoJSON(func.ST_Transform(fac.geom, 4326))
            ).scalar()
            geojson_geom = json.loads(geom_transformed)
            
            display_name = fac.name_cn
            
            # 处理分类：拼接“大类-中类-小类”
            categories = [fac.category_main, fac.category_mid, fac.category_sub]
            display_type = '-'.join([c for c in categories if c]) or '未分类'
            
            feature = Feature(
                geometry=geojson_geom,
                properties={
                    "id": fac.id,
                    "name": display_name,
                    "type": display_type,
                    "address": fac.address,
                    "city": fac.city,
                    "district": fac.district
                }
            )
            features.append(feature)
        return FeatureCollection(features)
    finally:
        session.close()

def add_poi(geojson_data):
    """新增POI，坐标从前端传来为EPSG:4326，需转为4490存储"""
    session = SessionLocal()
    try:
        coords = geojson_data['geometry']['coordinates']
        properties = geojson_data['properties']

        point_wkt = session.query(
            func.ST_AsText(
                func.ST_Transform(
                    func.ST_SetSRID(func.ST_MakePoint(coords[0], coords[1]), 4326),
                    4490
                )
            )
        ).scalar()

        new_poi = PublicFacility(
            name_cn=properties.get('name'),      # 存入“名称”列
            category_main=properties.get('type'), # 简易处理：前端type存入大类
            geom=point_wkt
        )
        session.add(new_poi)
        session.commit()
        return {"status": "success", "id": new_poi.id}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        session.close()

def update_poi(poi_id, properties):
    """编辑POI属性"""
    session = SessionLocal()
    try:
        poi = session.query(PublicFacility).filter(PublicFacility.id == poi_id).first()
        if not poi:
            return {"status": "error", "message": "POI not found"}
        
        # 更新名称和分类
        if 'name' in properties:
            poi.name_cn = properties['name']
        if 'type' in properties:
            poi.category_main = properties['type']
        if 'address' in properties:
            poi.address = properties['address']
        
        session.commit()
        return {"status": "success"}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        session.close()

def delete_poi(poi_id):
    """删除POI"""
    session = SessionLocal()
    try:
        poi = session.query(PublicFacility).filter(PublicFacility.id == poi_id).first()
        if not poi:
            return {"status": "error", "message": "POI not found"}
        session.delete(poi)
        session.commit()
        return {"status": "success"}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        session.close()

def get_poi_by_id(poi_id):
    """获取单个POI详情"""
    session = SessionLocal()
    try:
        poi = session.query(PublicFacility).filter(PublicFacility.id == poi_id).first()
        if not poi:
            return None
        geom_transformed = session.query(
            func.ST_AsGeoJSON(func.ST_Transform(poi.geom, 4326))
        ).scalar()
        geojson = json.loads(geom_transformed)
        
        display_name = poi.name_cn
        categories = [poi.category_main, poi.category_mid, poi.category_sub]
        display_type = '-'.join([c for c in categories if c]) or '未分类'
        
        return {
            "id": poi.id,
            "name": display_name,
            "type": display_type,
            "address": poi.address,
            "geometry": geojson
        }
    finally:
        session.close()