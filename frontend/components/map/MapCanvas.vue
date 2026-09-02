<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import { useCountryColors } from '@/composables/useCountryColors'

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
let selectedMarker: L.CircleMarker | null = null

// Single source of truth for country colors — also used in the dashboard's
// legend card, so a sighting's dot always matches its legend entry.
const { COUNTRY_COLORS } = useCountryColors()

// Cluster colours (12 clusters from your DBSCAN) — cycles by cluster id,
// no fixed name-to-color mapping, so the legend explains this via hover text
// rather than listing all 12.
const clusterColors = [
  '#FF0000', '#0066FF', '#00CC00', '#9900CC', '#FF6600',
  '#CC0066', '#FFCC00', '#00CCCC', '#CC9900', '#FF3399',
  '#339966', '#993366',
]

// Matches the app's theme primary — used for both the study area outline
// and the selected-point marker so the two "your input" elements read as
// visually related.
const ACCENT_COLOR = '#7367F0'

const initMap = () => {
  if (!mapContainer.value)
    return

  map = L.map(mapContainer.value, {
    center: [-18, 30],
    zoom: 5,
    zoomControl: true,
  })

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map)

  // Exact bounding box from Chapter 3.1.2 — same extent used for
  // pseudo-absence generation and the prediction grid
  const STUDY_AREA_BOUNDS: L.LatLngBoundsExpression = [
    [-26, 20], // SW corner
    [-8, 36], // NE corner
  ]

  boundaryLayer = L.rectangle(STUDY_AREA_BOUNDS, {
    color: ACCENT_COLOR,
    weight: 2,
    dashArray: '6 6',
    fill: false,
    interactive: false, // lets clicks pass through to the map for point prediction
  })
  if (props.showStudyArea)
    boundaryLayer.addTo(map)

  // Handle click events — mark exactly where the user clicked, replacing
  // any previous selection, so the prediction card's coordinates always
  // have a visible anchor on the map itself.
  map.on('click', (e: L.LeafletMouseEvent) => {
    if (selectedMarker)
      selectedMarker.removeFrom(map!)

    selectedMarker = L.circleMarker(e.latlng, {
      radius: 9,
      color: '#ffffff',
      weight: 3,
      fillColor: ACCENT_COLOR,
      fillOpacity: 1,
    }).addTo(map!)

    emit('pointSelected', e.latlng.lat, e.latlng.lng)
  })

  renderLayers()

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
  if (!map)
    return

  if (markerLayer) {
    markerLayer.clearLayers()
    markerLayer.removeFrom(map)
  }

  markerLayer = L.layerGroup().addTo(map)

  if (!props.sightings || props.sightings.length === 0)
    return

  props.sightings.forEach((sighting) => {
    const lat = sighting.decimalLatitude
    const lon = sighting.decimalLongitude
    if (!lat || !lon)
      return

    let color = '#888888'
    let radius = 4
    let popupText = `${sighting.countryCode} - ${sighting.year}`

    if (props.showClusters && sighting.cluster !== undefined && sighting.cluster !== -1) {
      color = clusterColors[sighting.cluster % clusterColors.length]
      radius = 6
      popupText = `Cluster ${sighting.cluster} - ${sighting.countryCode} - ${sighting.year}`
    }
    else if (props.showSightings && !props.showClusters) {
      color = COUNTRY_COLORS[sighting.countryCode] || '#888888'
      radius = 4
    }
    else if (!props.showSightings && !props.showClusters) {
      return // Don't show anything if both are off
    }

    if (props.showHeatmap)
      radius = 8

    const circle = L.circleMarker([lat, lon], {
      radius,
      color,
      fillColor: color,
      fillOpacity: props.showHeatmap ? 0.3 : 0.7,
      weight: 1,
      opacity: 0.8,
    })

    circle.bindPopup(popupText)
    circle.addTo(markerLayer!)
  })
}

watch(() => [props.showSightings, props.showClusters, props.showHeatmap], () => {
  renderLayers()
})

watch(() => props.sightings, () => {
  renderLayers()
}, { deep: true })

onMounted(() => {
  initMap()
})

const cleanup = () => {
  if (map) {
    map.remove()
    map = null
  }
}

if (import.meta.hot)
  import.meta.hot.dispose(cleanup)
</script>

<template>
  <div ref="mapContainer" class="map-canvas-wrapper" />
</template>

<style scoped>
.map-canvas-wrapper {
  width: 100%;
  height: 100%;
  min-height: 500px;
  position: relative;
}
</style>
