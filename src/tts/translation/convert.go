package translation

import (
	"cloud.google.com/go/texttospeech/apiv1"
	"context"
	texttospeechpb "google.golang.org/genproto/googleapis/cloud/texttospeech/v1"
)

func Convert(text string) (AudioContent, error) {
	req := texttospeechpb.SynthesizeSpeechRequest{
		Input: &texttospeechpb.SynthesisInput{
			InputSource: &texttospeechpb.SynthesisInput_Text{Text: text},
		},
		Voice: &texttospeechpb.VoiceSelectionParams{
			LanguageCode: "ru-RU",
			SsmlGender:   texttospeechpb.SsmlVoiceGender_NEUTRAL,
		},
		AudioConfig: &texttospeechpb.AudioConfig{
			AudioEncoding:   texttospeechpb.AudioEncoding_LINEAR16,
			SampleRateHertz: 8000,
		},
	}
	ctx := context.Background()
	ttsClient, err := texttospeech.NewClient(ctx)
	if err != nil {
		return nil, err
	}

	resp, err := ttsClient.SynthesizeSpeech(ctx, &req)
	if err != nil {
		return nil, err
	}
	return AudioContent(resp.GetAudioContent()), nil
}
