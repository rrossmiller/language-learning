use mini_redis::{client, Result};

async fn hi() {
    println!("hi");
}
#[tokio::main]
async fn main() -> Result<()> {
    // Open a connection to the mini-redis address.
    let mut client = client::connect("127.0.0.1:6379").await?;

    // Set the key "hello" with value "world"
    client.set("hello", "world".into()).await?;

    // Get key "hello"
    let result = client.get("hello").await?;
    if let Some(r) = result {
        println!("got value from the server;\nresult={:?}", r);
    }

    let op = hi();
    println!("hello");
    op.await;
    Ok(())
}
