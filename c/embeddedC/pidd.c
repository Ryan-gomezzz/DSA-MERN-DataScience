#include <stdio.h>
#include <unistd.h>

int main(void)
{
    pid_t pid = getpid();
    printf("Process ID: %d\n", pid);
    return 0;
}

// pid_t is a datatype defined in <unistd.h> that represents process IDs. The getpid() function retrieves the process ID of the calling process. In this code, we print the process ID to the console.


