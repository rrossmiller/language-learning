use std::{
    io::{self, Write},
    time::Instant,
};

fn main() {
    // fib seq

    // get max number from user
    let user_in = if false {
        let mut user_in = String::new();
        println!();
        print!("Enter the max index: ");
        io::stdout().flush().expect("Flush didn't work");
        io::stdin()
            .read_line(&mut user_in)
            .expect("failed to read the line");

        let user_in: i32 = match user_in.trim().parse() {
            Ok(num) => num,
            Err(_) => {
                panic!("Please enter a number")
            }
        };
        println!();
        user_in
    } else {
        45
    };

    let start = Instant::now();
    let res = fib(user_in);
    let duration = Instant::now() - start;

    println!("{}", user_in);
    for (i, v) in res.iter().enumerate() {
        println!("{}: {}", i, v)
    }
    println!("elapsed {}µs", duration.as_micros());
    // println!("elapsed {}ns", duration.as_nanos());
}

fn fib(max_idx: i32) -> Vec<i64> {
    let mut rtn = vec![0, 1];
    for i in 2..max_idx {
        let x = rtn[i as usize - 2] + rtn[i as usize - 1];
        rtn.push(x);
    }
    rtn
}
