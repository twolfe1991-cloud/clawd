.[] | 
select(.text | test("(?i)mog|keycat|kta|rei|virtual|tibbir")) |
.text as $text |
(
    if ($text | contains("$MOG")) then "MOG"
    elif ($text | contains("$KEYCAT")) then "KEYCAT"
    elif ($text | contains("$KTA")) then "KTA"
    elif ($text | contains("$REI")) then "REI"
    elif ($text | contains("$TIBBIR")) then "TIBBIR"
    elif ($text | test("Virtuals"; "i")) then "VIRTUAL"
    elif ($text | test("tibbir"; "i")) then "TIBBIR"
    else empty end
) as $token |
"\(.createdAt)|\(.author.username)|\(.likeCount)|\(.id)|\($token)|\(.text)"
