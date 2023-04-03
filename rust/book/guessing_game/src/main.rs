use rand::Rng;
use std::cmp::Ordering;

fn main() {
    let mut max = 100;
    println!("\nGuess the number");
    let secret = rand::thread_rng().gen_range(1..=max);
    println!("secret number: {}", secret);
    let mut guess = 50;
    let mut min = 0;
    for _ in 1..15 {
        println!("guess: {} | {}-{}", guess, min, max);

        match guess.cmp(&secret) {
            Ordering::Equal => {
                println!("Nice 👍");
                break;
            }
            Ordering::Less => {
                // guess between max and min
                min = guess;
                guess = (max + min) / 2;
            }
            Ordering::Greater => {
                max = guess;
                guess = (max + min) / 2;
            }
        }
    }
}
// // guessing game from the book
// fn main() {
//     println!("\nGuess the number");
//     let secret = rand::thread_rng().gen_range(1..=100);
//     // println!("The secret number is {}", secret);
//     loop {
//         println!("Enter your guess: ");
//         let mut guess = String::new();

//         io::stdin()
//             .read_line(&mut guess)
//             .expect("failed to read the line");
//         let guess: u32 = match guess.trim().parse() {
//             Ok(num) => num,
//             Err(_) => {
//                 println!("enter a number");
//                 continue;
//             }
//         };
//         println!("\nYou guessed {guess}");

//         match guess.cmp(&secret) {
//             Ordering::Equal => {
//                 println!("Nice 👍");
//                 break;
//             }
//             Ordering::Less => println!("too small"),
//             Ordering::Greater => println!("too big"),
//         }
//     }
// }
