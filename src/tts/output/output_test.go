package output

import (
	"testing"
)

func TestFormatOutput(t *testing.T) {
	type args struct {
		filename string
	}
	tests := []struct {
		name       string
		args       args
		wantResult string
		wantErr    bool
	}{
		{"case1", args{"/tmp/1.raw"}, `{"filename":"/tmp/1.raw"}`, false},
		{"case2", args{"/tmp/проверка.raw"}, `{"filename":"/tmp/проверка.raw"}`, false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			gotResult, err := FormatOutput(tt.args.filename)
			if (err != nil) != tt.wantErr {
				t.Errorf("FormatOutput() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if gotResult != tt.wantResult {
				t.Errorf("FormatOutput() = %v, want %v", gotResult, tt.wantResult)
			}
		})
	}
}
