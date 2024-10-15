# Lab Tasks for _Environment Variable and Set-UID_
## Task 1: Manipulating Environment Variables
In the first exercise of the week, we were asked to understand how environment variables work, in particular, to print, export and unset variables. 

For this process, we are using `printenv` to print the current environment variables in the default shell, set in the /etc/passwd file. The beginning of the print will look similar to the following image:

![image of printenv](images/LOGBOOK4/task1-image-printenv.png){width=400}

Now to export and unset an environment variable, we chose to create a new variable called `VARIAVEL` with content as `Ola`. We conclude, after an environment variable is unset, all its content will disappear. Besides, we can't unset an important environment variable, such as PATH. 

![image of export](images/LOGBOOK4/task1-image.png){width=350}

## Task 2: Passing Environment Variables from Parent Process to Child Process
On this task, we will understand how `fork()` will influence environment variables. We executed the code provide in the guidelines, and see what are the diferences if we execute `printenv();` whether in the child or parent process.

![image_of_converting_to_file](images/LOGBOOK4/task2_-image.png){width=300}

Saving both files and compared their content using `diff` (using website diff only to enhance the diferences), we concluded that the files are the same. Hence, the environment variables are copied when we call a new process. The reason behind this is due to parent process making a copy of the adress space for the child. After the child continues the process, it can change environment variables without modifying the parent adress space.

![image_of_dif_between_files](images/LOGBOOK4/task2-image2.png){width=400}

## Task 3: Environment Variables and _execve()_
We learnt that copying a new process using `fork()` will maintain the environment variables. Nevertheless, the execve() will not have a similar inheritance. To prove this fact, we will compile and run the the given code in the guidelines twice. However the first version will have `execve("/usr/bin/env", argv, NULL);` and the last one `execve("/usr/bin/env", argv, environ);`.

![image_of_compiling_programs](images/LOGBOOK4/task3_image.png){width=300}

Making `diff` between the two files (using online diff to have diferences visible), we noticed that the first file will be empty, whereas the second fills the page with environment variables as if `printenv` was executed.

![image_of_task3_2](images/LOGBOOK4/task3_image2.png){width=400}

The difference resides in the last parameter change `NULL -> environ`. The last parameter of `execv()` is `char *const envp[]`, which is a char vector containning the environment variables that we want to pass to the new program running in the current process.

In the first code example, the execve ran code without no environment variables due to NULL, leading to the failure of execution, and, thus, printing no text.

In the other hand, environ passed all the variables before running /usr/bin/env which made it possible to print the environment variables correctly.

## Task 4:  Environment Variables and _system()_
Conversly, `system()` function does not require aditional arguments to acquire the environment variables since its internal process uses a temporary fork() to obtain them from the parent process. Additionally, during the fork(), the function does `/bin/sh -c command` through `execl()`, being able to run advanced shell resources and sequential lines of commands.

The capability of `system()` is visible by running the following code:

```sh
#include <stdio.h>
#include <stdlib.h>

int main(){
  system("/usr/bin/env");
  return 0 ;
}
```

As foreseeable, we obtained the environment variables of the above code:

```sh
GJS_DEBUG_TOPICS=JS ERROR;JS LOG
LESSOPEN=| /usr/bin/lesspipe %s
USER=seed
SSH_AGENT_PID=2183
XDG_SESSION_TYPE=x11
SHLVL=1
HOME=/home/seed
OLDPWD=/home/seed/Documents
DESKTOP_SESSION=ubuntu
...
```

> Note: Since `system()` returns to the parent's process, any code written below the system function will be executed, whereas in `execve()`, the remaining code would be erased by the new command. This could be detrimental for execve(), when choosing which one of the functions to apply on our code.

## Task 5: Environment Variable and Set-UID Programs
To establish a better understanding of the shell powers, mainly executing with root privileges, we saw how a Set-UID program runs.

The code we compiled named ver_en_var prints the environment variables which are passed through the shell:  
```sh
#include <stdio.h>
#include <stdlib.h>
extern char **environ;
int main(){
  int i = 0;
  while (environ[i] != NULL) {
    printf("%s\n", environ[i]);
  i++;
  }
}
```
Then, we change its ownership to root and transformed it to a Set-UID program:
```sh
sudo chown root ver_en_var
sudo chmod 4755 ver_en_var
```

Besides, we altered some of the environment variables to verify if they were visible during execution:

- PATH: added "/meu/novo/caminho"
- LD_LIBRARY_PATH: altered to "/minha/biblioteca"
- ANY_PATH_NAME: constructed "/meu/diretorio/personalizado"

When we run the program, we confirmed that some environment variables were visible, such as: 

```sh
...
ANY_PATH_NAME=/meu/diretorio/personalizado
...
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:.:/meu/novo/caminho
...
```

However, `LD_LIBRARY_PATH` was not shown on the obtained file. Searching in depth on the root of the problem, it is likely that the system deemed our code vulnerable to exploitation by having access to the variable `LD_LIBRARY_PATH`. Of course, if we ran this code in no higher privileges than the normal user, then that variable exposed would not be relevant, as we would not have enough permissions to do any successfull attack.

## Task 6: Manipulating Environment Variables
For the next task, we had to gather all the above information to run our own malicious code. The following steps detail the procedure to accomplish it:

1. We created a file named `ls_relative.c`:

```sh
int main(){
  system("ls");
  return 0;
}
```
2. Besides, we inserted our malicious code ,`ls.c`, in a seperate folder for accessability: `home/seed/Documents/HAKERSCRIPTS`
```sh
#include <stdio.h>

int main(){
  printf("olá! Queres um presente?");
}
```

3. We compiled both programs, and transformed the `ls_relative` exectutable file into a Set-UID program.
```sh
sudo chown root ls_relative
sudo chmod 4755 ls_relative
```

4. Then we had to prepare our PATH environment variable by changing the priority of where the system tries find the `ls` program. This is possible by adding our malicious directory before $PATH. Afterwards, if we try to execute the command ls or ./ls_relative, our malicious code will be processed.

![](images/LOGBOOK4/hackerscript.png){width=400}

> Notes: If we try executing ls in /bin/sh program, it won´t work as /bin/dash will deactivate the root privileges, and, thus stop the execution of our code. Before step 4, it is necessary to link /bin/sh to /bin/zsh: `sudo ln-sf /bin/zsh /bin/sh` and then `zsh`

## Task 8: Invoking External Programs Using _system()_ versus _execve()_
According to the observations of Task4, we already know that the use of `execl()` inside the `system()` function deliberatly permits sequential commands to be written as one whole argument on the function. This is due to the shell feature of processing multiple commands using `;` to distinguish where each command ends.

An example of this would be:
![image_of_shell_commands](images/LOGBOOK4/shell_commands.png){width=350}

If we were Bob, we could take advantage of this vulnerabilty, and try to remove any file we wanted, including files that otherwise we did not have permissions to write. The reason that it is possible to achieve this is due to transforming `catall` as a Set-UID program. In other words, although us, mere users, have no permissions to write files, the program, in the other hand, has the same privileges as the root, that is, it has permissions to read/write/execute any file available. As a consequence, using the program to remove the files for us is feasible, no matter how sure Vince is.

For instance, we could run the following command:

```sh
./catall um_ficheiro_pouco_interessante; rm -f /path/do/ficheiro/muito_interessante
```
Or even be more destructive by:
```sh
./catall um_ficheiro_pouco_interessante; rm -r ~/*
```
This would lead to the deletion of all files and directories Vince would have in the system, compromising its integrity.

Nevertheless, if we had `execve()`, instead of system(), our exploit ought to not work, even if we compiled and executed as a Set-UID program.

Execve() can only replace the address space of the current program once, which means, it only executes the first command and ignores the rest of the string. Since `/bin/cat` only has one argument, then it captures the first input of the user, being probably the file name. After program captures a viable command, the program starts the process from zero, executing cat filename. The rest of the string, `; rm ~/*`, would be erased from the memory. Hence, no effects would be felt in the system.

In summary, having `catall.c` with `system(command)` is vital for our exploit in Vince's system.


