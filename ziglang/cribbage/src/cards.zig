const std = @import("std");
const expect = @import("std").testing.expect;

const Suit = enum {
    Spades,
    Clubs,
    Heart,
    Diamond,
};

const Val = enum(u8) {
    Ace,
    Two,
    Three,
    Four,
    Five,
    Six,
    Seven,
    Eight,
    Nine,
    Ten,
    Jack,
    Queen,
    King,

    pub fn get_val(self: Val) u8 {
        switch (self) {
            .Ten, .Jack, .Queen, .King => return 10,
            else => return @intFromEnum(self) + 1,
        }
    }
};

pub const Card = struct {
    suit: Suit,
    val: Val,
};

pub fn make_deck() ![52]Card {
    var prng = std.rand.DefaultPrng.init(blk: {
        var seed: u64 = undefined;
        try std.posix.getrandom(std.mem.asBytes(&seed));
        break :blk seed;
    });
    const r = prng.random();

    var deck = std.mem.zeroes([52]Card);
    var i: u8 = 0;
    for ([4]Suit{ Suit.Spades, Suit.Clubs, Suit.Heart, Suit.Diamond }) |suit| {
        for ([13]Val{ .Ace, .Two, .Three, .Four, .Five, .Six, .Seven, .Eight, .Nine, .Ten, .Jack, .Queen, .King }) |val| {
            deck[i] = Card{ .suit = suit, .val = val };
            i += 1;
        }
    }

    std.Random.shuffle(r, Card, &deck);
    return deck;
}

// ------------------------------------------------------------------------------------------------
test "Test Vals" {
    const vals = [13]Val{ .Ace, .Two, .Three, .Four, .Five, .Six, .Seven, .Eight, .Nine, .Ten, .Jack, .Queen, .King };
    const nums = [_]u8{ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10 };
    for (vals, nums) |v, n| {
        // std.log.warn("\n{}: {} {}", .{ v, v.get_val(), n });
        try expect(v.get_val() == n);
    }
}

test "Test Make Deck" {
    var deck = std.mem.zeroes([52]Card);
    const zero_card = Card{ .suit = Suit.Spades, .val = Val.Ace };
    for (deck) |c| {
        try expect(std.meta.eql(zero_card, c));
    }

    var i: u8 = 0;
    deck = make_deck();
    for ([4]Suit{ Suit.Spades, Suit.Clubs, Suit.Heart, Suit.Diamond }) |suit| {
        for ([13]Val{ .Ace, .Two, .Three, .Four, .Five, .Six, .Seven, .Eight, .Nine, .Ten, .Jack, .Queen, .King }) |val| {
            const c = Card{ .suit = suit, .val = val };
            try expect(std.meta.eql(deck[i], c));
            i += 1;
        }
    }
}
