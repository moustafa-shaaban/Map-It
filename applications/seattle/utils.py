import unicodedata
import re
from django.utils.encoding import force_str
from django.utils.html import escape
from django.utils.text import slugify
import folium
from folium.plugins import MarkerCluster

# def normalize_text(text):
#     """Full normalization for uniqueness. Writen with help from Grok AI"""
#     text = force_str(text or "") # Source: https://docs.djangoproject.com/en/6.0/ref/utils/#django.utils.encoding.force_str
#     text = unicodedata.normalize("NFKD", text).lower() # Remove accents from text ("café" to "cafe") Source: https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize
#     text = re.sub(r"[^a-z0-9\s\-\/]", "", text) # Accept only A to Z + 0 to 9 and dash ( - ) + forward slash ( / )
#     # Collapse multiple whitespace into single space and strip
#     return " ".join(text.split())


# import bleach

# def normalize_text(text, allow_unicode=False):
#     text = force_str(text or "")

#     # Use Bleach to strip anything that even looks like an HTML tag
#     # tags=[] means no tags allowed, strip=True deletes the angle brackets and tag name
#     text = bleach.clean(text, tags=[], strip=True)
    
#     text = slugify(text, allow_unicode=allow_unicode)
#     text = text.replace('-', ' ')
#     return " ".join(text.split()).lower().strip()


def normalize_text(text, allow_unicode=False):
    """
    Enhanced normalization for uniqueness and security.
    """
    text = force_str(text or "")
    
    # 1. Handle Unicode: If allow_unicode is False, it converts 'café' to 'cafe'
    # Django's slugify handles the NFKD normalization and stripping of non-ascii 
    # more robustly than a manual re.sub.
    text = slugify(text, allow_unicode=allow_unicode)
    
    # 2. Manual refinements (if you specifically need / and spaces preserved)
    # Note: slugify replaces spaces with dashes. If you want spaces, 
    # we swap them back.
    text = text.replace('-', ' ')
    
    # 3. Security: Prevent "Hidden" characters
    # Some unicode characters look like spaces but aren't. 
    # .split() handles all whitespace types (tabs, newlines, etc.)
    return " ".join(text.split()).lower().strip()



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
