"""Calculator with History - A simple calculator that tracks operation history."""

from calculator import Calculator
from history import History
from persistence import HistoryPersistence


class CalculatorWithHistory:
    """Calculator with operation history tracking."""
    
    def __init__(self, persistence_file: str = None):
        self.calculator = Calculator()
        self.history = History()
        self.persistence = HistoryPersistence(persistence_file) if persistence_file else None
    
    def add(self, a: float, b: float) -> float:
        result = self.calculator.add(a, b)
        self.history.add_operation('add', [a, b], result)
        return result
    
    def subtract(self, a: float, b: float) -> float:
        result = self.calculator.subtract(a, b)
        self.history.add_operation('subtract', [a, b], result)
        return result
    
    def multiply(self, a: float, b: float) -> float:
        result = self.calculator.multiply(a, b)
        self.history.add_operation('multiply', [a, b], result)
        return result
    
    def divide(self, a: float, b: float) -> float:
        result = self.calculator.divide(a, b)
        self.history.add_operation('divide', [a, b], result)
        return result
    
    def power(self, base: float, exponent: float) -> float:
        result = self.calculator.power(base, exponent)
        self.history.add_operation('power', [base, exponent], result)
        return result
    
    def square_root(self, number: float) -> float:
        result = self.calculator.square_root(number)
        self.history.add_operation('square_root', [number], result)
        return result
    
    def get_history(self, count: int = 10):
        return self.history.get_last_operations(count)
    
    def clear_history(self):
        self.history.clear_history()
    
    def get_statistics(self):
        return self.history.get_statistics()
    
    def save_to_file(self) -> bool:
        """Save history to file using persistence layer."""
        if self.persistence is None:
            raise ValueError("No persistence file configured")
        return self.persistence.save_history(self.history.operations)
    
    def load_from_file(self) -> bool:
        """Load history from file using persistence layer."""
        if self.persistence is None:
            raise ValueError("No persistence file configured")
        loaded_ops = self.persistence.load_history()
        if loaded_ops:
            self.history.operations = loaded_ops
            return True
        return False


def main():
    """Demo function for the calculator."""
    calc = CalculatorWithHistory()
    
    print("Calculator with History Demo")
    print("=" * 30)
    
    # Perform some operations
    print(f"10 + 5 = {calc.add(10, 5)}")
    print(f"20 - 3 = {calc.subtract(20, 3)}")
    print(f"4 * 7 = {calc.multiply(4, 7)}")
    print(f"15 / 3 = {calc.divide(15, 3)}")
    print(f"2 ^ 8 = {calc.power(2, 8)}")
    print(f"√16 = {calc.square_root(16)}")
    
    print("\nOperation History:")
    print("-" * 20)
    for i, op in enumerate(calc.get_history(), 1):
        operands_str = ', '.join(map(str, op['operands']))
        print(f"{i}. {op['operation']}({operands_str}) = {op['result']}")
    
    print("\nStatistics:")
    print("-" * 15)
    stats = calc.get_statistics()
    print(f"Total operations: {stats['total_operations']}")
    print(f"Operation types: {stats['operation_types']}")
    print(f"Average result: {stats['average_result']:.2f}")


if __name__ == "__main__":
    main()
