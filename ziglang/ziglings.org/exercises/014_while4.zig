//
// You can force a loop to exit immediately with a "break" statement:
//
//     while (condition) : (continue expression) {
//
//         if (other condition) break;
//
//     }
//
// Continue expressions do NOT execute when a while loop stops
// because of a break!
//
const std = @import("std");

pub fn main() void {
    var n: u32 = 1;

    // Oh dear! This while loop will go forever?!
    // Please fix this so the print statement below gives the desired output.
    while (true) : (n += 1) {
<<<<<<< HEAD
        if (n == 4)
            break;
=======
        if (n == 4) break;
>>>>>>> f8453b2c24c5077a228fa24f7a1fa1cf30645918
    }

    // Result: we want n=4
    std.debug.print("n={}\n", .{n});
}
