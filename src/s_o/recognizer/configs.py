from google.cloud.speech import types, enums


def get_recognition_config() -> types.RecognitionConfig:
    return types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='ru-RU',
        max_alternatives=1,
    )


def get_streaming_recognition_config(config: types.RecognitionConfig) -> types.StreamingRecognitionConfig:
    return types.StreamingRecognitionConfig(
        config=config,
        # single_utterance=True,
        interim_results=False,
    )
