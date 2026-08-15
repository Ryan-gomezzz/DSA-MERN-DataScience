#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void)
{
    pid_t pid = fork();

    if (pid == 0)
    {
        // Child process
        printf("Child is running\n");
        printf("Child PID: %d\n", getpid());
    }
    else if (pid > 0)
    {
        // Parent waits until child finishes
        wait(NULL);

        printf("Child finished execution\n");
        printf("Parent continues\n");
    }
    else
    {
        printf("Fork failed\n");
    }

    return 0;
}