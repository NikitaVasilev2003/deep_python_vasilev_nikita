import unittest
from unittest.mock import patch
from mood_predictor import predict_message_mood, SomeModel


class TestPredictMessageMood(unittest.TestCase):
    def test_neud(self):
        with patch.object(SomeModel, "predict") as mock_predict:
            mock_predict.return_value = 0.2
            result = predict_message_mood("test message")
            self.assertEqual(result, "неуд")
            mock_predict.assert_called_once_with("test message")

    def test_otl(self):
        with patch.object(SomeModel, "predict") as mock_predict:
            mock_predict.return_value = 0.9
            result = predict_message_mood("test message")
            self.assertEqual(result, "отл")
            mock_predict.assert_called_once_with("test message")

    def test_norm(self):
        with patch.object(SomeModel, "predict") as mock_predict:
            mock_predict.return_value = 0.5
            result = predict_message_mood("test message")
            self.assertEqual(result, "норм")

    def test_custom_thresholds(self):
        with patch.object(SomeModel, "predict") as mock_predict:
            mock_predict.return_value = 0.85
            result = predict_message_mood("test", bad_threshold=0.8, good_threshold=0.8)
            self.assertEqual(result, "отл")

            mock_predict.return_value = 0.8
            result = predict_message_mood("test", bad_threshold=0.8, good_threshold=0.8)
            self.assertEqual(result, "норм")

            mock_predict.return_value = 0.7
            result = predict_message_mood("test", bad_threshold=0.6, good_threshold=0.8)
            self.assertEqual(result, "норм")

    def test_edge_cases(self):
        with patch.object(SomeModel, "predict") as mock_predict:
            mock_predict.return_value = 0.3
            result = predict_message_mood("test", bad_threshold=0.3)
            self.assertEqual(result, "норм")

            mock_predict.return_value = 0.8
            result = predict_message_mood("test", good_threshold=0.8)
            self.assertEqual(result, "норм")

    def test_sample_cases(self):
        with patch.object(SomeModel, "predict") as mock_predict:
            mock_predict.return_value = 0.85
            self.assertEqual(predict_message_mood("Чапаев и пустота"), "отл")

            mock_predict.return_value = 0.9
            self.assertEqual(
                predict_message_mood("Чапаев и пустота", 0.8, 0.99), "норм"
            )

            mock_predict.return_value = 0.2
            self.assertEqual(predict_message_mood("Вулкан"), "неуд")


if __name__ == "__main__":
    unittest.main()
