namespace java com.miui.metok.cdc.thrift.GeolocateService

struct Location {
    1: required double lat;
    2: required double lng;
}

service Geolocate {
    Location calculatePosition(1: list<Location> cellList ,2: list<Location> wifiList )
}
