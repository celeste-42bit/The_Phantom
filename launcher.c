#include <stdio.h>
#include <stdlib.h>

int main() {
    int status;

    // Run the Python script
    status = system("python3 -m app");

    // Check if the script ran successfully
    if (status == -1) {
        printf("Failed to launch the bot\n");
        return 1;
    }

    return 0;
}