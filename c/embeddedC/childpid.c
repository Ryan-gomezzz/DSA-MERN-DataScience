#include<stdio.h>
#include<unistd.h>

int main(void)
{
    pid_t pif = fork();

    if (pif < 0) {
        printf("Fork failed.\n");
        return 1;
    } else if (pif == 0) {
        // Child process
        printf("Child Process ID: %d\n", getpid());
    } else {
        // Parent process
        printf("Parent Process ID: %d\n", getpid());
    }

    return 0;
}