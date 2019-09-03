package Server

import "net"

type Connection interface {
	net.Conn
}

type TcpConnection int64

//func (this *TcpConnection) Read() Stream  {
//	return nil
//}

func from() TcpConnection {
	return TcpConnection(1)
}
