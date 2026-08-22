PLUGINS = ["nbxsync"]

PLUGINS_CONFIG = {
    "nbxsync": {
        "sot": {
            "proxygroup": "netbox",
            "proxy": "netbox",
            "macro": "netbox",
            "host": "netbox",
            "hostmacro": "netbox",
            "hostgroup": "netbox",
            "hostinterface": "netbox",
            "hosttemplate": "netbox",
            "maintenance": "netbox",
        },

        "statusmapping": {
            "device": {
                "active": "enabled",
                "planned": "disabled",
                "failed": "disabled",
                "staged": "disabled",
                "offline": "disabled",
                "inventory": "disabled",
                "decommissioning": "disabled",
            },

            "virtualmachine": {
                "active": "enabled",
                "planned": "enabled_in_maintenance",
                "paused": "enabled_no_alerting",
                "offline": "disabled",
                "failed": "disabled",
            },
        },

        "snmpconfig": {
            "snmp_community": "{$SNMP_COMMUNITY}",
            "snmp_authpass": "{$SNMP_AUTHPASS}",
            "snmp_privpass": "{$SNMP_PRIVPASS}",
        },

        "inheritance_chain": [
            ["device"],
            ["role"],
            ["device", "role"],
            ["role", "parent"],
            ["device", "role", "parent"],
            ["device", "device_type"],
            ["device_type"],
            ["device", "platform"],
            ["platform"],
            ["device", "device_type", "manufacturer"],
            ["device_type", "manufacturer"],
            ["device", "manufacturer"],
            ["manufacturer"],
            ["cluster"],
            ["cluster", "type"],
            ["type"],
        ],

        "backgroundsync": {
            "objects": {
                "enabled": False,
                "interval": 60,
            },
            "templates": {
                "enabled": False,
                "interval": 1440,
            },
            "proxies": {
                "enabled": False,
                "interval": 1440,
            },
            "maintenance": {
                "enabled": False,
                "interval": 15,
            },
        },

        "no_alerting_tag": "NO_ALERTING",
        "no_alerting_tag_value": "1",
        "maintenance_window_duration": 3600,

        "attach_objtag": True,
        "objtag_type": "nb_type",
        "objtag_id": "nb_id",

        "custom_field_hostname": "",
        "custom_field_display_name": "",
    }
}
