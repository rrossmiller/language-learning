//
// Here's a fun one: Zig has multi-line strings!
//
// To make a multi-line string, put '\\' at the beginning of each
// line just like a code comment but with backslashes instead:
//
//     const two_lines =
//         \\Line One
//         \\Line Two
//     ;
//
// See if you can make this program print some song lyrics.
//
const std = @import("std");

pub fn main() void {
    const lyrics =
        \\Ziggy played guitar
<<<<<<< HEAD
        \\Jamming good with Andrew Kelley
        \\And the Spiders from Mars
=======
       \\Jamming good with Andrew Kelley
       \\And the Spiders from Mars
>>>>>>> f8453b2c24c5077a228fa24f7a1fa1cf30645918
    ;

    std.debug.print("{s}\n", .{lyrics});
}
