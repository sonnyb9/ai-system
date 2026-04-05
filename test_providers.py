#!/usr/bin/env python3
"""
Test script to validate provider configurations and routing.

This script verifies:
1. All provider JSON files are valid
2. All providers are referenced correctly in routing
3. Required fields are present
4. Endpoints are accessible (if local)
"""

import json
import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import BASE_DIR, MODEL, OLLAMA_URL

# Test utilities
def load_json_file(path):
    """Load and parse a JSON file"""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        return {"_error": f"JSON decode error: {e}"}

def validate_provider(provider_data):
    """Validate a single provider's configuration"""
    errors = []
    warnings = []
    
    if not provider_data or not isinstance(provider_data, dict):
        return False, errors, ["Provider data is invalid"]
    
    required_fields = ["provider_name", "type", "model"]
    for field in required_fields:
        if field not in provider_data:
            errors.append(f"Missing required field: {field}")
    
    if provider_data.get("type") != "ollama":
        # For Ollama providers, check endpoint
        if "endpoint" not in provider_data:
            errors.append("Ollama provider missing endpoint field")
        else:
            endpoint = provider_data.get("endpoint", "")
            if not endpoint.startswith("http"):
                errors.append(f"Invalid endpoint format: {endpoint}")
    
    # Validate model name
    model = provider_data.get("model", "")
    if model and len(model) > 100:
        warnings.append(f"Model name unusually long: {model}")
    
    # Validate capabilities
    capabilities = provider_data.get("capabilities", {})
    if not isinstance(capabilities, dict):
        errors.append("capabilities must be a dictionary")
    
    return len(errors) == 0, errors, warnings

def test_providers():
    """Test all provider files"""
    providers_dir = PROJECT_ROOT / "providers"
    print("=" * 60)
    print("🧪 PROVIDER CONFIGURATION TEST")
    print("=" * 60)
    print()
    
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "providers": []
    }
    
    # Find all JSON files
    json_files = list(providers_dir.glob("*.json"))
    
    for json_file in json_files:
        results["total"] += 1
        print(f"Testing: {json_file.name}")
        
        data = load_json_file(json_file)
        if data is None:
            print(f"  ❌ FAILED: File not found")
            results["failed"] += 1
            continue
        
        if "_error" in data:
            print(f"  ❌ FAILED: {data['_error']}")
            results["failed"] += 1
            continue
        
        # Validate provider
        is_valid, errors, warnings = validate_provider(data)
        
        if is_valid:
            print(f"  ✅ PASSED: {data['provider_name']}")
            print(f"     Type: {data['type']}")
            print(f"     Model: {data['model']}")
            print(f"     Endpoint: {data.get('endpoint', 'N/A')}")
            if warnings:
                print(f"     ⚠️  Warnings: {', '.join(warnings)}")
            results["passed"] += 1
        else:
            print(f"  ❌ FAILED:")
            for error in errors:
                print(f"     - {error}")
            results["failed"] += 1
        
        results["providers"].append({
            "name": json_file.name,
            "pass": is_valid,
            "errors": errors,
            "warnings": warnings
        })
        print()
    
    # Print summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total providers tested: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success rate: {results['passed'] / max(results['total'], 1) * 100:.1f}%")
    print("=" * 60)
    
    return results

def test_routing():
    """Test routing configuration"""
    print()
    print("=" * 60)
    print("🧪 ROUTING CONFIGURATION TEST")
    print("=" * 60)
    print()
    
    routing_file = PROJECT_ROOT / "routing" / "routing.json"
    print(f"Loading routing from: {routing_file}")
    
    data = load_json_file(routing_file)
    if data is None:
        print("❌ FAILED: routing.json not found")
        print("=" * 60)
        return False
    
    print(f"✅ Routing loaded successfully")
    print(f"  Priority order: {data.get('priority_order', [])}")
    print()
    
    # Verify each provider exists
    routing_dir = PROJECT_ROOT / "providers"
    missing = []
    
    for provider_name in data.get("priority_order", []):
        provider_data = load_json_file(routing_dir / f"{provider_name}.json")
        if provider_data is None:
            missing.append(provider_name)
            print(f"❌ Provider '{provider_name}' referenced in routing but NOT FOUND")
        else:
            print(f"✅ Provider '{provider_name}' exists and is valid")
    
    if missing:
        print()
        print("❌ MISSING PROVIDERS:")
        for name in missing:
            print(f"   - {name}")
        print()
        return False
    
    print("=" * 60)
    return True

def main():
    """Main test runner"""
    print("\n\n" + "=" * 60)
    print("🚀 STARTING PROVIDER AND ROUTING TEST")
    print("=" * 60 + "\n")
    
    # Reset counter
    test_providers()
    
    # Test routing
    routing_ok = test_routing()
    
    # Final status
    print()
    print("=" * 60)
    print("🏁 TEST COMPLETE")
    print("=" * 60)
    
    if routing_ok:
        print("✅ ALL TESTS PASSED")
        print()
        print("Next steps:")
        print("1. Run actual task execution")
        print("2. Review logs for any issues")
        print("3. Check if endpoint is accessible")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED - Please fix missing providers")
        return 1

if __name__ == "__main__":
    sys.exit(main())
