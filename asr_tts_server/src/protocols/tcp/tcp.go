package tcp

import (
	"Server"
	"bufio"
	"fmt"
	"net"
)

type tcpConnection struct {
	conn   net.Conn
}

func (this *tcpConnection) Read() Server.ClientMessage {
	r := bufio.NewScanner(this.conn)
	res, err := r.Scan()
	fmt.Println(res, err)
	return *new(Message)

}

func (this *tcpConnection) Write(message Server.ClientMessage) (error) {
	fmt.Println(message)
	_, err := this.conn.Write(make([]byte, 10))
	return err
}

func fromConn(conn net.Conn) Server.ClientConnection {
	return &tcpConnection{conn: conn}
}
