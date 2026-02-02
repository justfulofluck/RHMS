#!/usr/bin/env python3
"""
Test script to verify the monthly_availability.html redirect fix
"""
import re
import os

def test_fix():
    file_path = 'revana_hms/doctors/templates/doctors/monthly_availability.html'
    
    if not os.path.exists(file_path):
        print("❌ File not found:", file_path)
        return False
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Test 1: Check for enhanced configuration
    if 'APP_CONFIG' in content and 'FALLBACK_AVAILABILITY_URL' in content:
        print("✅ Enhanced configuration object found")
    else:
        print("❌ Enhanced configuration object missing")
        return False
    
    # Test 2: Check for debugging logs
    debug_patterns = [
        'DEBUG: URL Configuration',
        'DEBUG: Form submission started',
        'DEBUG: Response status',
        'DEBUG: Success path triggered',
        'DEBUG: Redirect timer executed'
    ]
    
    for pattern in debug_patterns:
        if pattern in content:
            print(f"✅ Debug log found: {pattern}")
        else:
            print(f"❌ Debug log missing: {pattern}")
            return False
    
    # Test 3: Check for fallback mechanism
    if "targetUrl.includes('availability')" in content:
        print('✅ Fallback URL validation found')
    else:
        print('❌ Fallback URL validation missing')
        return False
    
    # Test 4: Check for enhanced error handling
    if 'response.ok' in content and 'err.stack' in content:
        print("✅ Enhanced error handling found")
    else:
        print("❌ Enhanced error handling missing")
        return False
    
    # Test 5: Check for proper structure (no duplicate handlers)
    fetch_count = content.count('fetch(APP_CONFIG.MONTHLY_AVAILABILITY_URL')
    if fetch_count == 1:
        print("✅ Single fetch handler found")
    else:
        print(f"❌ Multiple fetch handlers found: {fetch_count}")
        return False
    
    # Test 6: Check Django template tags are properly quoted
    if 'AVAILABILITY_LIST_URL: \"{% url' in content:
        print("✅ Django template tags properly quoted")
    else:
        print("❌ Django template tags not properly quoted")
        return False
    
    print("\n🎉 All tests passed! The redirect fix has been successfully applied.")
    return True

if __name__ == "__main__":
    success = test_fix()
    exit(0 if success else 1)
