#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//additional functions
void addTask (int i);




//main function

int main(){
    int zero;
    int taskCount = 0;
    printf("Enter 0 to open the task manager and 1 to exit program\n");
    scanf("%d", &zero);
    if (zero == 1) {
        return 0;
    }
    elseif (zero == 0) {
        printf("Welcome to the Task Manager!\n");
        printf("You can add tasks, view tasks, and delete tasks.\n");
        printf("=========================================================\n");
        printf("type 'add' to add a task\n");

        char command[10];
        scanf("%s", command);
        if (strcmp(command, "add") == 0) {
            int i = 0;
            addTask(taskCount);
            taskCount++;
            printf("Task added successfully!\n");
        } else {
            printf("Invalid command. Please try again.\n");
        }
    }
    return 0;


 }