const std = @import("std");
const cards = @import("cards.zig");
pub const Player = struct {
    id: u8,
    points: u8,
    hand: [6]cards.Card,
};

pub const Game = struct {
    winner: ?Player,
    deck: [52]cards.Card,
    deck_idx: u8,
    p1: Player,
    p2: Player,
    crib: [4]cards.Card,

    pub fn deal(self: *Game) void {
        for (0..12) |i| {
            if (i % 2 == 0) {
                self.p1.hand[i / 2] = self.get_card();
            } else {
                self.p2.hand[i / 2] = self.get_card();
            }
        }
    }

    fn get_card(self: *Game) cards.Card {
        const c = self.deck[self.deck_idx];
        self.deck_idx += 1;
        return c;
    }
};

pub fn init() !Game {
    return .{
        .winner = null,
        .deck = try cards.make_deck(),
        .deck_idx = 0,
        .p1 = std.mem.zeroes(Player),
        .p2 = std.mem.zeroes(Player),
        .crib = std.mem.zeroes([4]cards.Card),
    };
}
