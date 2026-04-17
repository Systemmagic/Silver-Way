export interface POIProperties {
  id?: number;
  name: string;
  type: string;
}

export interface POIGeoJSON {
  type: string;
  geometry: {
    type: string;
    coordinates: [number, number];
  };
  properties: POIProperties;
}

export interface POIFeatureCollection {
  type: string;
  features: POIGeoJSON[];
}
