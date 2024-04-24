import gleam/int
import gleam/io
import gleam/list
import gleam/otp/task

fn spawn(i) {
  task.async(fn() {
    let n = int.to_string(i)
    io.println("Hello from " <> n)
  })
}

pub fn main() {
  list.range(0, 200_000)
  |> list.map(spawn)
  |> list.each(task.await_forever)
}
