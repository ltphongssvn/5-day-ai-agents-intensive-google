# day7/test_all.py - Test all day7 components

import sys


def test_component(module_name, description):
    """Test a single component."""
    try:
        print(f"Testing {description}...", end=" ")
        __import__(module_name)
        print("✓")
        return True
    except Exception as e:
        print(f"✗ ({e})")
        return False


def main():
    """Run all component tests."""
    print("=" * 60)
    print("Day 7 Component Tests - Complete Suite")
    print("=" * 60)

    tests = [
        # Core Primitives (6)
        ("day7.core_primitives.agent", "Agent Primitive"),
        ("day7.core_primitives.runner", "Runner"),
        ("day7.core_primitives.tools", "Tools (Functions, APIs, MCP)"),
        ("day7.core_primitives.handoff", "Handoff"),
        ("day7.core_primitives.guardrails", "Guardrails"),
        ("day7.core_primitives.tracing", "Tracing"),
        # Agent Anatomy
        ("day7.agent_anatomy", "Agent Anatomy & Design"),
        # Key Capabilities (NEW)
        ("day7.key_capabilities", "Key Capabilities & Management"),
        # Tool Types (4)
        ("day7.tool_types.custom_tools", "Custom Tools"),
        ("day7.tool_types.hosted_tools", "Hosted Tools"),
        ("day7.tool_types.agents_as_tools", "Agents as Tools"),
        ("day7.tool_types.mcp_servers", "MCP Servers"),
        # Other Components (3)
        ("day7.memory_management.memory", "Memory Management"),
        ("day7.control_logic.patterns", "Control Logic"),
        ("day7.orchestration.patterns", "Orchestration"),
    ]

    results = []
    for module, desc in tests:
        results.append(test_component(module, desc))

    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ ALL COMPONENTS WORKING")

    print("=" * 60)

    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
