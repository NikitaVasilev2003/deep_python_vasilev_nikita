class SomeModel:
    def predict(self, message: str) -> float:
        # Реализация не важна, будет заменена в тестах
        return 0.0


def predict_message_mood(
    message: str,
    bad_threshold: float = 0.3,
    good_threshold: float = 0.8,
) -> str:
    model = SomeModel()
    prediction = model.predict(message)
    if prediction < bad_threshold:
        return "неуд"
    elif prediction > good_threshold:
        return "отл"
    else:
        return "норм"
