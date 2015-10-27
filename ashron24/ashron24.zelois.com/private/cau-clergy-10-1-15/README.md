# cau-clergy
Draft multilayer Leaflet map with clergy, cbo, and demographic layers

This is a demo of an interactive web mapping application, utilizing leaflet, cartoDB, and a little JQuery. Data sets from NYC DCP (Bytes of the Big Apple), NYC DOT, OpenData, US Census Bureau and the MO-CAU. 

This is a draft version. Lots of kinks to be worked out.

#TODO:
<ul>
<li> Create a _legend_ for layers that need them (i.e. choropleths). This legend needs to either be in a sidebar DIV element or in a popup.
⋅⋅* Make the legend hide-able
⋅⋅* Make the legend items "active" only when the corresponding layer is displayed.
<li> Make hover-over interactivity (or info-window) for polygons and points. (preferably with D3-style info / box).
<li> Move layer selector to a collapsible/minimizable sidebar.  (with a tab for instructions)
<li> Add a secure log-in page.
<li> Convert choropleth items to radio-button type of selector
<li> Add nesting/ layer tree groups - style ala ArcGIS.
<li> Add Map Title
<li> DONE ~~Rotate legend item lables.~~
<li> Fix layer selector to be compatible with mobile/touchscreen devices (scroll issue)
</ul>
