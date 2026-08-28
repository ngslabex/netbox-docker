#!/bin/sh

set -eu

FILE="$(
    find /opt/netbox/netbox/static \
        -type f \
        -path "*/netbox_map/js/site_map.js" \
        -print \
        | head -n 1
)"

if [ -z "${FILE}" ]; then
    echo "ERROR: Collected site_map.js was not found."
    exit 1
fi

echo "Collected static file:"
echo "${FILE}"
echo

required_values="
maps.scada.local/styles/basic-preview/256/
Offline Street
GEOCODE_URL = null
Adres arama offline harita
"

echo "${required_values}" |
while IFS= read -r value
do
    if [ -z "${value}" ]; then
        continue
    fi

    if grep -Fq "${value}" "${FILE}"; then
        echo "FOUND: ${value}"
    else
        echo "ERROR: Required value is missing: ${value}"
        exit 1
    fi
done

for forbidden in \
    "tile.openstreetmap.org" \
    "server.arcgisonline.com" \
    "nominatim.openstreetmap.org"
do
    if grep -Fq "${forbidden}" "${FILE}"; then
        echo "ERROR: External dependency remains: ${forbidden}"
        exit 1
    else
        echo "ABSENT: ${forbidden}"
    fi
done

echo
echo "OK: Collected static file is configured for offline maps."
