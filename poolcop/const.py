"""Constants for PoolCopilot API client."""
from importlib import metadata
from typing import Final

API_HOST: Final = "poolcopilot.com"
USER_AGENT: Final = f"python-poolcop/{metadata.version(__package__)}"

# --- Aux label IDs (from PoolCopilot API) ---

# User-assignable labels (0-15) — can go on any aux port
AUX_LABEL_POOL_LIGHT: Final = 0
AUX_LABEL_POOL_CLEANER: Final = 1
AUX_LABEL_POOL_HEATING: Final = 2
AUX_LABEL_DISINFECTION: Final = 3
AUX_LABEL_ELECTROLYSIS: Final = 4
AUX_LABEL_REMNANT: Final = 5
AUX_LABEL_TRANSFER_PUMP: Final = 6
AUX_LABEL_UV: Final = 7
AUX_LABEL_SPA: Final = 8
AUX_LABEL_FOUNTAIN: Final = 9
AUX_LABEL_BOREHOLE: Final = 10
AUX_LABEL_POOL_HOUSE: Final = 11
AUX_LABEL_GARDEN_1: Final = 12
AUX_LABEL_GARDEN_2: Final = 13
AUX_LABEL_GARDEN_3: Final = 14
AUX_LABEL_AVAILABLE: Final = 15

# Fixed-function labels (16-27) — assigned by hardware config
AUX_LABEL_WASTE_VALVE: Final = 16       # Fixed to aux 5
AUX_LABEL_SPEED_CONTROL: Final = 17     # Fixed to aux 1-3
AUX_LABEL_ORP_CONTROL: Final = 18       # Fixed to aux 6
AUX_LABEL_REMNANT_FIXED: Final = 19
AUX_LABEL_POOL_COVER: Final = 20        # XM8: aux 13-15
AUX_LABEL_JET_STREAM: Final = 21        # XM8: aux 13-15
AUX_LABEL_EXTERNAL_WARNINGS: Final = 22
AUX_LABEL_CLEANING_VALVE: Final = 23
AUX_LABEL_RINSING_VALVE: Final = 24
AUX_LABEL_DOSING_APF: Final = 25
AUX_LABEL_DOSING_ACO: Final = 26
AUX_LABEL_SUCTION_VALVE: Final = 27

# Display name mapping
AUX_LABEL_NAMES: Final[dict[int, str]] = {
    0: "Pool Light",
    1: "Pool Cleaner",
    2: "Pool Heating",
    3: "Disinfection",
    4: "Electrolysis",
    5: "Remnant",
    6: "Transfer Pump",
    7: "UV",
    8: "Spa",
    9: "Fountain",
    10: "Borehole",
    11: "Pool House",
    12: "Garden 1",
    13: "Garden 2",
    14: "Garden 3",
    15: "Available",
    16: "Waste Valve",
    17: "Speed Control",
    18: "ORP Control",
    19: "Remnant",
    20: "Pool Cover",
    21: "Jet Stream",
    22: "External Warnings",
    23: "Cleaning Valve",
    24: "Rinsing Valve",
    25: "Dosing APF",
    26: "Dosing ACO",
    27: "Suction Valve",
}

# --- Port constraints ---
AUX_MAX_CCU: Final = 7    # Standard CCU: aux 1-7
AUX_MAX_XM8: Final = 15   # With XM8 expansion: aux 8-15

# --- Binary input function IDs ---
# CCU: Input 1-2, XM8: Input 3-10

INPUT_FUNC_AVAILABLE: Final = 0
INPUT_FUNC_ANTI_FREEZE: Final = 1
INPUT_FUNC_CONSUMABLES_DISINFECTION: Final = 2
INPUT_FUNC_CONSUMABLES_PH: Final = 3
INPUT_FUNC_CONSUMABLES_LOW: Final = 4
INPUT_FUNC_POOL_COVER: Final = 5
INPUT_FUNC_ELECTROLYSER_DIAG: Final = 6
INPUT_FUNC_EXTERNAL_PUMP_START: Final = 7
INPUT_FUNC_EXTERNAL_PUMP_STOP: Final = 8
INPUT_FUNC_JET_STREAM_BUTTON: Final = 9
INPUT_FUNC_FLOW_SWITCH: Final = 10
INPUT_FUNC_FLOODING: Final = 11
INPUT_FUNC_FLOODING_STOP: Final = 12
INPUT_FUNC_CL_SENSOR_FLOW: Final = 13
INPUT_FUNC_ACO_CONSUMABLES: Final = 14
INPUT_FUNC_APF_CONSUMABLES: Final = 15
INPUT_FUNC_OVERFLOW: Final = 16
INPUT_FUNC_OPEN_COVER: Final = 17
INPUT_FUNC_CLOSE_COVER: Final = 18
INPUT_FUNC_ELECTROLYSER_FLOW_SWITCH: Final = 19
INPUT_FUNC_AUX_CONTROL: Final = 20

INPUT_FUNC_NAMES: Final[dict[int, str]] = {
    0: "Available",
    1: "Anti-Freeze Detection",
    2: "Consumables Disinfection Low Level",
    3: "Consumables pH Low Level",
    4: "Consumables Low Level",
    5: "Pool Cover",
    6: "Electrolyser Diagnostic",
    7: "External Pump Start",
    8: "External Pump Stop",
    9: "Jet Stream Push Button",
    10: "Flow Switch",
    11: "Flooding",
    12: "Flooding Stop Filtration",
    13: "CL Sensor Flow",
    14: "ACO Consumables",
    15: "APF Consumables",
    16: "Overflow",
    17: "Open Cover",
    18: "Close Cover",
    19: "Electrolyser Protection Flow Switch",
    20: "Aux Control",
}
