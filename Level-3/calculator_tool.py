def calculate(expression):
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return result
    except Exception as e:
        return f"❌ Invalid expression: {e}"
