# Writeup for the Eat Sleep Trace Repeat:

![chall description](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr_description.png)

The file provided for the challenge was a simple text file named `trace.txt` 

Then I had the same reaction every reverse engineers would have when they see a txt file instead of a binary.

Still I proceeded to see the contents of the text file.

It was filled with `asm`.

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
![place for bin operations](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr5.png)
![some_data](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr7.png)

There is a problem from the asm extracted the read contents and the place where some binary stores some values from the result of first loop falls before .data section..(.data comes after .bss)

But we all know in general that in ELF binaries .bss comes after .data section..

The above first image prints enter password which is below the place where there are some values stored after the first loop executes which can be seen in third image and also below the place where the user input also stored this can be seen in second image and in the fourth image some data to print after some validation.

How I found it is enter password for the first write is the challenge description and the second input could be search complete..

But during the time of CTF.. I totally forgot about the search complete string instead in my `final2.asm` you will find a huge array of nulls 

Just not to over complicate more I went on to a huge .data section with nulls at the beginning and then the string enter password at the middle and then some nulls again as I had no idea that time that the string search complete will be there instead of that I placed huge number of nulls..

Then I had to create function labels and jump point labels for the `call insctructions` and `jmp instructions`.

And finally pray to god that no more errors should appear while compiling the asm to binary..

![compiled successfully](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr8.png)

Voila!!We have successfully created the binary after so many hardships..We see no errors on the above image..The strace shows that our binary works perfectly..

The final write prints 16 nulls to stdout which is fine because I already told about the search complete string I missed which is replaced there with some nulls..

Okk let's pop up our gdb..And start reversing this binary..

The first loops executes and puts the data calculated into our null initialized .data section.

![loop instructions](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr9.png)

The above image is from file `final2.asm` which consists of the loop instructions that perform some byte operations and stores in the .data from 0x402008
to 0x4027f8.

![data section bytes](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr10.png)

These are the values from the byte operations the next loop kinda iterates our input to the values from the byte operations and there is nothing more..

If the compared input is same with the value from the byte operations it stores the value in the memory using the instruction `mov byte  [rsi+0x40286c], al`

After scratching my head for a long time ..Suddenly like a bolt from the blue an idea suddenly struck in my mind..

The idea that struck in my mind is they give a trace right..There should be a person who could have entered the password and that trace of instructions of how the value  compared must have been present here.

The plan is to know the amount of how many times in the second loop a single character is getting compared with.. Because in this way the instructions after the compare will be the breaking point and the compare instruction will determine the number of times before the breaking instruction hits ..In this case the breaking instruction here is `dec rdx`.

![compare_instructions](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr11.png)

So I wrote a python program  `tracer.py` to parse the `trace.txt` to print the number of times for single character..

![tracer.py](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr12.png)

![py output 1](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr13.png)

![py output 2](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr14.png)

Just for start in python program I gave the loop ending as 60 characters..But the flag only has 49 characters after 49 characters others are bogus..

By this `tracer.py` I found out the number of times the compare instructions takes place before the `dec rdx`.So the next work is to find the characters from 0x402008+number_of_times_compare_took_place 

I could have automated this ..But I went for a dumb idea which is this..

![flag](https://github.com/team-ssod/Reverse-Engineering-Writeups/blob/main/Zh3ro-ctf-v2/Eat%20Sleep%20Trace%20Repeat/images/estr15.png)

After doing this repeatedly for 49 characters we end up with the flag:-

## zh3r0{d1d_y0u_enjoyed_r3v3rs1ng_w1th0ut_b1n4ry_?}

