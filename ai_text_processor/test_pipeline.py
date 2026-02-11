#!/usr/bin/env python3
"""
Quick test script for the AI Text Processor.
Runs basic validation tests without requiring OpenAI API key.
"""

import sys
sys.path.insert(0, '.')

def test_pipeline():
    """Test the full processing pipeline."""
    from pipeline.processor import processor
    
    test_cases = [
        {
            'name': 'Bengali digits with emoji',
            'input': 'Rahim ০১৭১১১২৩৪৫৬ 😊\nDhaka Mirpur',
            'expected_blocks': 1
        },
        {
            'name': 'Two orders',
            'input': 'Rahim 01711234567\nDhaka\n\nKarim 01812345678\nChittagong',
            'expected_blocks': 2
        },
        {
            'name': 'Phone with +88 prefix',
            'input': 'Ahmed +8801911234567\nSylhet\nShoes 2 pc',
            'expected_blocks': 1
        }
    ]
    
    print("🧪 Testing AI Text Processor Pipeline\n")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print("-" * 60)
        
        try:
            result = processor.process_text(test['input'])
            
            blocks_ok = result['blocks_processed'] == test['expected_blocks']
            has_orders = len(result['results']['orders']) > 0
            
            if blocks_ok and has_orders:
                print(f"✅ PASSED")
                print(f"   Blocks: {result['blocks_processed']}/{test['expected_blocks']}")
                print(f"   Orders: {len(result['results']['orders'])}")
                print(f"   Time: {result['processing_time']}")
                passed += 1
            else:
                print(f"❌ FAILED")
                print(f"   Blocks: {result['blocks_processed']}/{test['expected_blocks']}")
                print(f"   Orders: {len(result['results']['orders'])}")
                failed += 1
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    print("\n✨ All systems operational!" if failed == 0 else "\n⚠️  Some tests failed")
    
    return failed == 0


if __name__ == '__main__':
    success = test_pipeline()
    sys.exit(0 if success else 1)
