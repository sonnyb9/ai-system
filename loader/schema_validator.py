import json
import os

class SchemaValidator:
    def __init__(self, schema_dir):
        self.schema_dir = schema_dir

    def load_schema(self, filepath):
        with open(filepath, "r") as f:
            return json.load(f)

    def validate(self, schema):
        errors = []

        metadata = schema.get("schema_metadata")
        data = schema.get("data")

        if not metadata:
            errors.append("Missing schema_metadata")
            return errors

        validation_rules = metadata.get("validation", {})
        required_top = validation_rules.get("required_top_level_keys", [])
        required_fields = validation_rules.get("required_fields_by_object", {})

        # Check top-level keys
        for key in required_top:
            if key not in data:
                errors.append(f"Missing top-level key: {key}")

        # Check object fields
        for obj_name, fields in required_fields.items():
            objects = data.get(obj_name, [])

            if not isinstance(objects, list):
                errors.append(f"{obj_name} should be a list")
                continue

            for i, obj in enumerate(objects):
                for field in fields:
                    if field not in obj:
                        errors.append(f"{obj_name}[{i}] missing field: {field}")

        return errors

    def validate_all(self):
        results = {}

        for file in os.listdir(self.schema_dir):
            if file.endswith(".json"):
                path = os.path.join(self.schema_dir, file)
                schema = self.load_schema(path)
                errors = self.validate(schema)

                results[file] = {
                    "valid": len(errors) == 0,
                    "errors": errors
                }

        return results


if __name__ == "__main__":
    from config import SCHEMAS_DIR
    validator = SchemaValidator(str(SCHEMAS_DIR))
    results = validator.validate_all()

    for file, result in results.items():
        print(f"{file}: {'VALID' if result['valid'] else 'INVALID'}")
        for err in result["errors"]:
            print(f"  - {err}")