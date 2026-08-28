import importlib.util
import os
from pathlib import Path


STYLE_ID = os.environ.get(
    "NETBOX_MAP_OFFLINE_STYLE",
    "",
).strip()

TILE_BASE_URL = os.environ.get(
    "NETBOX_MAP_OFFLINE_TILE_BASE_URL",
    "https://maps.scada.local",
).strip().rstrip("/")

TARGET_FILE = os.environ.get(
    "NETBOX_MAP_TARGET_FILE",
    "",
).strip()


if not STYLE_ID:
    raise SystemExit(
        "ERROR: NETBOX_MAP_OFFLINE_STYLE is empty."
    )


if TARGET_FILE:
    site_map_js = Path(TARGET_FILE)
else:
    spec = importlib.util.find_spec("netbox_map")

    if spec is None or spec.origin is None:
        raise SystemExit(
            "ERROR: netbox_map module could not be located."
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
        f"ERROR: site_map.js not found: {site_map_js}"
    )


text = site_map_js.read_text(
    encoding="utf-8"
)

original = text


# ---------------------------------------------------------
# 1. Replace the public OpenStreetMap tile URL
# ---------------------------------------------------------

old_street_url = (
    "https://{s}.tile.openstreetmap.org/"
    "{z}/{x}/{y}.png"
)

new_street_url = (
    f"{TILE_BASE_URL}/styles/{STYLE_ID}/256/"
    "{z}/{x}/{y}.png"
)

street_url_count = text.count(
    old_street_url
)

if street_url_count != 1:
    raise SystemExit(
        "ERROR: Expected one OpenStreetMap tile URL, "
        f"found {street_url_count}."
    )

text = text.replace(
    old_street_url,
    new_street_url,
    1,
)


# ---------------------------------------------------------
# 2. Remove the online ArcGIS satellite layer
# ---------------------------------------------------------

satellite_start = (
    "    var satellite = L.tileLayer("
)

satellite_end = (
    "    var bounds = L.latLngBounds();"
)

start_index = text.find(
    satellite_start
)

end_index = text.find(
    satellite_end,
    start_index,
)

if start_index == -1:
    raise SystemExit(
        "ERROR: Satellite block start was not found."
    )

if end_index == -1:
    raise SystemExit(
        "ERROR: Satellite block end marker was not found."
    )

satellite_block = text[
    start_index:end_index
]

required_satellite_fragments = (
    "server.arcgisonline.com",
    "streets.addTo(map);",
    (
        "L.control.layers({ "
        "'Street': streets, "
        "'Satellite': satellite "
        "}).addTo(map);"
    ),
    "map.on('baselayerchange'",
)

for fragment in required_satellite_fragments:
    if fragment not in satellite_block:
        raise SystemExit(
            "ERROR: Satellite block structure changed. "
            f"Missing fragment: {fragment}"
        )

replacement_layers = (
    "    streets.addTo(map);\n"
    "    L.control.layers({\n"
    "        'Offline Street': streets\n"
    "    }).addTo(map);\n"
    "\n"
)

text = (
    text[:start_index]
    + replacement_layers
    + text[end_index:]
)


# ---------------------------------------------------------
# 3. Remove the online Nominatim endpoint
# ---------------------------------------------------------

old_geocode_url = (
    "    var GEOCODE_URL = "
    "'https://nominatim.openstreetmap.org/search';"
)

new_geocode_url = (
    "    var GEOCODE_URL = null;"
)

geocode_url_count = text.count(
    old_geocode_url
)

if geocode_url_count != 1:
    raise SystemExit(
        "ERROR: Expected one Nominatim URL declaration, "
        f"found {geocode_url_count}."
    )

text = text.replace(
    old_geocode_url,
    new_geocode_url,
    1,
)


# ---------------------------------------------------------
# 4. Disable address-based geocoding
# ---------------------------------------------------------

old_geocode_start = (
    "    function geocodeSite(site, chip) {\n"
    "        if (!site.physical_address) return;\n"
)

new_geocode_start = (
    "    function geocodeSite(site, chip) {\n"
    "        window.alert(\n"
    "            'Adres arama offline harita kurulumunda "
    "devre disidir. ' +\n"
    "            'Site enlem ve boylam alanlarini "
    "kullanin.'\n"
    "        );\n"
    "        return;\n"
    "\n"
    "        if (!site.physical_address) return;\n"
)

geocode_function_count = text.count(
    old_geocode_start
)

if geocode_function_count != 1:
    raise SystemExit(
        "ERROR: Expected one geocodeSite function start, "
        f"found {geocode_function_count}."
    )

text = text.replace(
    old_geocode_start,
    new_geocode_start,
    1,
)


# ---------------------------------------------------------
# 5. Validate that all external map dependencies are gone
# ---------------------------------------------------------

for forbidden_value in (
    "tile.openstreetmap.org",
    "server.arcgisonline.com",
    "nominatim.openstreetmap.org",
):
    if forbidden_value in text:
        raise SystemExit(
            "ERROR: External dependency remains "
            f"after patch: {forbidden_value}"
        )


required_after_patch = (
    new_street_url,
    "'Offline Street': streets",
    "var GEOCODE_URL = null;",
    (
        "Adres arama offline harita "
        "kurulumunda devre disidir."
    ),
)

for required_value in required_after_patch:
    if required_value not in text:
        raise SystemExit(
            "ERROR: Expected patched content is missing: "
            f"{required_value}"
        )


if text == original:
    raise SystemExit(
        "ERROR: Patch made no changes."
    )


# ---------------------------------------------------------
# 6. Create a source backup and write the patched file
# ---------------------------------------------------------

backup_path = site_map_js.with_suffix(
    site_map_js.suffix
    + ".before-offline-map"
)

if not backup_path.exists():
    backup_path.write_text(
        original,
        encoding="utf-8",
    )

site_map_js.write_text(
    text,
    encoding="utf-8",
)


print(
    f"Patched file: {site_map_js}"
)

print(
    f"Backup file: {backup_path}"
)

print(
    f"Offline tile URL: {new_street_url}"
)

print(
    "Satellite layer: disabled"
)

print(
    "Online Nominatim geocoding: disabled"
)
