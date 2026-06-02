import json
import sys

def infer_type(value):
    if isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "number"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, list):
        return "array"
    elif isinstance(value, dict):
        return "object"
    elif value is None:
        return "null"
    return "string"

def merge_schemas(s1, s2):
    if s1 is None:
        return s2
    if s2 is None:
        return s1
    t1, t2 = s1.get("type"), s2.get("type")
    # Allow integer/number merge to number
    if t1 != t2:
        if {t1, t2} == {"integer", "number"}:
            merged = {"type": "number"}
            mins = [s for s in (s1, s2) if "minimum" in s]
            maxs = [s for s in (s1, s2) if "maximum" in s]
            if mins:
                merged["minimum"] = min(s["minimum"] for s in mins)
            if maxs:
                merged["maximum"] = max(s["maximum"] for s in maxs)
            return merged
        return s1
    
    merged = {"type": t1}
    if t1 in ("integer", "number"):
        if "minimum" in s1 or "minimum" in s2:
            merged["minimum"] = min(s.get("minimum", float('inf')) for s in (s1, s2) if "minimum" in s)
        if "maximum" in s1 or "maximum" in s2:
            merged["maximum"] = max(s.get("maximum", float('-inf')) for s in (s1, s2) if "maximum" in s)
    elif t1 == "object":
        p1 = s1.get("properties", {})
        p2 = s2.get("properties", {})
        merged_props = {}
        for k in set(p1) | set(p2):
            if k in p1 and k in p2:
                merged_props[k] = merge_schemas(p1[k], p2[k])
            elif k in p1:
                merged_props[k] = p1[k]
            else:
                merged_props[k] = p2[k]
        req = set(s1.get("required", [])) & set(s2.get("required", []))
        merged["required"] = sorted(req)
        merged["properties"] = merged_props
    return merged

def infer_schema_from_value(value):
    t = infer_type(value)
    schema = {"type": t}
    if t in ("integer", "number"):
        schema["minimum"] = value
        schema["maximum"] = value
    elif t == "object":
        props = {}
        for k, v in value.items():
            props[k] = infer_schema_from_value(v)
        schema["required"] = sorted(value.keys())
        schema["properties"] = props
    return schema

def format_leaf(schema):
    """Format a leaf (non-object) schema on one line."""
    parts = []
    # Preserve key order: type, then minimum, maximum, then others
    keys_order = ["type", "minimum", "maximum", "items"]
    seen = set()
    for k in keys_order:
        if k in schema:
            parts.append(f'"{k}": {json.dumps(schema[k])}')
            seen.add(k)
    for k in schema:
        if k not in seen:
            parts.append(f'"{k}": {json.dumps(schema[k])}')
    return "{" + ", ".join(parts) + "}"

def format_schema(schema, indent=0):
    """Format the top-level object schema with custom layout."""
    if schema.get("type") != "object":
        return format_leaf(schema)
    
    pad = "  " * indent
    inner_pad = "  " * (indent + 1)
    lines = ["{"]
    lines.append(f'{inner_pad}"type": "object",')
    req = schema.get("required", [])
    req_str = "[" + ", ".join(json.dumps(r) for r in req) + "]"
    lines.append(f'{inner_pad}"required": {req_str},')
    props = schema.get("properties", {})
    lines.append(f'{inner_pad}"properties": {{')
    prop_pad = "  " * (indent + 2)
    prop_items = list(props.items())
    for i, (k, v) in enumerate(prop_items):
        comma = "," if i < len(prop_items) - 1 else ""
        if v.get("type") == "object":
            nested = format_schema(v, indent + 2)
            lines.append(f'{prop_pad}"{k}": {nested}{comma}')
        else:
            lines.append(f'{prop_pad}"{k}": {format_leaf(v)}{comma}')
    lines.append(f'{inner_pad}}}')
    lines.append(f'{pad}}}')
    return "\n".join(lines)

def main():
    objects = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            try:
                objects.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    if not objects:
        return
    merged = None
    for obj in objects:
        merged = merge_schemas(merged, infer_schema_from_value(obj))
    print(format_schema(merged))

if __name__ == "__main__":
    main()