# day7/core_primitives/guardrails.py - Guardrails for input/output validation and policy enforcement

from typing import Any, Dict, List, Callable
from datetime import datetime
from enum import Enum


class GuardrailType(Enum):
    """Types of guardrails."""

    INPUT_VALIDATION = "input_validation"
    OUTPUT_VALIDATION = "output_validation"
    CONTENT_FILTER = "content_filter"
    POLICY_ENFORCEMENT = "policy_enforcement"


class GuardrailViolation(Exception):
    """Exception raised when a guardrail is violated."""

    def __init__(self, message: str, guardrail_name: str, violation_type: str):
        self.message = message
        self.guardrail_name = guardrail_name
        self.violation_type = violation_type
        super().__init__(self.message)


class Guardrail:
    """
    Base Guardrail class for validation and policy enforcement.
    """

    def __init__(
        self,
        name: str,
        guardrail_type: GuardrailType,
        check_function: Callable[[Any], bool],
        error_message: str = "Guardrail violation",
    ):
        self.name = name
        self.guardrail_type = guardrail_type
        self.check_function = check_function
        self.error_message = error_message
        self.violations: List[Dict[str, Any]] = []
        self.checks_performed = 0

    def check(self, data: Any) -> bool:
        """Check if data passes the guardrail."""
        self.checks_performed += 1

        try:
            passed = self.check_function(data)

            if not passed:
                violation = {
                    "timestamp": datetime.now().isoformat(),
                    "data": str(data)[:100],  # Limit length
                    "message": self.error_message,
                }
                self.violations.append(violation)

            return passed

        except Exception as e:
            violation = {
                "timestamp": datetime.now().isoformat(),
                "data": str(data)[:100],
                "message": f"Check failed: {str(e)}",
            }
            self.violations.append(violation)
            return False

    def enforce(self, data: Any):
        """Enforce the guardrail, raising exception on violation."""
        if not self.check(data):
            raise GuardrailViolation(
                self.error_message,
                self.name,
                self.guardrail_type.value,
            )

    def get_metrics(self) -> Dict[str, Any]:
        """Get guardrail metrics."""
        return {
            "name": self.name,
            "type": self.guardrail_type.value,
            "checks_performed": self.checks_performed,
            "violations": len(self.violations),
            "violation_rate": (
                len(self.violations) / self.checks_performed
                if self.checks_performed > 0
                else 0
            ),
        }


class GuardrailManager:
    """
    Manages multiple guardrails for input/output validation.
    """

    def __init__(self, enforce_mode: bool = True):
        self.enforce_mode = enforce_mode
        self.input_guardrails: List[Guardrail] = []
        self.output_guardrails: List[Guardrail] = []
        self.total_checks = 0
        self.total_violations = 0

    def add_input_guardrail(self, guardrail: Guardrail):
        """Add an input validation guardrail."""
        self.input_guardrails.append(guardrail)

    def add_output_guardrail(self, guardrail: Guardrail):
        """Add an output validation guardrail."""
        self.output_guardrails.append(guardrail)

    def validate_input(self, data: Any) -> bool:
        """Validate input against all input guardrails."""
        self.total_checks += len(self.input_guardrails)

        for guardrail in self.input_guardrails:
            if self.enforce_mode:
                try:
                    guardrail.enforce(data)
                except GuardrailViolation:
                    self.total_violations += 1
                    raise
            else:
                if not guardrail.check(data):
                    self.total_violations += 1
                    return False

        return True

    def validate_output(self, data: Any) -> bool:
        """Validate output against all output guardrails."""
        self.total_checks += len(self.output_guardrails)

        for guardrail in self.output_guardrails:
            if self.enforce_mode:
                try:
                    guardrail.enforce(data)
                except GuardrailViolation:
                    self.total_violations += 1
                    raise
            else:
                if not guardrail.check(data):
                    self.total_violations += 1
                    return False

        return True

    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics."""
        return {
            "enforce_mode": self.enforce_mode,
            "total_checks": self.total_checks,
            "total_violations": self.total_violations,
            "input_guardrails": [g.get_metrics() for g in self.input_guardrails],
            "output_guardrails": [g.get_metrics() for g in self.output_guardrails],
        }


# Pre-built guardrails


def create_length_guardrail(
    name: str,
    max_length: int,
    guardrail_type: GuardrailType = GuardrailType.INPUT_VALIDATION,
) -> Guardrail:
    """Create a length validation guardrail."""

    def check_length(data: Any) -> bool:
        return len(str(data)) <= max_length

    return Guardrail(
        name=name,
        guardrail_type=guardrail_type,
        check_function=check_length,
        error_message=f"Data exceeds maximum length of {max_length}",
    )


def create_content_filter_guardrail(
    name: str,
    blocked_words: List[str],
) -> Guardrail:
    """Create a content filter guardrail."""

    def check_content(data: Any) -> bool:
        text = str(data).lower()
        return not any(word.lower() in text for word in blocked_words)

    return Guardrail(
        name=name,
        guardrail_type=GuardrailType.CONTENT_FILTER,
        check_function=check_content,
        error_message="Content contains blocked words",
    )


def create_format_guardrail(
    name: str,
    allowed_formats: List[str],
) -> Guardrail:
    """Create a format validation guardrail."""

    def check_format(data: Any) -> bool:
        if isinstance(data, dict) and "format" in data:
            return data["format"] in allowed_formats
        return True

    return Guardrail(
        name=name,
        guardrail_type=GuardrailType.INPUT_VALIDATION,
        check_function=check_format,
        error_message=f"Format must be one of: {', '.join(allowed_formats)}",
    )


def create_policy_guardrail(
    name: str,
    policy_function: Callable[[Any], bool],
    policy_description: str,
) -> Guardrail:
    """Create a custom policy enforcement guardrail."""
    return Guardrail(
        name=name,
        guardrail_type=GuardrailType.POLICY_ENFORCEMENT,
        check_function=policy_function,
        error_message=f"Policy violation: {policy_description}",
    )


# Demo function
def demo():
    """Demonstrate guardrails."""
    print("=== Guardrails Demo ===\n")

    # Create guardrail manager
    manager = GuardrailManager(enforce_mode=False)

    # Add input guardrails
    length_guard = create_length_guardrail("input_length", max_length=100)
    content_guard = create_content_filter_guardrail(
        "content_filter",
        blocked_words=["spam", "hack", "malicious"],
    )

    manager.add_input_guardrail(length_guard)
    manager.add_input_guardrail(content_guard)

    # Add output guardrail
    output_length = create_length_guardrail(
        "output_length",
        max_length=200,
        guardrail_type=GuardrailType.OUTPUT_VALIDATION,
    )
    manager.add_output_guardrail(output_length)

    # Test input validation
    print("--- Input Validation ---")

    test_inputs = [
        "Hello, this is a valid input",
        "This input contains spam content",
        "A" * 150,  # Too long
    ]

    for i, test_input in enumerate(test_inputs, 1):
        try:
            is_valid = manager.validate_input(test_input)
            print(
                f"Test {i}: {'✓ PASS' if is_valid else '✗ FAIL'} - {test_input[:50]}..."
            )
        except GuardrailViolation as e:
            print(f"Test {i}: ✗ VIOLATION - {e.message}")

    # Test output validation
    print("\n--- Output Validation ---")

    test_outputs = [
        "This is a valid output",
        "B" * 250,  # Too long
    ]

    for i, test_output in enumerate(test_outputs, 1):
        try:
            is_valid = manager.validate_output(test_output)
            print(f"Output {i}: {'✓ PASS' if is_valid else '✗ FAIL'}")
        except GuardrailViolation as e:
            print(f"Output {i}: ✗ VIOLATION - {e.message}")

    # Show metrics
    print("\n--- Metrics ---")
    metrics = manager.get_metrics()
    print(f"Total checks: {metrics['total_checks']}")
    print(f"Total violations: {metrics['total_violations']}")
    print(f"Input guardrails: {len(metrics['input_guardrails'])}")
    print(f"Output guardrails: {len(metrics['output_guardrails'])}")

    # Test enforce mode
    print("\n--- Enforce Mode Test ---")
    manager_strict = GuardrailManager(enforce_mode=True)
    manager_strict.add_input_guardrail(content_guard)

    try:
        manager_strict.validate_input("This contains spam")
        print("✓ Input accepted")
    except GuardrailViolation as e:
        print(f"✗ Input rejected: {e.message}")


if __name__ == "__main__":
    demo()
