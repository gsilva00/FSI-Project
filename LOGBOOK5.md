# SEED Labs Tasks for _Buffer-Overflow Attack Lab - Set-UID Version_

## General Information
In this week, we learnt how to use a buffer-overflow vulnerability to conclude an attack which would start a shell during the execution of our program. Ultimately, we obtained knowledge in attacking using C, pyhon and assembly language in either 32bit or 64bit shellcode.

## (Work done in Week #5)

## Task1: Getting Familiar with Shellcode
In the first task, we had to understand how to lauch the shell using a `C shellcode` by transmitting our command using `execve()`.

```sh
int main() {
  char *name[2];
  name[0] = "/bin/sh";
  name[1] = NULL;
  execve(name[0], name, NULL);  //restarts process with shell launched
}
```

If we executed the previous code, we secure a shell interface, where we can write our commands. For instance, ls, pwd, etc.

But since the system doesn't understand C code transformed in binary when trying to follow commands on the stack, basically this code won't work as a shellcode.

Instead we need to insert assembly code into the memory so that the program instructions understand the exploit and lauches the shell in the stack.

One of the ways we can do that is by using the code provided by the guidelines in the last step of the task.

```sh
 ...
 strcpy(code,shellcode);  //Copy the shellcode to the stack
 int(*func)()=(int(*)())code;
 func();  //Invoke the shellcode from the stack
 ...
```

The shellcode being dependent on the type of bit the program is using:
> note: this code will be helpfull in the following tasks.
#if__x86_64__
"\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e" 
"\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57"
"\x48\x89\xe6\x48\x31\xc0\xb0\x3b\x0f\x05"
#else
"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f"
"\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31"
"\xd2\x31\xc0\xb0\x0b\xcd\x80"
#endif

If we compile `call shellcode.c` using `make`, two versions of binary files will be available to execute: `a32.out` (32-bit) and `a64.out` (64-bit). Afterwards, choosing either one of them to compile, will run a shell interface and we will be able to interact with it using shell commands.

<img src="images/LOGBOOK5/task1_image.png" width="400" alt="printenv"/>

>note: Makefile compiles the program with `execstack` option, allowing our code to be executed from the stack. Otherwise, the exploit would've failed.

## Task2: Understanding the Vulnerable Program
In the second task, we are asked to exploit a buffer-overflow vulnerability. To successed in this task, we are given `stack.c`, where a big buffer gets its contents copied to a smaller size buffer with no restrictions of neither inputs nor content size. In other words, `strcpy()` doesn't check if `BUF SIZE` is bigger than the content capacity, leading to overflow of string (or possibly malicious code) to a restricted area of the stack.

Moreover, the file `stack.c` accepts a file named `badfile` to fill the contents of the original buffer of `517 Bytes`. Therefore, if we fill badfile with malicious code, we are able to exploit the system, hence obtaining a shell interface.

This is how the vulnerability works in `stack.c`:
```sh
char str[517];
char buffer[BUF_SIZE]; /*size depending on the group number. Since we are G02, then BUF_SIZE = 100 + 8*2  */
FILE *badfile;
badfile = fopen("badfile", "r");
fread(str, sizeof(char), 517, badfile);
strcpy(buffer, str);  //vulnerability here
```

Compilation of `stack.c` requires both the StackGuard and the non-executable stack protections to be turned off. Besides, this program must be a root-owned Set-UID program. Luckily, `Makefile` already does the work for us.

## Task3: Launching Attack on 32-bit Program (Level 1)
To make sure our exploit works, first we need to adquire certain addresses. In particular, the `buffer’s starting position` and `return-address position` are essential to obtain the difference between them. Debugging the code using the `-g` flag while compiling, will shows us those addresses.

After doing the steps shown:
```sh
$ touch badfile    //Create an empty badfile
$ gdb stack-L1-dbg
gdb-peda$ b bof    //Set a break point at function bof()
gdb-peda$ run      // Start executing the program
gdb-peda$ next
gdb-peda$ p $ebp
gdb-peda$ p &buffer
gdb-peda$ quit
```
We got `buffer’s starting position` and `return-address position`:

<img src="images/LOGBOOK5/task3_image.jpg" width="250" alt="printenv"/>

#### buffer’s starting position= 0xffffcae8
#### return-address position = 0xffffca7c

>note1: the command `next` is relevant to get the ebp register with the current stack frame. Without it, we would obtain the caller's ebp value, since gdb stops right before ebp changes value.

>note2: the frame pointer value differs executed normally or in gdb. This is due to gdb pushing some environment data into the
stack before running the debugged program. Consequently, executing normally will result in a larger frame pointer value.

Done adquiring the addresses, we had to prepare a python script named `exploit.py` to convert our shellcode in binary and write it inside badfile. 

To understand how should we attack the system, lets first summarize how the memory looks like after the buffer overflows:

```sh
  +-----------------------+  <-- Higher Memory Address
  |   Data not affected    |  
  +-----------------------+
  | Data affected by       |  <-- Overflow reaches this point
  | overflow               |
  +-----------------------+
  | Return Address         |  <-- Return address overwritten
  +-----------------------+
  | EBP (Base Pointer)     |  <-- EBP can be overwritten by overflow
  +-----------------------+
  | Buffer                 |  <-- Buffer where data is stored
  +-----------------------+
  | ...                    |
  | Stack continues        |
  +-----------------------+  <-- Lower Memory Address
```
The steps to prepare the attack are the following:
1) Need to put our shellcode above the stack.
2) Define where the return address should point to execute the shellcode.

#### 1) Need to put our shellcode above the stack
We tried using the 32 bit exploit. For that, we substituted empty shellcode for code from the first task. Of course, 64 bit would still work, however the code would need few tweeks to run properly.

<img src="images/LOGBOOK5/task3_image2.png" width="400" alt="printenv"/>

We chose to place our code in the data area where overflow will happen. In this case, 200 seemed feasible since our vulnerable buffer had less than 150 Bytes.

The rest of the buffer will have NOP's to redirect memory towards shellcode execution.

#### 2) Define where the return address should point to execute the shellcode

For this step, we had to find an address where, if the return address gets executed, then it needs to be able to find the shellcode. We know that return address is above ebp, and that anything above that is outside stack, so using ebp to find a suitable place is helpful. The addition of start made a possible return address.

On the other hand, we also had to find the address of the return address, so we could modify it with the above information when filling the buffer. Taking a look at the memory image, we can see that return address is above ebp, in particular, 4 bytes above ebp. Knowing that the buffer starts at 0xffffca7c, then return address should be located in a distance of `ebp - buffer address + 4` from the beggining of the buffer.

>note: (ebp - buffer address) indicates the buffer content to skip over the stack data, going directly to where the ebp is located.

<img src="images/LOGBOOK5/task3_image3.png" width="400" alt="printenv"/>

### Executing the code
Executing the compilation and run commands, we finally get a shell interface. Ultimately, we can now further compromise the system >:)

<img src="images/LOGBOOK5/task3_image4.png" width="300" alt="printenv"/>

## Question 2: Memory Region
Completed the exploit, it is important to understand how the buffer looks like in detail, in particular, the correlation between the shellcode start address and the return address.

Debugging the program, we see that the NOPs start around the address 0xffffcf13.

<img src="images/LOGBOOK5/question2_image1.png" width="300" alt="printenv"/>

And the shellcode is a bit further up.

<img src="images/LOGBOOK5/question2_image3.png" width="300" alt="printenv"/>

On the other hand, the return address can be found lower, close to the start of the buffer. It points to the start of the NOPs, leading to the execution of the shellcode.

<img src="images/LOGBOOK5/question2_image2.png" width="300" alt="printenv"/>

We can find the return address by making the calculations of the offset:

```sh
.----------------------------------.
|Hexadecimal          | Decimal    |
|ebp = 0xffffcae8     | 4294953704 |
|buffer = 0xffffca7c  | 4294953596 |
.----------------------------------.
ebp - buffer = 108 (decimal)
ebp - buffer + 4 = 112 (decimal)
buffer[112] = 4 294 953 708 + 4 = 4 294 953 712 (decimal)

4 294 953 712 = 0xffffcaf0
```