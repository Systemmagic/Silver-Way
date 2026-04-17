<template>
  <div class="app-container">
    <div class="map-wrapper">
      <MapContainer
        ref="mapContainerRef"
        @map-ready="onMapReady"
        @feature-selected="onFeatureSelected"
        @bbox-changed="onBboxChanged"
      />
    </div>
    <div class="panel-wrapper">
      <PoiPanel
        :bbox="currentBbox"
        @feature-selected="onPanelFeatureSelected"
        @refresh-map="onRefreshMap"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import MapContainer from './components/MapContainer.vue'
import PoiPanel from './components/PoiPanel.vue'
import type Map from 'ol/Map'

const mapContainerRef = ref<InstanceType<typeof MapContainer> | null>(null)
const currentBbox = ref('')
let mapInstance: Map | null = null

function onMapReady(map: Map) {
  mapInstance = map
}

function onFeatureSelected(feature: any) {
}

function onPanelFeatureSelected(payload: any) {
  if (mapContainerRef.value && payload.geometry) {
    const coords = payload.geometry.coordinates
    mapInstance?.getView().animate({
      center: coords,
      zoom: 16,
      duration: 500
    })
  }
}

function onRefreshMap() {
  mapContainerRef.value?.refresh()
}

function onBboxChanged(bbox: string) {
  currentBbox.value = bbox
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body,
#app {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.app-container {
  display: flex;
  width: 100%;
  height: 100%;
}

.map-wrapper {
  flex: 1;
  height: 100%;
}

.panel-wrapper {
  width: 400px;
  height: 100%;
  background-color: #fff;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}
</style>
