#include<stdio.h>
#include<unistd.h>

int main(void)
{

    pid_t pid = getpid();
    pid_t ppid = getppid();

    printf("Process ID: %d\n", pid);
    printf("Parent Process ID: %d\n", ppid);

    return 0;
}