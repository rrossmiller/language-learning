use mini_grep::Config;
use std::{env, process};

fn main() {
    let args: Vec<String> = env::args().collect();
    let config = Config::new(&args).unwrap_or_else(|err| {
        eprintln!("Problem parsing args: {}", err);
        process::exit(1);
    });
    println!(
        "Searching for: \"{}\" in file {}",
        config.query, config.file_name
    );

    if let Err(e) = mini_grep::run(config) {
        eprintln!("App error: {}", e);
        process::exit(1);
    };
}
