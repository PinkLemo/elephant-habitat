<script setup lang="ts">
import {ref, onMounted, watch} from 'vue'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Fix for Leaflet's default marker icons in Vue
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

const props = defineProps<{
  sightings: Array<{
    decimalLatitude: number
    decimalLongitude: number
    countryCode: string
    year: number
    cluster?: number
  }>
  showSightings: boolean
  showClusters: boolean
  showHeatmap: boolean
  showStudyArea: boolean
}>()

const emit = defineEmits<{
  (e: 'pointSelected', lat: number, lon: number): void
}>()

const mapContainer = ref<HTMLDivElement>()
let map: L.Map | null = null
let markerLayer: L.LayerGroup | null = null
let boundaryLayer: L.Rectangle | null = null

// Country colours matching your notebook
const countryColors: Record<string, string> = {
  ZW: '#00ff00',
  MZ: '#ff8c00',
  ZM: '#0000ff',
  BW: '#ff0000'
}

// Cluster colours (12 clusters from your DBSCAN)
const clusterColors = [
  '#FF0000', '#0066FF', '#00CC00', '#9900CC', '#FF6600',
  '#CC0066', '#FFCC00', '#00CCCC', '#CC9900', '#FF3399',
  '#339966', '#993366'
]

const initMap = () => {
  if (!mapContainer.value) return

  map = L.map(mapContainer.value, {
    center: [-18, 30],
    zoom: 5,
    zoomControl: true
  })

  // Add OpenStreetMap tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map)

  // Exact bounding box from Chapter 3.1.2 — same extent used for
  // pseudo-absence generation and the prediction grid
  const STUDY_AREA_BOUNDS: L.LatLngBoundsExpression = [
    [-26, 20], // SW corner
    [-8, 36],  // NE corner
  ]

  boundaryLayer = L.rectangle(STUDY_AREA_BOUNDS, {
    color: '#7367F0',
    weight: 2,
    dashArray: '6 6',
    fill: false,
    interactive: false, // lets clicks pass through to the map for point prediction
  })
  if (props.showStudyArea)
    boundaryLayer.addTo(map)

  // Handle click events
  map.on('click', (e: L.LeafletMouseEvent) => {
    emit('pointSelected', e.latlng.lat, e.latlng.lng)
  })

  renderLayers()

  // Resize map after a moment (ensures proper rendering)
  setTimeout(() => {
    map?.invalidateSize()
  }, 100)
}

watch(() => props.showStudyArea, (visible) => {
  if (!map || !boundaryLayer)
    return
  visible ? boundaryLayer.addTo(map) : boundaryLayer.removeFrom(map)
})

const renderLayers = () => {
  if (!map) return

  // Remove existing layers
  if (markerLayer) {
    markerLayer.clearLayers()
    markerLayer.removeFrom(map)
  }

  markerLayer = L.layerGroup().addTo(map)

  if (!props.sightings || props.sightings.length === 0) return

  let pointsToShow = props.sightings

  props.sightings.forEach((sighting) => {
    const lat = sighting.decimalLatitude
    const lon = sighting.decimalLongitude
    if (!lat || !lon) return

    let color = '#888888'
    let radius = 4
    let popupText = `${sighting.countryCode} - ${sighting.year}`

    if (props.showClusters && sighting.cluster !== undefined && sighting.cluster !== -1) {
      color = clusterColors[sighting.cluster % clusterColors.length]
      radius = 6
      popupText = `Cluster ${sighting.cluster} - ${sighting.countryCode} - ${sighting.year}`
    } else if (props.showSightings && !props.showClusters) {
      color = countryColors[sighting.countryCode] || '#888888'
      radius = 4
    } else if (!props.showSightings && !props.showClusters) {
      return // Don't show anything if both are off
    }

    // For the heatmap overlay, we'd use a different approach
    // but for now we just show points
    if (props.showHeatmap) {
      // This would be a different layer type
      // For simplicity, we'll use circles with varying opacity
      radius = 8
    }

    const circle = L.circleMarker([lat, lon], {
      radius,
      color,
      fillColor: color,
      fillOpacity: props.showHeatmap ? 0.3 : 0.7,
      weight: 1,
      opacity: 0.8
    })

    circle.bindPopup(popupText)
    circle.addTo(markerLayer!)
  })
}

// Watch for layer toggle changes
watch(() => [props.showSightings, props.showClusters, props.showHeatmap], () => {
  renderLayers()
})

watch(() => props.sightings, () => {
  renderLayers()
}, {deep: true})

onMounted(() => {
  initMap()
})

// Cleanup
const cleanup = () => {
  if (map) {
    map.remove()
    map = null
  }
}

// Component cleanup
if (import.meta.hot) {
  import.meta.hot.dispose(cleanup)
}
</script>

<template>
  <div ref="mapContainer" class="map-canvas-wrapper"></div>
</template>

<style scoped>
.map-canvas-wrapper {
  width: 100%;
  height: 100%;
  min-height: 500px;
  position: relative;
}
</style>
