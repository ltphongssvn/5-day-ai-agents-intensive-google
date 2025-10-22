# day7/core_primitives/tracing.py - Tracing for observability and debugging

from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
import json


class SpanType(Enum):
    """Types of trace spans."""

    AGENT_EXECUTION = "agent_execution"
    TOOL_CALL = "tool_call"
    LLM_CALL = "llm_call"
    HANDOFF = "handoff"
    VALIDATION = "validation"
    CUSTOM = "custom"


class EventType(Enum):
    """Types of trace events."""

    START = "start"
    END = "end"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"
    DEBUG = "debug"


class TraceEvent:
    """Individual event in a trace."""

    def __init__(
        self,
        event_type: EventType,
        message: str,
        data: Optional[Dict[str, Any]] = None,
    ):
        self.event_type = event_type
        self.message = message
        self.data = data or {}
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "type": self.event_type.value,
            "message": self.message,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
        }


class Span:
    """
    Trace Span: Represents a unit of work with start/end times.
    """

    def __init__(
        self,
        name: str,
        span_type: SpanType,
        parent_id: Optional[str] = None,
    ):
        self.span_id = f"{name}_{datetime.now().timestamp()}"
        self.name = name
        self.span_type = span_type
        self.parent_id = parent_id
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.duration_ms: Optional[float] = None
        self.events: List[TraceEvent] = []
        self.metadata: Dict[str, Any] = {}
        self.status = "in_progress"

    def add_event(self, event: TraceEvent):
        """Add an event to the span."""
        self.events.append(event)

    def log_info(self, message: str, data: Optional[Dict] = None):
        """Log info event."""
        self.add_event(TraceEvent(EventType.INFO, message, data))

    def log_warning(self, message: str, data: Optional[Dict] = None):
        """Log warning event."""
        self.add_event(TraceEvent(EventType.WARNING, message, data))

    def log_error(self, message: str, data: Optional[Dict] = None):
        """Log error event."""
        self.add_event(TraceEvent(EventType.ERROR, message, data))

    def log_debug(self, message: str, data: Optional[Dict] = None):
        """Log debug event."""
        self.add_event(TraceEvent(EventType.DEBUG, message, data))

    def set_metadata(self, key: str, value: Any):
        """Set metadata."""
        self.metadata[key] = value

    def end(self, status: str = "success"):
        """End the span."""
        self.end_time = datetime.now()
        self.duration_ms = (self.end_time - self.start_time).total_seconds() * 1000
        self.status = status

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "span_id": self.span_id,
            "name": self.name,
            "type": self.span_type.value,
            "parent_id": self.parent_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "events": [e.to_dict() for e in self.events],
            "metadata": self.metadata,
        }


class Tracer:
    """
    Tracer: Manages spans and events for observability.
    """

    def __init__(self, name: str = "default"):
        self.name = name
        self.spans: List[Span] = []
        self.active_spans: Dict[str, Span] = {}

    def start_span(
        self,
        name: str,
        span_type: SpanType,
        parent_id: Optional[str] = None,
    ) -> Span:
        """Start a new span."""
        span = Span(name, span_type, parent_id)
        span.add_event(TraceEvent(EventType.START, f"Started {name}"))
        self.spans.append(span)
        self.active_spans[span.span_id] = span
        return span

    def end_span(self, span: Span, status: str = "success"):
        """End a span."""
        span.end(status)
        span.add_event(TraceEvent(EventType.END, f"Ended {span.name}"))
        if span.span_id in self.active_spans:
            del self.active_spans[span.span_id]

    def get_trace(self) -> List[Dict[str, Any]]:
        """Get all spans as trace."""
        return [span.to_dict() for span in self.spans]

    def export_json(self) -> str:
        """Export trace as JSON."""
        return json.dumps(self.get_trace(), indent=2)

    def get_metrics(self) -> Dict[str, Any]:
        """Get trace metrics."""
        total_spans = len(self.spans)
        completed_spans = sum(1 for s in self.spans if s.status != "in_progress")
        failed_spans = sum(1 for s in self.spans if s.status == "failed")

        durations = [s.duration_ms for s in self.spans if s.duration_ms is not None]

        return {
            "tracer_name": self.name,
            "total_spans": total_spans,
            "completed_spans": completed_spans,
            "failed_spans": failed_spans,
            "active_spans": len(self.active_spans),
            "avg_duration_ms": sum(durations) / len(durations) if durations else 0,
            "total_events": sum(len(s.events) for s in self.spans),
        }

    def print_trace(self, show_events: bool = False):
        """Print trace in readable format."""
        print(f"\n=== Trace: {self.name} ===")

        for span in self.spans:
            indent = "  " if span.parent_id else ""
            duration = (
                f"{span.duration_ms:.2f}ms" if span.duration_ms else "in_progress"
            )
            print(
                f"{indent}[{span.span_type.value}] {span.name} - {duration} ({span.status})"
            )

            if show_events:
                for event in span.events:
                    print(f"{indent}  • {event.event_type.value}: {event.message}")


# Context manager for automatic span tracking
class traced_span:
    """Context manager for automatic span start/end."""

    def __init__(
        self,
        tracer: Tracer,
        name: str,
        span_type: SpanType = SpanType.CUSTOM,
    ):
        self.tracer = tracer
        self.name = name
        self.span_type = span_type
        self.span: Optional[Span] = None

    def __enter__(self) -> Span:
        self.span = self.tracer.start_span(self.name, self.span_type)
        return self.span

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.span:
            status = "failed" if exc_type else "success"
            if exc_val:
                self.span.log_error(str(exc_val))
            self.tracer.end_span(self.span, status)
        return False


# Demo function
def demo():
    """Demonstrate tracing."""
    print("=== Tracing Demo ===\n")

    # Create tracer
    tracer = Tracer("demo_trace")

    # Manual span management
    print("--- Manual Span Management ---")
    span1 = tracer.start_span("agent_task", SpanType.AGENT_EXECUTION)
    span1.log_info("Processing user request")
    span1.set_metadata("user_id", "user123")

    # Child span
    span2 = tracer.start_span("tool_call", SpanType.TOOL_CALL, parent_id=span1.span_id)
    span2.log_info("Calling weather tool")
    span2.set_metadata("tool_name", "get_weather")
    tracer.end_span(span2)

    span1.log_info("Task completed")
    tracer.end_span(span1)

    # Context manager usage
    print("--- Context Manager Usage ---")
    try:
        with traced_span(tracer, "llm_call", SpanType.LLM_CALL) as span:
            span.log_info("Sending prompt to LLM")
            span.set_metadata("model", "gpt-3.5-turbo")
            # Simulate work
            import time

            time.sleep(0.1)
            span.log_info("Received LLM response")
    except Exception as e:
        print(f"Error: {e}")

    # Demonstrate error tracking
    print("\n--- Error Tracking ---")
    try:
        with traced_span(tracer, "failing_task", SpanType.CUSTOM) as span:
            span.log_warning("This task will fail")
            raise ValueError("Simulated error")
    except ValueError:
        pass

    # Print trace
    tracer.print_trace(show_events=True)

    # Show metrics
    print("\n--- Metrics ---")
    metrics = tracer.get_metrics()
    for key, value in metrics.items():
        print(f"{key}: {value}")

    # Export JSON
    print("\n--- JSON Export (first span only) ---")
    trace_data = tracer.get_trace()
    print(json.dumps(trace_data[0], indent=2)[:500] + "...")


if __name__ == "__main__":
    demo()
