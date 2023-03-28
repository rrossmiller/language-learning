use rand::Rng;
use std::io;

// guessing game from the book
fn main() {
    println!("\nGuess the number");
    let secret = rand::thread_rng().gen_range(1..=100);
    println!("The secret number is {}", secret);

    println!("Enter your guess: ");
    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("failed to read the line");

    println!("\nYou guessed {guess}")
    // !bookmark
    // https://doc.rust-lang.org/book/ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
}
