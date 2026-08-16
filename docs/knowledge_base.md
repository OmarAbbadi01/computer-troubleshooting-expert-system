# Knowledge Base

The knowledge base is stored as JSON in `data/knowledge_base.json` and
contains the domain knowledge used by the system. It is completely separate
from the inference engine; the engine only knows how to reason over the rules
it is given.

## Sources of troubleshooting knowledge

The rules are based on commonly documented troubleshooting steps for
consumer computers:

- PC repair / troubleshooting guides describing power, display and boot
  symptom-to-cause mappings (e.g., "no power LED + no fans -> check power
  delivery and the power supply").
- Operating-system support documentation for startup repair, Safe Mode, and
  network troubleshooting (e.g., "can reach the router but not the internet ->
  connectivity issue outside the local network").
- Basic hardware documentation for RAM/disk health checks (Task Manager,
  disk-check tools) and peripheral troubleshooting (try another port, try
  another computer, check the driver).

These sources provide heuristic, broad "symptom -> probable cause" knowledge
suitable for an academic expert system.

## Fact categories

| Category | Example facts |
|----------|---------------|
| Power | `power_led_on`, `fans_not_running`, `power_cable_loose`, `outlet_power_fails` |
| Display | `screen_blank`, `post_screen_blank`, `external_monitor_works` |
| Boot / OS | `os_loading_screen_visible`, `bsod_occurs`, `post_screen_visible` |
| Performance | `os_loads_slowly`, `programs_launch_slowly`, `many_startup_programs` |
| Overheating | `computer_hot`, `shuts_down_unexpectedly`, `vents_blocked`, `fan_unusually_noisy` |
| Network | `wifi_connected`, `router_reachable`, `internet_unreachable`, `ip_address_missing` |
| Storage | `disk_nearly_full`, `disk_activity_high`, `disk_errors_reported` |
| Memory | `ram_usage_high`, `system_freezes`, `ram_sticks_missing` |
| Peripheral | `device_not_detected`, `device_fails_any_port`, `driver_issue` |

The vocabulary is kept consistent (one name per concept) to avoid duplicate
or conflicting facts.

## Intermediate facts

A limited number of facts are inferred in-between input and diagnosis to
demonstrate real chaining:

- `power_delivery_issue`, `internal_power_fault`
- `display_path_fault`, `backlight_or_panel_fault`
- `os_boot_reached`, `os_boot_failed`
- `system_slow_indicators`, `startup_overload`
- `cooling_problem`
- `local_connectivity_only`
- `storage_pressure`, `memory_pressure`

## Final diagnoses

| Fact | Display name |
|------|--------------|
| `diagnosis_power` | Power problem |
| `diagnosis_display` | Display problem |
| `diagnosis_boot` | Boot / operating-system problem |
| `diagnosis_performance` | Performance problem |
| `diagnosis_overheating` | Overheating problem |
| `diagnosis_network` | Network problem |
| `diagnosis_storage` | Storage problem |
| `diagnosis_memory` | Memory problem |
| `diagnosis_peripheral` | Peripheral/device problem |

## Rules (34 IF-THEN rules)

| ID | Conditions | Conclusion | Type |
|----|-----------|-----------|------|
| P1 | power_cable_loose | power_delivery_issue | intermediate |
| P2 | outlet_power_fails | power_delivery_issue | intermediate |
| P3 | power_delivery_issue + power_led_off | diagnosis_power | diagnosis |
| P4 | power_led_off + fans_not_running + power_cable_ok + outlet_power_ok | internal_power_fault | intermediate |
| P5 | internal_power_fault | diagnosis_power | diagnosis |
| D1 | computer_running + screen_blank + post_screen_blank | display_path_fault | intermediate |
| D2 | display_path_fault | diagnosis_display | diagnosis |
| D3 | external_monitor_works + screen_blank | backlight_or_panel_fault | intermediate |
| D4 | backlight_or_panel_fault | diagnosis_display | diagnosis |
| B1 | os_loading_screen_visible | os_boot_reached | intermediate |
| B2 | os_boot_reached + bsod_occurs | diagnosis_boot | diagnosis |
| B3 | post_screen_visible + os_loading_screen_absent | os_boot_failed | intermediate |
| B4 | os_boot_failed | diagnosis_boot | diagnosis |
| PERF1 | os_loads_slowly + programs_launch_slowly | system_slow_indicators | intermediate |
| PERF2 | system_slow_indicators + disk_nearly_full | diagnosis_performance | diagnosis |
| PERF3 | system_slow_indicators + many_startup_programs | startup_overload | intermediate |
| PERF4 | startup_overload | diagnosis_performance | diagnosis |
| O1 | computer_running + computer_hot + fans_not_running | cooling_problem | intermediate |
| O2 | computer_hot + vents_blocked | cooling_problem | intermediate |
| O3 | cooling_problem + shuts_down_unexpectedly | diagnosis_overheating | diagnosis |
| O4 | computer_hot + fan_unusually_noisy + shuts_down_unexpectedly | diagnosis_overheating | diagnosis |
| NET1 | wifi_connected + router_reachable + internet_unreachable | local_connectivity_only | intermediate |
| NET2 | local_connectivity_only | diagnosis_network | diagnosis |
| NET3 | wifi_no_networks + other_devices_offline | diagnosis_network | diagnosis |
| NET4 | ip_address_missing + router_reachable + wifi_connected | diagnosis_network | diagnosis |
| S1 | disk_nearly_full + disk_activity_high | storage_pressure | intermediate |
| S2 | storage_pressure | diagnosis_storage | diagnosis |
| S3 | disk_errors_reported + files_missing_corrupt | diagnosis_storage | diagnosis |
| M1 | ram_usage_high + system_freezes | memory_pressure | intermediate |
| M2 | memory_pressure | diagnosis_memory | diagnosis |
| M3 | ram_sticks_missing + frequent_app_crashes | diagnosis_memory | diagnosis |
| PE1 | device_not_detected + device_fails_any_port + device_fails_other_computer | diagnosis_peripheral | diagnosis |
| PE2 | device_not_detected + device_works_in_another_port | diagnosis_peripheral | diagnosis |
| PE3 | device_detected + driver_issue | diagnosis_peripheral | diagnosis |

## Rule organization

- **Distribution:** roughly 4–5 rules per problem area, for 34 rules total.
- **Chaining:** about half of the rules infer intermediate facts; the rest
  turn intermediate (or direct) evidence into final diagnoses. Several
  diagnoses require two inference steps (e.g., Power, Display, Overheating)
  and one requires three steps (startup overload).
- **Firing order:** rules fire in deterministic rule-ID order; no priorities
  are used — the order only affects which intermediate facts appear first in
  the explanation, not which conclusions are reached.
- **Multiple conclusions:** rules are not contradictory; different rules may
  reach the same diagnosis from different evidence, and several independent
  chains may fire in one session (producing multiple diagnoses).
