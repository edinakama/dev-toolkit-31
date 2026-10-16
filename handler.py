from typing import Any, Callable, Generator, List, Dict


class Constraint:
    def __init__(self, check: Callable[[Any], bool], msg: str):
        self.check = check
        self.msg = msg

    def __or__(self, other: "Constraint") -> "Constraint":
        return Constraint(
            lambda x: self.check(x) or other.check(x),
            f"({self.msg} OR {other.msg})"
        )

    def __and__(self, other: "Constraint") -> "Constraint":
        return Constraint(
            lambda x: self.check(x) and other.check(x),
            f"({self.msg} AND {other.msg})"
        )


def validate_and_process(stream: List[Any]) -> Generator[Dict[str, Any], None, None]:
    is_str = Constraint(lambda x: isinstance(x, str), "must be string")
    is_num = Constraint(lambda x: isinstance(x, (int, float)), "must be number")
    is_positive = Constraint(lambda x: isinstance(x, (int, float)) and x > 0, "must be positive")
    not_empty = Constraint(lambda x: len(str(x).strip()) > 0, "cannot be blank")

    valid_payload = (is_str & not_empty) | (is_num & is_positive)

    for idx, item in enumerate(stream):
        if item is None or not valid_payload.check(item):
            yield {
                "status": "rejected",
                "index": idx,
                "input": item,
                "reason": f"Failed constraint rule: {valid_payload.msg}"
            }
            continue

        transformed = item.strip().upper() if isinstance(item, str) else item ** 2
        yield {
            "status": "processed",
            "index": idx,
            "input": item,
            "result": transformed
        }


def run_pipeline(data: List[Any]) -> List[Dict[str, Any]]:
    return list(validate_and_process(data))


if __name__ == "__main__":
    raw_inputs = ["  hello  ", -5, "", 4.5, None, "toolkit"]
    output = run_pipeline(raw_inputs)
    print(f"Processed {len(output)} items successfully.")
