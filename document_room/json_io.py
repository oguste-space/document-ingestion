"""JSON boundary: named object members on input, dataclass entities on output."""
import json
from dataclasses import dataclass, fields, is_dataclass
from datetime import date
from decimal import Decimal
from enum import Enum


@dataclass(frozen=True)
class JsonMember:
    name: str
    value: object


@dataclass(frozen=True)
class JsonObject:
    members: tuple[JsonMember, ...]

    @classmethod
    def from_pairs(cls, pairs: list[tuple[str, object]]) -> "JsonObject":
        names = [name for name, _ in pairs]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate JSON object member")
        return cls(tuple(JsonMember(name, value) for name, value in pairs))

    def get(self, name: str) -> object:
        for member in self.members:
            if member.name == name:
                return member.value
        raise ValueError(f"Missing JSON member: {name}")

    def string(self, name: str) -> str:
        value = self.get(name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Expected non-empty string: {name}")
        return value

    def objects(self, name: str) -> tuple["JsonObject", ...]:
        value = self.get(name)
        if not isinstance(value, list):
            raise ValueError(f"Expected array: {name}")
        result: list[JsonObject] = []
        for item in value:
            if not isinstance(item, JsonObject):
                raise ValueError(f"Expected object in: {name}")
            result.append(item)
        return tuple(result)

    def child(self, name: str) -> "JsonObject":
        value = self.get(name)
        if not isinstance(value, JsonObject):
            raise ValueError(f"Expected object: {name}")
        return value


def load_json(text: str) -> JsonObject:
    result: object = json.loads(text, object_pairs_hook=JsonObject.from_pairs)
    if not isinstance(result, JsonObject):
        raise ValueError("Expected a JSON object")
    return result


def dump_json(value: object, *, indent: int | None = None) -> str:
    """Serialize entities, optionally with indentation, without untyped mappings."""
    if indent is not None and indent < 0:
        raise ValueError("Indent must be non-negative")

    def container(opening: str, closing: str, items: list[str], depth: int) -> str:
        if not items:
            return opening + closing
        if indent is None:
            return opening + ", ".join(items) + closing
        padding = " " * (indent * (depth + 1))
        return opening + "\n" + padding + (",\n" + padding).join(items) + "\n" + " " * (indent * depth) + closing

    def encode(item: object, depth: int) -> str:
        if isinstance(item, Enum):
            return encode(item.value, depth)
        if isinstance(item, date):
            return json.dumps(item.isoformat())
        if isinstance(item, Decimal):
            if not item.is_finite():
                raise ValueError("Non-finite decimal cannot be serialized")
            return json.dumps(format(item, "f"))
        if is_dataclass(item) and not isinstance(item, type):
            members = [json.dumps(member.name) + ": " + encode(getattr(item, member.name), depth + 1) for member in fields(item)]
            return container("{", "}", members, depth)
        if isinstance(item, (tuple, list)):
            return container("[", "]", [encode(child, depth + 1) for child in item], depth)
        if item is None or isinstance(item, (str, bool, int, float)):
            return json.dumps(item, ensure_ascii=False, allow_nan=False)
        raise TypeError(f"Unsupported JSON value: {type(item).__name__}")

    return encode(value, 0)
