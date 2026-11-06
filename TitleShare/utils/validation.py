from jsonschema import validate, Draft202012Validator



# ---------------------------
# JSON Schema for PresetModel
# ---------------------------
vector3_schema = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "X": {"type": "number"},
        "Y": {"type": "number"},
        "Z": {"type": "number"}
    },
    "required": ["X", "Y", "Z"]
}
vector4_schema =  {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "X": {"type": "number"},
        "Y": {"type": "number"},
        "Z": {"type": "number"},
        "W": {"type": "number"}
    },
    "required": ["X", "Y", "Z", "W"]
}
preset_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "PresetModel",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "Version": {"type": "integer", "enum": [6]},
        "Name": {"type": "string", "maxLength": 256},
        "Author": {"type": "string", "maxLength": 256},
        "CameraFollowMode": {"type": "integer", "enum": [0, 1, 2]},
        "LastLocationMount": {"type": "boolean"},
        "LocationModel": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "Version": {"type": "integer", "enum": [6]},
                "LocationType": {"type": "integer", "enum": [0, 1]},
                "TitleScreenLogo": {"type": "integer", "enum": [0, 1, 2, 3, 4, 5, 6, 7, 8]},
                "TerritoryPath": {"type": "string", "maxLength": 1024},
                "TerritoryTypeId": {"type": "integer"},
                "LayoutTerritoryTypeId": {"type": "integer"},
                "LayoutLayerFilterKey": {"type": "integer"},
                "Position": vector3_schema,
                "CameraPosition": vector3_schema,
                "Rotation": {"type": "number"},
                "Yaw": {"type": "number"},
                "Roll": {"type": "number"},
                "Pitch": {"type": "number"},
                "Fov": {"type": "number"},
                "WeatherId": {"type": "integer"},
                "TimeOffset": {"type": "integer"},
                "BgmId": {"type": "integer"},
                "BgmPath": {"type": ["string", "null"], "maxLength": 1024},
                "MovementMode": {"type": "integer", "enum": [0, 1, 2]},
                "Mount": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "LastLocationMount": { "type": "boolean" },
                        "MountId": { "type": "integer" },
                        "BuddyModelTop": { "type": "integer" },
                        "BuddyModelBody": { "type": "integer" },
                        "BuddyModelLegs": { "type": "integer" },
                        "BuddyStain": { "type": "integer" }
                    },
                    "required": [
                        "LastLocationMount",
                        "MountId",
                        "BuddyModelTop",
                        "BuddyModelBody",
                        "BuddyModelLegs",
                        "BuddyStain"
                    ]
                },
                "Active": {
                    "type": "array",
                    "items": {"type": "integer"}
                },
                "Inactive": {
                    "type": "array",
                    "items": {"type": "integer"}
                },
                "VfxTriggerIndexes": {
                    "type": "object",
                    "patternProperties": {
                        r"^\d+$": {"type": "integer"}
                    }
                },
                "Festivals": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "Id": { "type": "integer" },
                            "Phase": { "type": "integer" },
                        },
                        "required": ["Id", "Phase"]
                    },
                    "minItems": 8,
                    "maxItems": 8
                },
                "SaveLayout": {"type": "boolean"},
                "UseVfx": {"type": "boolean"},
                "SaveHousing": {"type": "boolean"},
                "SaveFestivals": {"type": "boolean"},
                "TitleScreenOverride": {"type": ["integer", "null"], "enum": [None, 0, 1, 2, 3, 4, 5]},
                "UiColor": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "Expansion": {"type": "integer", "enum": [-2, -1, 0, 1, 2, 3, 4, 5]},
                        "Color": vector4_schema,
                        "EdgeColor": vector4_schema,
                        "HighlightColor": vector4_schema
                    },
                    "required": ["Expansion", "Color", "EdgeColor", "HighlightColor"]
                },
                "TitleScreenMovie": {"type": "integer", "enum": [-1, 1, 4, 5, 6, 7, 8]},
                "UseLiveTime": {"type": "boolean"},

                # Complex optional lists/objects
                "Furniture": {
                    "type": ["array", "null"],
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "Id": { "type": "integer" },
                            "Stain": { "type": "integer" },
                            "Position": vector3_schema,
                            "Rotation": { "type": "number" },
                            "HousingObjectData": {
                                "type": ["null", "object"],
                                "additionalProperties": False,
                                "properties": {
                                    #Value1 is 8 ushorts and Value2-4 are 8 bytes encoded as Base64 
                                    "Value1": {
                                        "type": "array", 
                                        "items": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 65535
                                        },  
                                        "minItems": 8,
                                        "maxItems": 8
                                    },
                                    "Value2": { 
                                        "type": "string", 
                                        "minLength": 12,
                                        "maxLength": 12,
                                        "pattern": "^[A-Za-z0-9+/]{11}=$"
                                    },
                                    "Value3": {
                                        "type": "string", 
                                        "minLength": 12,
                                        "maxLength": 12,
                                        "pattern": "^[A-Za-z0-9+/]{11}=$"
                                    },
                                    "Value4": {
                                        "type": "string", 
                                        "minLength": 12,
                                        "maxLength": 12,
                                        "pattern": "^[A-Za-z0-9+/]{11}=$"
                                    },
                                },
                                "required": ["Value1", "Value2", "Value3", "Value4"]
                            }
                        },
                        "required": ["Id", "Stain", "Position", "Rotation"]
                    }
                },
                "Plots": {
                    "type": ["array", "null"],
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "Plot": { "type": "integer" },
                            "Fixtures": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "additionalProperties": False,
                                    "properties": {
                                        "FixtureId": { "type": "integer" },
                                        "StainId": { "type": "integer" },
                                    },
                                    "required": ["FixtureId", "StainId"]
                                }
                            }
                        },
                        "required": ["Plot", "Fixtures"]
                    }
                },
                "Estate": {
                    "type": ["object", "null"],
                    "additionalProperties": False,
                    "properties": {
                        "LightLevel": { "type": "number" },
                        "Floors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "Part0": { "type": "integer" },
                                    "Part1": { "type": "integer" },
                                    "Part2": { "type": "integer" },
                                    "Part3": { "type": "integer" },
                                    "Part4": { "type": "integer" }
                                },
                                "required": ["Part0", "Part1", "Part2", "Part3", "Part4"]
                            }
                        },
                    },
                    "required": ["LightLevel", "Floors"]
                },
            },
            "required": [
                "Version", "LocationType", "TitleScreenLogo",
                "TerritoryPath", "TerritoryTypeId",
                "LayoutTerritoryTypeId", "LayoutLayerFilterKey",
                "Position", "CameraPosition", "Rotation", "Yaw",
                "Roll", "Pitch", "Fov", "WeatherId", "TimeOffset",
                "BgmId", "MovementMode", "Active", "Inactive",
                "VfxTriggerIndexes", "Festivals", "SaveLayout",
                "UseVfx", "SaveHousing", "SaveFestivals",
                "UiColor", "TitleScreenMovie", "UseLiveTime"
            ]
        },
    },
    "required": ["Version", "Name", "Author", "CameraFollowMode", "LocationModel"]
}

def validate_preset(preset_json: dict) -> bool:
    
    validator = Draft202012Validator(preset_schema)
    errors = sorted(validator.iter_errors(preset_json), key=lambda e: e.path)

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f" - {list(err.path)}: {err.message}")
        return False
    return True