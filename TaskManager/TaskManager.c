#include <stdio.h>
#include <stdlib.h>
#include <string.h>


//additional functions

// // //
void clearInputBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}
void stripNewline(char *str) {
    size_t len = strlen(str);
    if (len > 0 && str[len - 1] == '\n') {
        str[len - 1] = '\0';
    }
}


// 01 addTask function

void addTask() {
    
    
    char name[50];
    char description[150];
    
    clearInputBuffer();
    printf("Enter the name of the task: ");
    if (fgets(name, sizeof(name), stdin) == NULL) {
        printf("Error reading task name!\n");
        return;
    }
    //fgets(name, sizeof(name), stdin);
    stripNewline(name); // Remove newline character from the end of the string
    
    clearInputBuffer();
    printf("Enter task description: ");
    if (fgets(description, sizeof(description), stdin) == NULL) {
        printf("Error reading task description!\n");
        return;
    }
    //fgets(description, sizeof(description), stdin);
    stripNewline(description); // Remove newline character from the end of the string
    
    
    FILE *file = fopen("tasks.txt", "r");
    if (file == NULL) {
        // File doesn't exist, create with header
        file = fopen("tasks.txt", "w");
        if (file == NULL) {
            printf("Error creating file!\n");
            return;
        }
        fprintf(file, "TASKS :\n\n");
    } else {
        // File exists, close read mode and open in append mode
        fclose(file);
        file = fopen("tasks.txt", "a");
        if (file == NULL) {
            printf("Error opening file for appending!\n");
            return;
        }
    }
    
    fprintf(file, "...Task: %s\n       .Description: %s\n", name, description);
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
        printf("\nEnter 0 to open the task manager and 1 to exit program\n");
        if (scanf("%d", &zero) != 1) {
            printf("Invalid input. Please enter 0 or 1.\n");
            clearInputBuffer();
            continue;
        }
        
        
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
            clearInputBuffer();
            printf("Enter command: ");
            if (fgets(command, sizeof(command), stdin) == NULL) {
                printf("Error reading command!\n");
                continue;
            }
            stripNewline(command);
            
            
            if (strcmp(command, "add") == 0) {
                addTask();
                printf("Task added successfully!\n");
            } 
            
            else if (strcmp(command, "view") == 0) {
                viewTasks();   
            }
            
            
            else {
                printf("Invalid command. Please try again.\n");
                clearInputBuffer();
            }
    }
    }
    
    return 0;


 }




 