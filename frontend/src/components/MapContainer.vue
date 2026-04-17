<template>
  <div id="map" class="map-container"></div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Map, View } from 'ol'
import TileLayer from 'ol/layer/Tile'
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import OSM from 'ol/source/OSM'
import XYZ from 'ol/source/XYZ'
import { Draw, Select } from 'ol/interaction'
import { GeoJSON } from 'ol/format'
import { Style, Stroke, Fill, Circle as CircleStyle } from 'ol/style'
import type { POIGeoJSON } from '../types/poi'
import { fetchPoisByBbox, createPoi } from '../services/poiApi'

const emit = defineEmits<{
  (e: 'map-ready', map: Map): void
  (e: 'feature-selected', feature: any): void
  (e: 'bbox-changed', bbox: string): void
}>()

const mapRef = ref<Map | null>(null)
const vectorSource = new VectorSource()
const vectorLayer = new VectorLayer({
  source: vectorSource,
  style: new Style({
    image: new CircleStyle({
      radius: 6,
      fill: new Fill({ color: '#3388ff' }),
      stroke: new Stroke({ color: '#fff', width: 2 })
    })
  })
})

onMounted(() => {
  initMap()
})

function initMap() {
  const view = new View({
    projection: 'EPSG:4326',
    center: [112.94, 28.23],
    zoom: 12
  })

  const tiandituKey = ((import.meta.env.VITE_TIANDITU_KEY as string | undefined) ?? '').trim()
  const useTianditu = tiandituKey.length > 0 && tiandituKey !== '你的天地图密钥'

  const baseLayer = new TileLayer({
    source: useTianditu
      ? new XYZ({
          url: `https://t0.tianditu.gov.cn/vec_c/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=vec&STYLE=default&TILEMATRIXSET=c&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=${tiandituKey}`
        })
      : new OSM()
  })

  const map = new Map({
    target: 'map',
    layers: [baseLayer, vectorLayer],
    view
  })

  mapRef.value = map

  const draw = new Draw({
    source: vectorSource,
    type: 'Point'
  })
  map.addInteraction(draw)

  draw.on('drawend', async (e) => {
    const feature = e.feature
    const coords = (feature.getGeometry() as any).getCoordinates()
    const name = prompt('请输入设施名称：')
    const type = prompt('请输入设施类型（如：医疗/助餐/生鲜/公厕）：')
    if (name && type) {
      const geojson: POIGeoJSON = {
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: coords
        },
        properties: { name, type }
      }
      const result = await createPoi(geojson)
      if (result.status === 'success') {
        alert('添加成功')
        loadPoisByCurrentExtent()
      } else {
        alert('添加失败：' + result.message)
      }
    }
    vectorSource.removeFeature(feature)
  })

  const select = new Select()
  map.addInteraction(select)
  select.on('select', (e) => {
    const selected = e.selected[0]
    if (selected) {
      emit('feature-selected', selected)
    }
  })

  map.on('moveend', () => {
    const extent = map.getView().calculateExtent(map.getSize())
    const bbox = extent.join(',')
    emit('bbox-changed', bbox)
    loadPoisByCurrentExtent()
  })

  if (!useTianditu) {
    console.warn('未检测到天地图 Key，已自动回退到 OSM 底图')
  }

  emit('map-ready', map)
  const initialExtent = map.getView().calculateExtent(map.getSize())
  emit('bbox-changed', initialExtent.join(','))
  loadPoisByCurrentExtent()
}

async function loadPoisByCurrentExtent() {
  if (!mapRef.value) return
  const extent = mapRef.value.getView().calculateExtent(mapRef.value.getSize())
  const bbox = extent.join(',')
  try {
    const data = await fetchPoisByBbox(bbox)
    vectorSource.clear()
    const format = new GeoJSON()
    const features = format.readFeatures(data)
    vectorSource.addFeatures(features as any)
  } catch (error) {
    console.error('加载POI失败:', error)
  }
}

function zoomToFeature(feature: any) {
  if (!mapRef.value) return
  const geom = feature.getGeometry()
  if (geom) {
    const extent = geom.getExtent()
    mapRef.value.getView().fit(extent, { duration: 500, maxZoom: 18 })
  }
}

function refresh() {
  loadPoisByCurrentExtent()
}

defineExpose({
  refresh,
  zoomToFeature
})
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
}
</style>
