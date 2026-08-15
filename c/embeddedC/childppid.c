#include<stdio.h>
#include<unistd.h>

int main(void)
{
    pid_t pid = fork();

    if(pid==0)
    {
        printf("I'm the child process");
        printf("Child ID %d \n",getpid());
        printf("Parent ID %d \n",getppid());
    }

    else if(pid>0)
    {
        printf("I'm the parent process");
        printf("Parent ID %d \n",getpid());
        printf("Child ID %d \n",pid);
    }

    else
    {
        printf("Fork failed");
    }

    return 0;
}