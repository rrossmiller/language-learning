use std::{
    collections::HashMap,
    sync::{Arc, Mutex},
};

use bytes::Bytes;
use mini_redis::{Connection, Frame};
use tokio::{
    self,
    net::{TcpListener, TcpStream},
};

type Db = Arc<Mutex<HashMap<String, Bytes>>>;

#[tokio::main]
async fn main() {
    let port = "6379";
    let addr = format!("127.0.0.1:{}", port);
    // Bind the listener to the address
    let listener = TcpListener::bind(addr).await.unwrap();
    println!("Listening on :{port}");

    let db = Arc::new(Mutex::new(HashMap::new()));
    // The second item contains the IP and port of the new connection.
    loop {
        // A new task is spawned for each inbound socket. The socket is
        // moved to the new task and processed there.
        let (socket, _) = listener.accept().await.unwrap();
        // Clone the handle to the hash map.
        let db = db.clone();

        tokio::spawn(async move {
            process(socket, db).await;
        });
    }
}

async fn process(socket: TcpStream, db: Db) {
    use mini_redis::Command::{self, Get, Set};

    // A hashmap is used to store data
    let mut db = HashMap::new();

    // Connection, provided by `mini-redis`, handles parsing frames from
    // the socket
    let mut connection = Connection::new(socket);

    // Use `read_frame` to receive a command from the connection.
    while let Some(frame) = connection.read_frame().await.unwrap() {
        let response = match Command::from_frame(frame).unwrap() {
            Set(cmd) => {
                // The value is stored as `Vec<u8>`
                db.insert(cmd.key().to_string(), cmd.value().to_vec());
                Frame::Simple("OK".to_string())
            }
            Get(cmd) => {
                if let Some(value) = db.get(cmd.key()) {
                    // `Frame::Bulk` expects data to be of type `Bytes`. This
                    // type will be covered later in the tutorial. For now,
                    // `&Vec<u8>` is converted to `Bytes` using `into()`.
                    Frame::Bulk(value.clone().into())
                } else {
                    Frame::Null
                }
            }
            cmd => panic!("unimplemented {:?}", cmd),
        };

        // Write the response to the client
        connection.write_frame(&response).await.unwrap();
    }
}
