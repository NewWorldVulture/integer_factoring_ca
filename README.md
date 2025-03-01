Literally just uploading this to show i did it :p
https://x.com/IoOrBust/status/1371440605759373315

It's a cellular automata that factors integers. You need to run it first to figure out how many generations it takes to factor it, and to see how many columns you need, because PIL needs to know in advance, as far as I knew in 2021. I will not be updating this again, probably. This is the code as it existed in 2021 when I posted the tweet. After that, I got very burnt out on programming for several years. The code exists as-is, completely unmaintainable. lmao

It takes a "command" in the form `FXXXX`. It then copies the number, and initializes a set of columns, D, that will be iterating from 1 to `XXXX`. At this point, the tape looks like `XXXXcXXXX.DDDDf`. For example, `0110c0110.0001f`.

Quite a lot of the machinery in the cellular automata is just responsible for the initialization described above. I could've saved something like 15 states by requiring the initial tape to be the above.


The CA then subtracts `DDDD` from the second copy of `XXXX`, producing `SSSS`. Then the CA checks if `SSSS` is greater than zero. All it does is check if it runs into a `1` anywhere in `XXXX`. If it's greater than 0, it subtracts `DDDD` again. When it subtracts, if it attempts to borrow from the `c` column (meaning that `DDDD` is greater than `SSSS`), it errors out (purple) and it knows that `XXXX` is not divisible by `DDDD`.

If `XXXX` is divisible by `DDDD`, it sends a message to copy `DDDD` over to the factors. While it does this, it writes over `SSSS` with `XXXX` again. Tape is now `XXXXcXXXX.DDDDfDDDD`. Whether it copies it or not, it then adds 1 to DDDD. It repeats this process until `DDDD` is equal to `XXXX`

Backing up to subtraction, after a copy is triggered, if the first subtraction performed brings `SSSS` to zero (meaning that `DDDD` is equal to `XXXX`, it immediately copies `DDDD` to the factors columns, and wipes all the colums to the left of `f`, only leaving the factors behind.

It's been long enough that I'd need to spend days to understand the specifics of this, but I stand by this tweet:
![image](https://github.com/user-attachments/assets/f556738c-fc60-4fba-9bf6-ff6fed3ae7ef)
