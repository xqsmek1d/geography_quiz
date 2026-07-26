from shapely.ops import transform

def crosses_antimeridian(geometry):
    """
    Check whether a geometry has parts on both sides of the dateline.
    """
    minx, _, maxx, _ = geometry.bounds
    return minx < -170 and maxx > 170

def shift_longitudes(geometry):
    """
    Shift negative longitudes to the 0-360 range.
    """
    def shift(x, y, z=None):
        if x < 0:
            x += 360

        if z is None:
            return x, y

        return x, y, z

    return transform(shift, geometry)

def get_local_projection(geometry):
    """
    Create a Lambert Azimuthal Equal Area projection centred on a country.
    """
    point = geometry.representative_point()

    return (
        f"+proj=laea "
        f"+lat_0={point.y} "
        f"+lon_0={point.x}"
    )

def prepare_world(gdf, use_dateline_shift):
    """
    Prepare a consistent longitude system for the whole dataset.
    """
    if not use_dateline_shift:
        return gdf

    shifted = gdf.copy()

    shifted["geometry"] = shifted.geometry.apply(
        shift_longitudes
    )

    return shifted