package Server

type ConnectionHandler interface {
	Handle(Connection)
}

type Server interface {
	Listen(Socket)
}

type Socket interface {
	GetHost() Host
	GetPort() Port
	Pass()
}

type Stream string

type Host string

type Port int64
