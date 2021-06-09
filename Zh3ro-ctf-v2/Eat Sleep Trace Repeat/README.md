# Writeup for the Eat sleep Trace Repeat:
The file provided for the challenge was a simple text file named `trace.txt` 

Then I had the same reaction every reverse engineers would have when they see a txt file instead of a binary.

Still I proceeded to see the contents of the text file.

It was filled was `asm`.

A part of the contents of the file are:-

![text file contents](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr1.png)

Then I kinda looked at the numbering near the instructions these instructions all are not in order..And also my eye caught on something more the 
instructions are exactly in the order in which they are executed.. 

The first instruction in above image makes a `call to 0x401068` and the instruction is exactly the `0x401068 instruction`.

As I glanced on the text file ..Same set of instructions getting executed multiple times maybe there are some huge loops present....

I had really no idea to how to use work around to get the flags.

So I made a big brain frustating move `using the txt file to reconstruct the binary somehow`...

Guys I am telling you..This is always will be one of the decisions in my life that I would regret till the end of my days and I am little bit happy to as it one of the steps i used it to get the flag.

My first step to implement this idea was to write a python script to remove instructions being repeated and order these instructions in a ascending order.

So I wrote a python script called `unique.py` and pipe its output to file called `final.asm`.

![python_program](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr2.png)

![piping the output to asm](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr3.png)

But on sight seasoned veteran reverse engineers and asm programmers will know on sight that the above asm cannote be compiled to binary.

So I had to make a copy named `final2.asm`..Because I need to look on the original instructions and even if I make some mistakes..

The file called `final2.asm` is going to be the reconstructed binary where the `final.asm` is going to be the file I am going to use it for some lookups..

But there were some problems like  creating .data and .bss  section for binary.. 

Because the unintialized data which goes in .bss and and some initialized data which goes in .data section are not in perfect place..

![.data contents](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr6.png)
![read_bss_contents](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr4.png)
![some_more_bss](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr5.png)
![some_more_bss](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr7.png)

creating functions for `call instructions` and also jump labels for some `jump instructions`..
