const std = @import("std");
const cards = @import("cards.zig");
const cribbage = @import("game.zig");

pub fn main() !void {
    const stdout_file = std.io.getStdOut().writer();
    var bw = std.io.bufferedWriter(stdout_file);
    const stdout = bw.writer();

    try stdout.print("\nDealing...\n", .{});
    try stdout.print("********************************************************************************************************\n", .{});
    var game = try cribbage.init();
    // try stdout.print("{}\n", .{game});
    while (game.winner == null) {
        // deal
        game.deal();
        stdout.print("p1 discard\n", args: anytype)
        try print_cards(&game.p1.hand);
        try print_cards(&game.p2.hand);
        // discard
        // count
        // score
        game.winner = game.p1;
    }
    // report winner
    try stdout.print("Winner: {?}\n", .{game.winner.?.id});
    try bw.flush();
}

fn print_cards(hand: []cards.Card) !void {
    const stdout_file = std.io.getStdOut().writer();
    var bw = std.io.bufferedWriter(stdout_file);
    const stdout = bw.writer();
    try stdout.print("\n", .{});
    for (hand) |c| {
        try stdout.print("{}\n", .{c});
    }
    try bw.flush();
}

// fn show_cards(deck: [52]cards.Card) void {
//     for (deck, 0..) |d, i| {
//         std.debug.print("{}\n", .{d});
//         if (i >= 10) {
//             break;
//         }
//     }
//     std.debug.print("{}\n", .{deck[deck.len - 1]});
// }
