from analyzer.ml_model import predict_role

text = """
Python Pandas NumPy Statistics Machine Learning
"""

print(
    predict_role(text)
)