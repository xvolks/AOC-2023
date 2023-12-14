# Day 5

This was the first day I have struggled to find a solution for part #2.

Part 1 was simple, and part 2 with the sample data was a no-brainer.

When I used the real data and saw no response in the few first seconds, 
I thought: there is a bug in my code that does not handle correctly the 
data (an infinite loop?).

So I've added a tqdm to the loop to see if the program advance over time,
and oh God, billions of iterations were awaiting.

I opened the text file (puzzle input) for the first time and realized that
the ranges to test were so huge that it was not possible to do it my way in
a reasonable time.

I went to Reddit to see if someone was talking about it and found that many did.

I saw the idea of as we search for the minimum location we just have to start with
location 0 and go backwards to see if we reach one of the input seed.

I've implemented that and after few minutes (05:02 on Mac M1) had the correct result, 
and won the 2nd star. On your data this may vary depending on the solution (here 59370572).

I'm still unsatisfied of this solution and will search something less 
bruteforce-ish. As I'm writing this, I still haven't tried yet.

Dec. 14. 
Ok, I finally got a working solution running very fast (no visible waiting).
There is still an off-by-one error (I guess), since I see ranges of 1 seed for a total of 143 ranges.
