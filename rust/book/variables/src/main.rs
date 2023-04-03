fn main() {
    let x = 5;
    let x = x + 1;
    {
        let x = x + 1;
        println!("x: {x}");
    }
    println!("x: {x}");

    let tup = ('a', 1.891, x);
    println!("{} {} {}", tup.0, tup.1, tup.2);

    let (_, f, _) = tup;
    println!("The val of the float in tuple is {f}");
    println!();

    let a: [i32; 4] = [1, 2, 3, 45];
    println!("{:?}", a);
    let a = [0;5];
     println!("{:?}", a);
     println!("{:?}", a[1]);
}
