import axios from 'axios'
import type { POIFeatureCollection, POIGeoJSON, POIProperties } from '../types/poi'

const API_BASE = '/api'

export const fetchPoisByBbox = async (bbox: string): Promise<POIFeatureCollection> => {
  const response = await axios.get(`${API_BASE}/pois`, { params: { bbox } })
  return response.data
}

export const fetchPoiById = async (id: number): Promise<POIGeoJSON> => {
  const response = await axios.get(`${API_BASE}/pois/${id}`)
  return response.data
}

export const createPoi = async (poi: POIGeoJSON): Promise<any> => {
  const response = await axios.post(`${API_BASE}/pois`, poi)
  return response.data
}

export const updatePoi = async (id: number, properties: POIProperties): Promise<any> => {
  const response = await axios.put(`${API_BASE}/pois/${id}`, properties)
  return response.data
}

export const deletePoi = async (id: number): Promise<any> => {
  const response = await axios.delete(`${API_BASE}/pois/${id}`)
  return response.data
}
