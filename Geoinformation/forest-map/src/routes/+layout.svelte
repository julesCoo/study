<script>
  import '../app.css'
</script>

<div class="bg-lime-900 w-screen h-screen overflow-hidden flex flex-col">
  <header class="bg-lime-700 h-14 text-white p-4">
    <span class="text-lg">Forest Map</span>
  </header>
  <main class="flex flex-1">
    <div id="sidebar" class="w-14 bg-lime-700" />
    <slot />
  </main>
</div>
