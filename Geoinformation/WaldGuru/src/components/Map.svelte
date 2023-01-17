<script lang="ts">
  import { onMount } from 'svelte'
  import { PUBLIC_MAPBOX_TOKEN } from '$env/static/public'

  onMount(() => {
    // @ts-ignore
    const mapbox = window.mapboxgl

    mapbox.accessToken = PUBLIC_MAPBOX_TOKEN
    const map = new mapbox.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/satellite-v9',
      center: [15.4395, 47.0707],
      maxBounds: [
        // Southwest corner of styria
        [13.5, 46.5],
        // Northeast corner of styria
        [17.5, 47.5],
      ],
      zoom: 15,
      pitch: 45,
      maxPitch: 60,
    })

    map.on('style.load', () => {
      map.addSource('mapbox-dem', {
        type: 'raster-dem',
        url: 'mapbox://mapbox.mapbox-terrain-dem-v1',
        tileSize: 512,
        maxzoom: 15,
      })
      // add the DEM source as a terrain layer with exaggerated height
      map.setTerrain({ source: 'mapbox-dem', exaggeration: 1 })

      map.addLayer({
        id: 'wms-test-layer',
        type: 'raster',
        source: {
          type: 'raster',
          tiles: [
            'https://gis.stmk.gv.at/arcgis/services/OGD/flaewi/MapServer/WMSServer' +
              '?bbox={bbox-epsg-3857}' +
              '&format=image/png' +
              // '&format=image/svg+xml' +
              '&service=WMS' +
              '&version=1.1.1' +
              '&request=GetMap' +
              '&srs=EPSG:3857' +
              '&width=256' +
              '&height=256' +
              '&layers=Grundstuecksgrenzen' +
              '&styles=default',
          ],
          tileSize: 256,
        },
        paint: {
          'raster-opacity': 0.25,
        },
      })
    })
  })
</script>

<svelte:head>
  <script src="https://api.mapbox.com/mapbox-gl-js/v2.11.0/mapbox-gl.js"></script>
  <link href="https://api.mapbox.com/mapbox-gl-js/v2.11.0/mapbox-gl.css" rel="stylesheet" />
</svelte:head>

<div id="map" class="w-full h-full" />
