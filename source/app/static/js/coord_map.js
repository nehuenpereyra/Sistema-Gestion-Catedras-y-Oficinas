function init_map() {
  var map = L.map("mapid").setView([-34.658, -58.474], 9);
  L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
    maxZoom: 19,
  }).addTo(map);
  L.control.scale().addTo(map);
  return map;
}

function add_limits(map) {
  var polyline = new L.Polyline([
    [-34.1959, -58.966],
    [-35.077, -57.73],
  ]).addTo(map);
  map.removeLayer(polyline);
  // Devuleve los limites
  var bounds = polyline.getBounds();

  // Setea los limites
  map.fitBounds(bounds);

  // Restringe solo en esos limites la vista
  map.setMaxBounds(bounds);
}

function add_layer(map) {
  // Se crea una nueva capa para los marcadores
  var markers = new L.FeatureGroup();
  // Se agrega la capa al mapa
  map.addLayer(markers);
  return markers;
}

function get_coord(map, markers) {
  // Al precionar sobre el mapa se agrega un marcador y se retorna las coordenadas
  map.on("click", function (e) {
    markers.clearLayers();
    L.marker(e.latlng).addTo(markers);
    var coord = e.latlng;
    document.getElementById("latitude").value = coord.lat;
    document.getElementById("longitude").value = coord.lng;
  });
}

var map = init_map();
add_limits(map);
markers = add_layer(map);
get_coord(map, markers);

$(document).ready(function () {
  if (document.getElementById("latitude").value !== "") {
    var newLatLng = new L.LatLng(
      document.getElementById("latitude").value,
      document.getElementById("longitude").value
    );
    L.marker(newLatLng).addTo(markers);
  }
});
