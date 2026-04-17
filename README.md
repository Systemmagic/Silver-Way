# Silver Way

适老化生活圈 WebGIS 平台示例项目，后端使用 Flask + PostGIS，前端使用 Vue3 + OpenLayers + TypeScript。

## 目录结构

```text
backend/
frontend/
```

## 后端启动

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端默认地址：`http://127.0.0.1:5000`

## 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端默认地址：`http://localhost:3000`

## 关键配置

1. 修改 `backend/config.py` 中数据库连接参数（尤其 `password`）。
2. 在 `frontend/src/components/MapContainer.vue` 中替换 `tiandituKey`。若无天地图密钥，程序会自动加载OSM底图
3. 确保 PostGIS 存在 `public_facilities` 表。
4. 确保 SRID `4490` 可用。

## 接口概览

- `GET /api/pois?bbox=minLon,minLat,maxLon,maxLat`
- `GET /api/pois/<poi_id>`
- `POST /api/pois`
- `PUT /api/pois/<poi_id>`
- `DELETE /api/pois/<poi_id>`
