"""
Basic functionality tests for voice assistant
"""

import os
import sys
import json
import tempfile

def test_config_loading():
    """Test configuration file loading"""
    print("Testing config loading...")
    
    # Create temporary config
    config_data = {
        "wake_word": "test",
        "whisper_model": "tiny",
        "output_file": "test_output.txt"
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        temp_config = f.name
    
    try:
        # Test loading
        with open(temp_config, 'r') as f:
            loaded = json.load(f)
        
        assert loaded['wake_word'] == "test"
        assert loaded['whisper_model'] == "tiny"
        print("✓ Config loading works")
    finally:
        os.unlink(temp_config)

def test_imports():
    """Test that all required modules can be imported"""
    print("\nTesting imports...")
    
    required_modules = [
        'numpy',
        'pyaudio',
        'pvporcupine',
        'whisper',
        'symspellpy',
        'tkinter',
        'matplotlib'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            if module == 'tkinter':
                import tkinter
            else:
                __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\nFailed to import: {', '.join(failed_imports)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_file_structure():
    """Test that required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'voice_assistant.py',
        'config.json',
        'requirements.txt',
        'README.md',
        'build_exe.py',
        'setup_symspell.py'
    ]
    
    missing_files = []
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✓ {filename}")
        else:
            print(f"✗ {filename} not found")
            missing_files.append(filename)
    
    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        return False
    
    return True

def test_config_validity():
    """Test that config.json is valid"""
    print("\nTesting config.json validity...")
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        required_keys = [
            'wake_word',
            'whisper_model',
            'audio_sample_rate',
            'output_file'
        ]
        
        for key in required_keys:
            if key in config:
                print(f"✓ {key}: {config[key]}")
            else:
                print(f"✗ Missing key: {key}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error reading config: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Voice Assistant - Basic Functionality Tests")
    print("=" * 60)
    
    results = []
    
    # Test 1: File structure
    results.append(("File Structure", test_file_structure()))
    
    # Test 2: Config validity
    results.append(("Config Validity", test_config_validity()))
    
    # Test 3: Config loading
    try:
        test_config_loading()
        results.append(("Config Loading", True))
    except Exception as e:
        print(f"✗ Config loading failed: {e}")
        results.append(("Config Loading", False))
    
    # Test 4: Imports
    results.append(("Module Imports", test_imports()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
