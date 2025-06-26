#include <stdio.h>
#include <stdlib.h>
#include <string.h>


/*#define MAX_NAME_LENGTH 50
#define MAX_DESC_LENGTH 150

// Global variables
struct Task {
    char name[MAX_NAME_LENGTH];
    char description[MAX_DESC_LENGTH];
};*/




//additional functions


// 01 addTask function

void addTask() {
    
    //struct Task newTask;
    char name[50];
    char description[150];
    
    printf("Enter the name of the task: ");
    //scanf_s("%s", newTask.name, MAX_NAME_LENGTH);
    scanf("%s", name);
    
    printf("Enter task description: ");
    //scanf_s("%s", newTask.description, MAX_DESC_LENGTH);
    scanf("%s", description);
    
    
    
    FILE *file = fopen("tasks.txt", "r");
    if (file == NULL) {
        // File doesn't exist, create with header
        file = fopen("tasks.txt", "w");
        if (file == NULL) {
            printf("Error creating file!\n");
            return;
        }
        fprintf(file, "tasks :\n");
    } else {
        // File exists, close read mode and open in append mode
        fclose(file);
        file = fopen("tasks.txt", "a");
        if (file == NULL) {
            printf("Error opening file for appending!\n");
            return;
        }
    }
    //fprintf(file, "\nTask: %s, \nDescription: %s\n", newTask.name, newTask.description);
    fprintf(file, "\nTask: %s \nDescription: %s\n", name, description);
    fclose(file);
}


// 02 viewTasks function

void viewTasks() {
    FILE *file;
    file = fopen("tasks.txt", "r");
    if (file == NULL) {
        printf("No tasks found.\n");
        return;
    }

    char line[256];
    while (fgets(line, sizeof(line), file)) {
        printf("%s", line);
    }
    
    fclose(file);
 }





//main function

int main(){
    int zero;
    
    while (1)
    {
        printf("Enter 0 to open the task manager and 1 to exit program\n");
        scanf("%d", &zero);
        if (zero == 1) {
            break;
        }
        else if (zero == 0) {
            printf("Welcome to the Task Manager!\n");
            printf("You can add tasks, view tasks, and delete tasks.\n");
            printf("=========================================================\n");
            printf("type 'add' to add a task\n");
            printf("type 'view' to view all tasks\n");

            char command[10];
            
            scanf("%s", command);
            if (strcmp(command, "add") == 0) {
                addTask();
                printf("Task added successfully!\n");
            } 
            
            else if (strcmp(command, "view") == 0) {
                viewTasks();   
            }
            
            
            else {
                printf("Invalid command. Please try again.\n");
            }
    }
    }
    
    return 0;


 }




 