from marcingest import field_handlers as fh

## Configuration options ##

SOLR_URL = "http://localhost/solr/"

FIELD_HANDLERS = {
    'DataType': fh.datatype,
    'ThemeKeywords': fh.theme_keywords_concat,
    'ThemeKeywordsSort': fh.theme_keywords,
    'PlaceKeywords': fh.place_keywords_concat,
    'PlaceKeywordsSort': fh.place_keywords,
    'Publisher': fh.publisher,
    'LayerId': fh.layer_id,
    'Location': fh.location,
    'Name': fh.name,
    'LayerDisplayName': fh.layer_display_name,
    'ContentDate': fh.content_date,
    'Abstract': fh.abstract,
    'MinX': fh.min_x,
    'MaxX': fh.max_x,
    'MinY': fh.min_y,
    'MaxY': fh.max_y,
    'CenterX': fh.center_x,
    'CenterY': fh.center_y,
    'Area': fh.area,
    'HalfWidth': fh.half_width,
    'HalfHeight': fh.half_height,
    'Access': "Public",
    'Availability': "Offline",
    'GeoReferenced': False,
    'Institution': "MIT"
}
