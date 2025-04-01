import geopandas as gpd

def find_intersections(gdf, ucs, min_area=0.0001):
#    print(gdf)
    """
    Finds intersections between two GeoDataFrames (gdf and ucs) using spatial indexes
    and returns a GeoDataFrame containing the intersection geometries.
    
    Parameters:
    gdf (GeoDataFrame): GeoDataFrame of properties.
    ucs (GeoDataFrame): GeoDataFrame of UCs (units).
    min_area (float): Minimum area threshold for intersections. Defaults to 0.0001.
    
    Returns:
    GeoDataFrame: A GeoDataFrame containing intersections.
    """
    # Create spatial indexes for faster intersection lookup
    gdf_sindex = gdf.sindex
    ucs_sindex = ucs.sindex
    
    # List to store intersection results
    intersection_data = []
    
    # Iterate over UCs to find overlapping properties
    for ucs_idx, ucs_geom in ucs.geometry.items():
        # Find possible matches within the UC's bounding box
        possible_matches = list(gdf_sindex.intersection(ucs_geom.bounds))

        for prop_idx in possible_matches:
            prop_geom = gdf.geometry.iloc[prop_idx]
            #print(gdf.iloc[prop_idx])
            # Check for intersection
            if ucs_geom.intersects(prop_geom):
                intersection = ucs_geom.intersection(prop_geom)
                
                # Verify intersection area exceeds threshold
                if not intersection.is_empty and intersection.area >= min_area:
                    intersection_data.append({
                        "property_id": gdf.iloc[prop_idx]["cod_imovel"],
                        "uc_id": ucs.iloc[ucs_idx]["id"],
                        "intersection_area": intersection.area,
                        "geometry": intersection
                    })
    
    # Create a GeoDataFrame for intersections
    intersecting_gdf = gpd.GeoDataFrame(intersection_data, geometry="geometry", crs=gdf.crs)
    
    return intersecting_gdf

# Example usage:
# intersecting_gdf = find_intersections(gdf, ucs, min_area=0.0001)
