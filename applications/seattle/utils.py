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


# def normalize_text(text):
#     if not text:
#         return

#     text = str(text)
#     # Normalize: strip, lowercase, collapse whitespace
#     return " ".join(text.strip().lower().split())

import unicodedata
import re

def normalize_text(text):
    if text is None:
        return ""

    if isinstance(text, (int, float)):
        return str(text)

    # Normalize unicode (handles weird encodings)
    text = unicodedata.normalize("NFKD", text)


    # Lowercase
    text = text.lower()

    # Remove special characters (keep letters, numbers, spaces, dashes and forward slashs)
    text = re.sub(r"[^a-z0-9\s\-\/]", "", text)

    # Collapse multiple spaces → single space
    text = " ".join(text.strip().split())

    return text