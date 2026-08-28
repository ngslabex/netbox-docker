import importlib.util
import sys
from pathlib import Path


expected_tile_url = (
    "https://maps.scada.local/"
    "styles/basic-preview/256/"
    "{z}/{x}/{y}.png"
)

required_values = {
    "local_tile": expected_tile_url,
    "offline_layer": "Offline Street",
    "geocode_disabled": "var GEOCODE_URL = null;",
    "offline_geocode_message": (
        "Adres arama offline harita "
        "kurulumunda devre disidir."
    ),
}

forbidden_values = {
    "external_osm": "tile.openstreetmap.org",
    "external_arcgis": "server.arcgisonline.com",
    "external_nominatim": "nominatim.openstreetmap.org",
}


spec = importlib.util.find_spec("netbox_map")

if spec is None or spec.origin is None:
    raise SystemExit(
        "ERROR: netbox_map Python module could not be located."
    )


plugin_root = Path(spec.origin).resolve().parent

site_map_js = (
    plugin_root
    / "static"
    / "netbox_map"
    / "js"
    / "site_map.js"
)


if not site_map_js.is_file():
    raise SystemExit(
        f"ERROR: site_map.js was not found: {site_map_js}"
    )


text = site_map_js.read_text(
    encoding="utf-8"
)


print(f"Checked file: {site_map_js}")
print()


failed = False


print("Required content checks:")

for check_name, expected_value in required_values.items():
    result = expected_value in text

    print(
        "{}={}".format(
            check_name,
            result,
        )
    )

    if not result:
        print(
            "  Missing value: {}".format(
                expected_value
            )
        )
        failed = True


print()
print("External dependency checks:")

for check_name, forbidden_value in forbidden_values.items():
    absent = forbidden_value not in text

    print(
        "{}_absent={}".format(
            check_name,
            absent,
        )
    )

    if not absent:
        print(
            "  Forbidden value remains: {}".format(
                forbidden_value
            )
        )
        failed = True


print()

if failed:
    print(
        "ERROR: One or more offline NetBox Map checks failed."
    )
    sys.exit(1)


print(
    "OK: Image contains the expected offline NetBox Map patch."
)
