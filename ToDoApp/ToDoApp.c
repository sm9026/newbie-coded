#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// additional functions

// // //
void clearInputBuffer()
{
    int c;
    while ((c = getchar()) != '\n' && c != EOF)
        ;
}
void stripNewline(char *str)
{
    size_t len = strlen(str);
    if (len > 0 && str[len - 1] == '\n')
    {
        str[len - 1] = '\0';
    }
}

int l; // declare taskCount globally

// 01 addTask function

void addTask()
{

    char name[50];
    char description[150];

    clearInputBuffer();
    printf("Enter the name of the task: ");
    if (fgets(name, sizeof(name), stdin) == NULL)
    {
        printf("Error reading task name!\n");
        return;
    }
    // fgets(name, sizeof(name), stdin);
    stripNewline(name); // Remove newline character from the end of the string

    clearInputBuffer();
    printf("Enter task description: ");
    if (fgets(description, sizeof(description), stdin) == NULL)
    {
        printf("Error reading task description!\n");
        return;
    }
    // fgets(description, sizeof(description), stdin);
    stripNewline(description); // Remove newline character from the end of the string

    FILE *file = fopen("tasks.txt", "r");
    if (file == NULL)
    {
        // File doesn't exist, create with header
        file = fopen("tasks.txt", "w");
        if (file == NULL)
        {
            printf("Error creating file!\n");
            return;
        }
        fprintf(file, "TASKS :\n");
    }
    else
    {
        // File exists, close read mode and open in append mode
        fclose(file);
        file = fopen("tasks.txt", "a");
        if (file == NULL)
        {
            printf("Error opening file for appending!\n");
            return;
        }
    }

    int iD;
    int lineCount = countLinesInFile("tasks.txt");
    if (lineCount == 0)
    {
        iD = 1;
    }
    else
    {
        iD = (lineCount + 1) / 2;
    }

    fprintf(file, "%d. Task: %s\n...Description: %s\n", iD, name, description);
    fclose(file);
}

// 02 viewTasks function

void viewTasks()
{
    FILE *viewFile;
    viewFile = fopen("tasks.txt", "r");
    if (viewFile == NULL)
    {
        printf("No tasks found.\n");
        return;
    }

    char line[256];
    while (fgets(line, sizeof(line), viewFile))
    {
        printf("%s", line);
    }
    printf("\nNo of tasks: %d\n", (l - 1) / 2);
    fclose(viewFile);
}

// 03 counting lines in a file

int countLinesInFile(char *filename)
{
    FILE *file = fopen(filename, "r");
    if (file == NULL)
    {
        return 0; // File doesn't exist or can't be opened
    }

    int count = 0;
    char ch;
    while ((ch = fgetc(file)) != EOF)
    {
        if (ch == '\n')
        {
            count++;
        }
    }

    fclose(file);
    return count;
}

// 04 deleting a task

void deleteTask()
{
    int totalTasks = (l - 1) / 2; // Calculate total tasks based on the number of lines
    clearInputBuffer();
    int toDelete;
    printf("Enter the task number to delete: ");
    scanf("%d", &toDelete);
    clearInputBuffer();
    if (toDelete < 1 || toDelete > totalTasks)
    {
        printf("Invalid task number. Please try again.\n");
        clearInputBuffer();
        return;
    }
    FILE *temp = fopen("tasks.txt", "r");
    if (temp == NULL)
    {
        printf("No tasks found.\n");
        return;
    }

    int lc = countLinesInFile("tasks.txt");
    int i = 0;
    char lines[100][250];
    while (fgets(lines[i], sizeof(lines[i]), temp) && i < lc)
    {
        i++;
    }
    fclose(temp);
    FILE *rough = fopen("tasks.txt", "w");
    if (rough == NULL)
    {
        printf("Error opening file for writing!\n");
        return;
    }
    fprintf(rough, "TASKS :\n");

    i = 1;
    int j;
    char tsk[100];
    char desc[150];
    int len;
    int iD = 1;

    while (i < lc)
    {

        if ((i + 1) / 2 == toDelete)
        {
            FILE *bin = fopen("bin.txt", "r");
            if (bin == NULL)
            {
                // If bin.txt doesn't exist, create it
                bin = fopen("bin.txt", "w");
                if (bin == NULL)
                {
                    printf("Error creating bin file!\n");
                    fclose(rough);
                    return;
                }
                fprintf(bin, "DELETED TASKS :\n");
            }
            else
            {
                fclose(bin); // Close the file to reopen in append mode later
                bin = fopen("bin.txt", "a");
                if (bin == NULL)
                {
                    printf("Error opening bin file for appending!\n");
                    return;
                }
            }

            len = strlen(lines[i]);
            for (j = 0; lines[i][j] != '\0'; j++)
            {
                tsk[j] = lines[i][j + 3];
            }
            tsk[j] = '\0'; // Null-terminate the string
            i++;
            len = strlen(lines[i]);
            for (j = 0; lines[i][j] != '\0'; j++)
            {
                desc[j] = lines[i][j];
            }
            desc[j] = '\0'; // Null-terminate the string
            i++;
            int BiD;
            int lineCount = countLinesInFile("bin.txt");
            if (lineCount == 0)
            {
                BiD = 1;
            }
            else
            {
                BiD = (lineCount + 1) / 2;
            }
            fprintf(bin, "%d. %s%s", BiD, tsk, desc); // add deleted task to bin
            fclose(bin);
            continue;
        }

        len = strlen(lines[i]);
        for (j = 0; lines[i][j] != '\0'; j++)
        {
            tsk[j] = lines[i][j + 3];
        }
        tsk[j] = '\0'; // Null-terminate the string
        i++;
        len = strlen(lines[i]);
        for (j = 0; lines[i][j] != '\0'; j++)
        {
            desc[j] = lines[i][j];
        }
        desc[j] = '\0'; // Null-terminate the string
        i++;
        fprintf(rough, "%d. %s%s", iD, tsk, desc);
        iD++;
    }

    fclose(rough);
}

// main function

int main()
{
    int zero;
    l = countLinesInFile("tasks.txt");

    while (1)
    {
        printf("\nEnter 0 to open the task manager and 1 to exit program\n");
        if (scanf("%d", &zero) != 1)
        {
            printf("Invalid input. Please enter 0 or 1.\n");
            clearInputBuffer();
            continue;
        }

        if (zero == 1)
        {
            printf("Exiting the ToDoApp. Goodbye!\n");
            break;
        }
        else if (zero == 0)
        {
            printf("Welcome to the ToDoApp!\n");
            printf("You can add tasks, view tasks, and delete tasks.\n");
            printf("=========================================================\n");
            printf("type 'add' to add a task\n");
            printf("type 'view' to view all tasks\n");
            printf("type 'delete' to delete a task\n");
            printf("=========================================================\n");

            char command[10];
            clearInputBuffer();
            printf("Enter command: ");
            if (fgets(command, sizeof(command), stdin) == NULL)
            {
                printf("Error reading command!\n");
            }
            stripNewline(command);

            if (strcmp(command, "add") == 0)
            {
                addTask();
                printf("Task added successfully!\n");
            }

            else if (strcmp(command, "view") == 0)
            {
                viewTasks();
            }
            else if (strcmp(command, "delete") == 0)
            {
                deleteTask();
                printf("Task deleted successfully!\n");
            }

            else
            {
                printf("Invalid command. Please try again.\n");
                clearInputBuffer();
            }
        }
    }

    return 0;
}
