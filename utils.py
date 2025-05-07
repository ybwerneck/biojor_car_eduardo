

from shapely.geometry import box
import geopandas as gpd

import geopandas as gpd
from shapely.geometry import box

from shapely.geometry import box
import geopandas as gpd

def find_intersections(gdf, ucs, min_area=0.0001):
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
        # Find possible matches within the UC's bounding box using the spatial index
        possible_matches = list(gdf_sindex.intersection(ucs_geom.bounds))
        # Iterate through possible matches and check if there is an actual intersection
        for prop_idx in possible_matches:
            prop_geom = gdf.geometry.iloc[prop_idx]
            
            # Check if there is an intersection using the `intersects()` method
            if ucs_geom.intersects(prop_geom):
                intersection = ucs_geom.intersection(prop_geom)
            #    print(ucs_idx)
                try:
                    # Check if the intersection is valid and meets the minimum area threshold
                    if not intersection.is_empty and intersection.area >= min_area:
                        intersection_data.append({
                            "property_id": gdf.iloc[prop_idx]["cod_imovel"],
                            "uc_id": ucs.iloc[ucs_idx]["id"] if "id" in ucs.columns else ucs.iloc[ucs_idx]["FID"] if "FID" in ucs.columns else ucs_idx,
                            "intersection_area": intersection.area,
                            "geometry": intersection
                        })
                except Exception as e:
                    continue
        
    # Create a GeoDataFrame for intersections
    intersecting_gdf = gpd.GeoDataFrame(intersection_data, geometry="geometry", crs=gdf.crs)
    
    return intersecting_gdf




def gpu_intersection(gdf1: gpd.GeoDataFrame, gdf2: gpd.GeoDataFrame, output_file: str):
    # Ensure that the dataframes have the same CRS
    if gdf1.crs != gdf2.crs:
        raise ValueError("CRS of gdf1 and gdf2 must be the same.")

    scale=1.0   
    max_depth=10
    max_size=1000
    # Convert GeoDataFrames to cuDF DataFrames for GPU processing
    gdf1_cudf = cuspatial.from_geopandas(gdf1)
    polygons = gdf1_cudf['geometry']

    poly_bboxes = cuspatial.polygon_bounding_boxes(
        polygons
    )
    intersections = cuspatial.join_quadtree_and_bounding_boxes(
        quadtree,
        poly_bboxes,
        polygons.polygons.x.min(),
        polygons.polygons.x.max(),
        polygons.polygons.y.min(),
        polygons.polygons.y.max(),
        scale,
        max_depth
    )
    polygons_and_points = cuspatial.quadtree_point_in_polygon(
        intersections,
        quadtree,
        point_indices,
        points,
        polygons
    )
    print(polygons_and_points.head())
    print(result.head())

    return result_gdf
