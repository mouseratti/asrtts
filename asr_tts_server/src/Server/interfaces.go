package Server


type Socket interface {
	GetHost() Host
	GetPort() Port
	AsString() string
}

type Stream string

type Host string

type Port int64
