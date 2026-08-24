PLUGINS = ["nbxsync",
           "netbox_ipcalculator",
           "netbox_topology_views",
           "netbox_documents",
           "netbox_data_flows",
           "netbox_acls",
           "netbox_lifecycle",
           "netbox_inventory"]

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
    },
    "netbox_ipcalculator": {},
    "netbox_topology_views": {
        'static_image_directory': 'netbox_topology_views/img',
        'allow_coordinates_saving': True,
        'always_save_coordinates': True
    },
    "netbox_documents": {

        # Enable the global navigation menu
        'enable_navigation_menu': True,

        # Location of the documents panel on object detail pages (left/right)
        'documents_location': 'left',

        # Custom document types (see below)
        'custom_doc_types': [],

        # Per-model document type filtering (see below)
        'allowed_doc_types': {},
    },
    "netbox_data_flows": {
        # Create a menu section for the plugin
        'top_level_menu': True,
        # Use a Custom Field to identify objects linked to an application
        'application_custom_field': "application",
    },
    "netbox_acls": {
        # Set to True to add a top-level menu item, or False to place it
        # under the Plugins menu. Default is True.
        "top_level_menu": True,
        # Sequence number increment for new ACL rules (e.g., 10, 20, 30...)
        "rule_sequence_step": 10,
    },
    "netbox_lifecycle": {
        'lifecycle_card_position': 'right_page',
        'contract_card_position': 'right_page',
    },
    "netbox_inventory": {
        # Example settings below, see "Available settings"
        # in README.md for all possible settings
        "used_status_name": "used",
        "stored_status_name": "stored",
        "sync_hardware_serial_asset_tag": True,
    }
}
