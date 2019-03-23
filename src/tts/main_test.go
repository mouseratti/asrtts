package main

import (
	"testing"
)

func Test_getFileName(t *testing.T) {
	type args struct {
		directory string
	}
	tests := []struct {
		name string
		args args
		want string
	}{
		{"regular", args{"/tmp"}, "/tmp/1"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := getFileName(tt.args.directory); got != tt.want {
				t.Errorf("getFileName() = %v, want %v", got, tt.want)
			}
		})
	}
}
