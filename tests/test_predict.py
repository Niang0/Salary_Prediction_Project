from src.predict import (
  load_model,
  predict_salary,
)

def test_predict_salary():

  model = load_model()

  prediction = predict_salary(
    model,
    [30, 5, 1, 0, 0]
  )

  assert prediction is not None