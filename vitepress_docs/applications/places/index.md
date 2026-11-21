---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "Places Application"
  tagline: Application built using Django Web Framework and Leaflet JS library
  actions:
    - theme: brand
      text: App Structure
      link: ./structure.md
    # - theme: alt
    #   text: Folium
    #   link: https://python-visualization.github.io/folium/latest/

features:
  - title: Interactive Web Map
    details: An interactive web map built using leaflet js that displays data about places.
  - title: CRUD Operations
    details: Create, Read, Update and Delete operations for Place, Review, Type and Tags database models.
  - title: Dynamic Filtering
    details: Dynamic data filtering for Place model, both in the interactive map and a Bootstrap table.

---

::: details
Libraries and Packages used
* [Django Web Framework](https://www.djangoproject.com/)

* [django-filter](https://django-filter.readthedocs.io/en/stable/guide/usage.html/)

* [Leaflet.js](https://leafletjs.com/)
:::