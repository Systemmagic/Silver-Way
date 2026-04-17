from flask import Blueprint, request, jsonify
from services import poi_service

poi_bp = Blueprint('poi', __name__)


@poi_bp.route('/pois', methods=['GET'])
def get_pois():
    bbox = request.args.get('bbox')
    if not bbox:
        return jsonify({"error": "bbox parameter required"}), 400
    try:
        feature_collection = poi_service.get_pois_in_bbox(bbox)
        return jsonify(feature_collection)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@poi_bp.route('/pois/<int:poi_id>', methods=['GET'])
def get_poi(poi_id):
    poi = poi_service.get_poi_by_id(poi_id)
    if poi:
        return jsonify(poi)
    return jsonify({"error": "POI not found"}), 404


@poi_bp.route('/pois', methods=['POST'])
def add_poi():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    result = poi_service.add_poi(data)
    return jsonify(result), 201 if result['status'] == 'success' else 500


@poi_bp.route('/pois/<int:poi_id>', methods=['PUT'])
def update_poi(poi_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    result = poi_service.update_poi(poi_id, data)
    return jsonify(result), 200 if result['status'] == 'success' else 500


@poi_bp.route('/pois/<int:poi_id>', methods=['DELETE'])
def delete_poi(poi_id):
    result = poi_service.delete_poi(poi_id)
    return jsonify(result), 200 if result['status'] == 'success' else 500
