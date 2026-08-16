"""The ten (plus one) evaluation scenarios.

These cases exist ONLY for evaluation. They are run through the real
questionnaire and the real inference engine; the application itself
never references them and contains no test-case-specific logic.

Each case records the machine type, the selected main problem, the
Yes/No answers, and the expected diagnosis.
"""

CASES = [
    {
        "number": 1,
        "name": "Power",
        "machine": "desktop",
        "problem": "power_off",
        "answers": {
            "q_power_led": False,
            "q_fans": False,
            "q_power_cable": True,
            "q_outlet": True,
        },
        "expected": ["Power problem"],
        "notes": "Two-step chain: facts -> internal_power_fault -> Power problem.",
    },
    {
        "number": 2,
        "name": "Display",
        "machine": "desktop",
        "problem": "blank_screen",
        "answers": {
            "q_computer_running": True,
            "q_screen_blank": True,
            "q_post_screen": False,
            "q_external_monitor": None,  # desktop: not asked
        },
        "expected": ["Display problem"],
        "notes": "Two-step chain: facts -> display_path_fault -> Display problem.",
    },
    {
        "number": 3,
        "name": "Boot / OS",
        "machine": "desktop",
        "problem": "boot_problem",
        "answers": {
            "q_computer_running": True,
            "q_post_screen": True,
            "q_os_loading_screen": True,
            "q_bsod": True,
        },
        "expected": ["Boot / operating-system problem"],
        "notes": "Two-step chain: facts -> os_boot_reached -> Boot/OS problem.",
    },
    {
        "number": 4,
        "name": "Network",
        "machine": "desktop",
        "problem": "network",
        "answers": {
            "q_wifi_connected": True,
            "q_networks_visible": True,
            "q_router_reachable": True,
            "q_internet": False,
            "q_other_devices": False,
            "q_ip_address": True,
        },
        "expected": ["Network problem"],
        "notes": "Two-step chain: facts -> local_connectivity_only -> Network problem.",
    },
    {
        "number": 5,
        "name": "Overheating",
        "machine": "desktop",
        "problem": "overheating",
        "answers": {
            "q_computer_running": True,
            "q_computer_hot": True,
            "q_shutdown": True,
            "q_fans": False,
            "q_vent_blocked": False,
            "q_fan_noise": False,
        },
        "expected": ["Overheating problem"],
        "notes": "Two-step chain: facts -> cooling_problem -> Overheating problem.",
    },
    {
        "number": 6,
        "name": "Performance",
        "machine": "desktop",
        "problem": "slow",
        "answers": {
            "q_os_load_time": True,
            "q_program_launch": True,
            "q_disk_nearly_full": False,
            "q_disk_activity": False,
            "q_startup_programs": True,
        },
        "expected": ["Performance problem"],
        "notes": "Three-step chain: facts -> system_slow_indicators -> startup_overload -> Performance problem.",
    },
    {
        "number": 7,
        "name": "Storage",
        "machine": "desktop",
        "problem": "storage",
        "answers": {
            "q_disk_nearly_full": True,
            "q_disk_activity": True,
            "q_disk_errors": False,
            "q_files_corrupt": False,
        },
        "expected": ["Storage problem"],
        "notes": "Two-step chain: facts -> storage_pressure -> Storage problem.",
    },
    {
        "number": 8,
        "name": "Memory",
        "machine": "desktop",
        "problem": "memory",
        "answers": {
            "q_ram_usage": True,
            "q_freezes": True,
            "q_app_crashes": False,
            "q_ram_detected": True,
        },
        "expected": ["Memory problem"],
        "notes": "Two-step chain: facts -> memory_pressure -> Memory problem.",
    },
    {
        "number": 9,
        "name": "Peripheral",
        "machine": "desktop",
        "problem": "peripheral",
        "answers": {
            "q_device_detected": False,
            "q_device_other_port": False,
            "q_device_other_computer": False,
            "q_driver": False,
        },
        "expected": ["Peripheral/device problem"],
        "notes": "Single-step rule (device itself faulty).",
    },
    {
        "number": 10,
        "name": "Multiple diagnoses",
        "machine": "desktop",
        "problem": "slow",
        "answers": {
            "q_os_load_time": True,
            "q_program_launch": True,
            "q_disk_nearly_full": True,
            "q_disk_activity": True,
            "q_startup_programs": False,
        },
        "expected": ["Performance problem", "Storage problem"],
        "notes": "Slow computer with a full, constantly active disk: two independent chains fire.",
    },
    {
        "number": 11,
        "name": "Insufficient evidence",
        "machine": "desktop",
        "problem": "overheating",
        "answers": {
            "q_computer_running": True,
            "q_computer_hot": True,
            "q_shutdown": False,
            "q_fans": False,
            "q_vent_blocked": False,
            "q_fan_noise": False,
        },
        "expected": [],
        "notes": "Cooling problem is inferred but no unexpected shutdown, so no final diagnosis.",
    },
]
