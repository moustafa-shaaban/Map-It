from django.utils.html import escape
import folium
from folium.plugins import MarkerCluster

def render_markers(folium_map, layer, queryset):
    tooltip_field, popup_field = layer['fields']

    # simple_markers    = folium.FeatureGroup(name=f"{layer['label']} Simple Markers", show=layer['label'] == 'Schools').add_to(folium_map)
    simple_markers = folium.FeatureGroup(name=f"{layer['label']} Simple Markers", show=True).add_to(folium_map)
    clustered = folium.FeatureGroup(name=f"{layer['label']} Marker Cluster", show=False).add_to(folium_map)
    cluster = MarkerCluster().add_to(clustered)

    for obj in queryset:
        coords  = [obj.latitude, obj.longitude]
        tooltip = f"{layer['label']}: {escape(str(getattr(obj, tooltip_field)))}"
        popup   = f"Address: {escape(str(getattr(obj, popup_field)))}"

        folium.Marker(coords, icon=folium.Icon(**layer['icon']), tooltip=tooltip, popup=popup).add_to(simple_markers)
        folium.Marker(coords, icon=folium.Icon(**layer['icon']), tooltip=tooltip, popup=popup).add_to(cluster)