"""Comprehensive Integration Tests for Calculator with History System.

This test suite focuses on integration testing - verifying the correct 
interaction between different modules: Calculator, History, CalculatorWithHistory,
and HistoryPersistence.
"""

import pytest
import os
import json
from datetime import datetime
from pathlib import Path

from calculator import Calculator
from history import History
from main import CalculatorWithHistory
from persistence import HistoryPersistence


class TestCalculatorHistoryIntegration:
    """Test integration between Calculator and History modules."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calc_with_history = CalculatorWithHistory()
    
    def test_operation_with_history_recording(self):
        """
        Integration Test 1: Basic Calculator-History Integration
        Tests that mathematical operations are correctly recorded in history.
        
        Integration Points:
        - Calculator.add() → CalculatorWithHistory → History.add_operation()
        """
        result = self.calc_with_history.add(10, 5)
        
        # Verify calculation
        assert result == 15
        
        # Verify history integration
        history = self.calc_with_history.get_history(1)
        assert len(history) == 1
        assert history[0]['operation'] == 'add'
        assert history[0]['operands'] == [10, 5]
        assert history[0]['result'] == 15
        assert 'timestamp' in history[0]
        assert isinstance(history[0]['timestamp'], datetime)
    
    def test_multiple_operations_chain(self):
        """
        Integration Test 2: Sequential Operations Chain
        Tests that a sequence of operations maintains correct state across all modules.
        
        Integration Points:
        - Multiple Calculator operations
        - History accumulation and ordering
        - Last result tracking in Calculator
        """
        # Execute a chain: 5 + 3 = 8, 8 * 2 = 16, 16 / 4 = 4
        result1 = self.calc_with_history.add(5, 3)
        result2 = self.calc_with_history.multiply(result1, 2)
        result3 = self.calc_with_history.divide(result2, 4)
        
        # Verify final result
        assert result3 == 4.0
        
        # Verify Calculator state
        assert self.calc_with_history.calculator.get_last_result() == 4.0
        
        # Verify History integration - operations in reverse chronological order
        history = self.calc_with_history.get_history()
        assert len(history) == 3
        assert [op['operation'] for op in history] == ['divide', 'multiply', 'add']
        assert [op['result'] for op in history] == [4.0, 16, 8]
    
    def test_error_handling_across_modules(self):
        """
        Integration Test 3: Error Propagation
        Tests that errors from Calculator are properly handled and don't corrupt History.
        
        Integration Points:
        - Calculator error handling
        - History consistency after errors
        - State isolation between successful and failed operations
        """
        # Perform successful operation
        self.calc_with_history.add(10, 5)
        initial_count = len(self.calc_with_history.get_history())
        
        # Attempt invalid operation
        with pytest.raises(ZeroDivisionError):
            self.calc_with_history.divide(10, 0)
        
        # Verify error didn't add to history
        final_count = len(self.calc_with_history.get_history())
        assert final_count == initial_count
        
        # Verify system still works after error
        result = self.calc_with_history.multiply(3, 4)
        assert result == 12
        assert len(self.calc_with_history.get_history()) == initial_count + 1
    
    def test_statistics_integration(self):
        """
        Integration Test 4: Statistics Generation
        Tests integration between History operations and statistical calculations.
        
        Integration Points:
        - Calculator operations → History recording
        - History data → Statistics aggregation
        - Multiple operation types tracking
        """
        # Perform varied operations
        self.calc_with_history.add(10, 5)          # 15
        self.calc_with_history.add(20, 25)         # 45
        self.calc_with_history.multiply(3, 4)      # 12
        self.calc_with_history.subtract(50, 10)    # 40
        self.calc_with_history.power(2, 3)         # 8
        self.calc_with_history.square_root(16)     # 4
        
        # Verify statistics integration
        stats = self.calc_with_history.get_statistics()
        
        assert stats['total_operations'] == 6
        assert stats['operation_types']['add'] == 2
        assert stats['operation_types']['multiply'] == 1
        assert stats['operation_types']['subtract'] == 1
        assert stats['operation_types']['power'] == 1
        assert stats['operation_types']['square_root'] == 1
        
        # Verify calculated statistics
        expected_avg = (15 + 45 + 12 + 40 + 8 + 4) / 6
        assert abs(stats['average_result'] - expected_avg) < 0.001
        assert stats['max_result'] == 45
        assert stats['min_result'] == 4
    
    def test_history_limit_integration(self):
        """
        Integration Test 5: History Size Management
        Tests that History correctly limits size while maintaining Calculator functionality.
        
        Integration Points:
        - Calculator operations under high load
        - History size management
        - Data integrity when exceeding limits
        """
        # Create calculator with small history limit
        small_history = History(max_size=5)
        calc = CalculatorWithHistory()
        calc.history = small_history
        
        # Add more operations than limit
        for i in range(10):
            calc.add(i, 1)
        
        # Verify history size is capped
        assert calc.history.get_operation_count() == 5
        
        # Verify most recent operations are kept
        history = calc.get_history()
        results = [op['result'] for op in reversed(history)]
        assert results == [6, 7, 8, 9, 10]  # Last 5 operations


class TestPersistenceIntegration:
    """Test integration between CalculatorWithHistory and Persistence modules."""
    
    def setup_method(self):
        """Set up test fixtures with temporary file."""
        self.test_file = "test_history.json"
        self.calc = CalculatorWithHistory(persistence_file=self.test_file)
    
    def teardown_method(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_and_load_integration(self):
        """
        Integration Test 6: Save/Load Cycle
        Tests complete data flow from Calculator through History to file storage.
        
        Integration Points:
        - Calculator operations → History
        - History → HistoryPersistence.save_history()
        - File I/O
        - HistoryPersistence.load_history() → History
        """
        # Perform operations
        self.calc.add(10, 5)
        self.calc.multiply(3, 7)
        self.calc.subtract(20, 8)
        
        # Save to file
        assert self.calc.save_to_file() is True
        assert os.path.exists(self.test_file)
        
        # Create new calculator and load
        new_calc = CalculatorWithHistory(persistence_file=self.test_file)
        assert new_calc.load_from_file() is True
        
        # Verify loaded history matches original
        original_history = self.calc.get_history()
        loaded_history = new_calc.get_history()
        
        assert len(loaded_history) == len(original_history)
        
        for orig, loaded in zip(original_history, loaded_history):
            assert orig['operation'] == loaded['operation']
            assert orig['operands'] == loaded['operands']
            assert orig['result'] == loaded['result']
    
    def test_persistence_data_integrity(self):
        """
        Integration Test 7: Data Format Integrity
        Tests that data maintains integrity through serialization/deserialization.
        
        Integration Points:
        - History data structures
        - JSON serialization (datetime handling)
        - Data type preservation
        """
        # Add operations with various data types
        self.calc.add(10.5, 5.3)
        self.calc.power(2, 8)
        self.calc.square_root(144)
        
        self.calc.save_to_file()
        
        # Manually verify JSON structure
        with open(self.test_file, 'r') as f:
            data = json.load(f)
        
        assert isinstance(data, list)
        assert len(data) == 3
        
        # Verify data types are preserved
        assert isinstance(data[0]['result'], float)
        assert isinstance(data[0]['operands'], list)
        assert isinstance(data[0]['timestamp'], str)  # Serialized as ISO string
    
    def test_concurrent_operations_and_save(self):
        """
        Integration Test 8: Concurrent Modifications
        Tests system behavior under rapid operations and saves.
        
        Integration Points:
        - Multiple rapid Calculator operations
        - History state consistency
        - File write reliability
        """
        # Perform rapid operations
        for i in range(20):
            self.calc.add(i, 1)
            if i % 5 == 0:
                self.calc.save_to_file()
        
        # Final save
        self.calc.save_to_file()
        
        # Load and verify
        verify_calc = CalculatorWithHistory(persistence_file=self.test_file)
        verify_calc.load_from_file()
        
        assert verify_calc.history.get_operation_count() == 20
        
        # Verify statistics work after load
        stats = verify_calc.get_statistics()
        assert stats['total_operations'] == 20
        assert stats['operation_types']['add'] == 20


class TestComplexScenarios:
    """Test complex real-world scenarios involving all modules."""
    
    def test_calculator_session_workflow(self):
        """
        Integration Test 9: Complete User Session
        Simulates a realistic user session with all features.
        
        Integration Points:
        - All calculator operations
        - History tracking
        - Statistics generation
        - Clear functionality
        """
        calc = CalculatorWithHistory()
        
        # Session: Calculate (10 + 5) * 2 - 8 / 2
        step1 = calc.add(10, 5)        # 15
        step2 = calc.multiply(step1, 2)  # 30
        step3 = calc.divide(8, 2)        # 4
        final = calc.subtract(step2, step3)  # 26
        
        assert final == 26
        
        # Check session statistics
        stats = calc.get_statistics()
        assert stats['total_operations'] == 4
        
        # Clear history and verify
        calc.clear_history()
        assert calc.history.get_operation_count() == 0
        
        # Verify calculator still works after clear
        new_result = calc.add(100, 200)
        assert new_result == 300
    
    def test_error_recovery_scenario(self):
        """
        Integration Test 10: Error Recovery
        Tests system recovery after various error conditions.
        
        Integration Points:
        - Error handling across all modules
        - State consistency after errors
        - Continued functionality post-error
        """
        calc = CalculatorWithHistory()
        
        # Successful operation
        calc.add(10, 5)
        
        # Multiple errors
        errors_caught = 0
        try:
            calc.divide(5, 0)
        except ZeroDivisionError:
            errors_caught += 1
        
        try:
            calc.square_root(-16)
        except ValueError:
            errors_caught += 1
        
        try:
            calc.power(-2, 0.5)
        except ValueError:
            errors_caught += 1
        
        assert errors_caught == 3
        
        # Verify only successful operation in history
        assert calc.history.get_operation_count() == 1
        
        # System should still work
        result = calc.multiply(6, 7)
        assert result == 42
        assert calc.history.get_operation_count() == 2
    
    def test_persistence_with_empty_and_full_history(self):
        """
        Integration Test 11: Edge Cases in Persistence
        Tests persistence behavior with edge cases.
        
        Integration Points:
        - Empty history save/load
        - Large history save/load
        - File system interaction
        """
        test_file = "edge_case_history.json"
        
        try:
            # Test empty history
            calc1 = CalculatorWithHistory(persistence_file=test_file)
            calc1.save_to_file()
            
            calc2 = CalculatorWithHistory(persistence_file=test_file)
            calc2.load_from_file()
            assert calc2.history.get_operation_count() == 0
            
            # Test large history
            for i in range(100):
                calc1.add(i, i + 1)
            
            calc1.save_to_file()
            
            calc3 = CalculatorWithHistory(persistence_file=test_file)
            calc3.load_from_file()
            assert calc3.history.get_operation_count() == 100
            
            # Verify statistics still work
            stats = calc3.get_statistics()
            assert stats['total_operations'] == 100
            
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)


class TestModuleBoundaries:
    """Test integration at module boundaries and contracts."""
    
    def test_calculator_independence(self):
        """
        Integration Test 12: Module Independence
        Verify Calculator works independently and integrates properly.
        
        Tests the contract between Calculator and CalculatorWithHistory.
        """
        # Direct calculator usage
        calc = Calculator()
        result = calc.add(5, 3)
        assert result == 8
        assert calc.get_last_result() == 8
        
        # Integrated usage
        calc_with_hist = CalculatorWithHistory()
        result = calc_with_hist.add(5, 3)
        assert result == 8
        assert calc_with_hist.calculator.get_last_result() == 8
        
        # Both should produce same mathematical results
        assert calc.multiply(4, 5) == calc_with_hist.multiply(4, 5)
    
    def test_history_search_integration(self):
        """
        Integration Test 13: History Search Functionality
        Tests searching across accumulated operations.
        
        Integration Points:
        - Calculator operations of various types
        - History search functionality
        - Data filtering and retrieval
        """
        calc = CalculatorWithHistory()
        
        # Perform varied operations
        calc.add(1, 2)
        calc.multiply(3, 4)
        calc.add(5, 6)
        calc.divide(10, 2)
        calc.add(7, 8)
        
        # Search for specific operation type
        add_ops = calc.history.search_operations('add')
        assert len(add_ops) == 3
        
        multiply_ops = calc.history.search_operations('multiply')
        assert len(multiply_ops) == 1
        assert multiply_ops[0]['result'] == 12


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
