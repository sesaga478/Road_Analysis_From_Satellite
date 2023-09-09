import osmnx as ox

def shp_down_bb(north, south, east, west,shp_out):
    # Create a network graph from OpenStreetMap data within the bounding box
    graph = ox.graph_from_bbox(north, south, east, west, network_type='drive')
    graph_proj = ox.project_graph(graph)
    # Save the graph as a shapefile or GeoJSON if needed
    ox.save_graph_shapefile(graph_proj, filepath=shp_out)
