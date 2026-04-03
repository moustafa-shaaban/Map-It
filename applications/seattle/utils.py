import unicodedata
import re
from django.utils.encoding import force_str
from django.utils.html import escape
import folium
from folium.plugins import MarkerCluster

def normalize_text(text):
    """Full normalization for uniqueness. Writen with help from Grok AI"""
    text = force_str(text or "") # Source: https://docs.djangoproject.com/en/6.0/ref/utils/#django.utils.encoding.force_str
    text = unicodedata.normalize("NFKD", text).lower() # Remove accents from text ("café" to "cafe") Source: https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize
    text = re.sub(r"[^a-z0-9\s\-\/]", "", text) # Accept only A to Z + 0 to 9 and dash ( - ) + forward slash ( / )
    # Collapse multiple whitespace into single space and strip
    return " ".join(text.split())



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

# import unicodedata
# import re
# def normalize_text(text):
#     if not text:
#         return

#     text = str(text)
#     # Normalize: strip, lowercase, collapse whitespace
#     return " ".join(text.strip().lower().split())
