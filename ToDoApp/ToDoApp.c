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
    char priority[5];

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

    clearInputBuffer();
    printf("Enter task priority (1-5): ");
    if (fgets(priority, sizeof(priority), stdin) == NULL)
    {
        printf("Error reading task priority!\n");
        return;
    }
    stripNewline(priority); // Remove newline character from the end of the string

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
        iD = lineCount/3 + 1;
    }

    fprintf(file, "%d. Task: %s\n...Description: %s\n...Priority level: %s\n", iD, name, description, priority);
    fclose(file);
    
    // setting all tasks as not done in NotDone.txt
    file = fopen("NotDone.txt", "r");
    if (file == NULL){
        file = fopen("NotDone.txt", "w");
        if (file == NULL)
        {
            printf("Error creating NotDone.txt file!\n");
            return;
        }
        fprintf(file, "TASK STATUS: NOT DONE:\n");
    }
    else
    {
        fclose(file);
        file = fopen("NotDone.txt", "a");
        if (file == NULL)
        {
            printf("Error opening NotDone.txt for appending!\n");
            return;
        }

    }
    fprintf(file, "%d. Task: %s\n...Description: %s\n...Priority level: %s\n", iD, name, description, priority);
    fclose(file);
}

// 02 viewTasks function

void viewTasks(FILE *viewFile)
{
    char line[256];
    while (fgets(line, sizeof(line), viewFile))
    {
        printf("%s", line);
    }
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
    int totalTasks = (l-1) / 3; // Calculate total tasks based on the number of lines
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

    // Read all lines from the file into an array
    int i = 0;
    char lines[100][250];
    while (fgets(lines[i], sizeof(lines[i]), temp) && i < l)
    {
        i++;
    }
    fclose(temp);

    // Reopen the file in write mode to overwrite it without the deleted task
    FILE *file = fopen("tasks.txt", "w");
    if (file == NULL)
    {
        printf("Error opening file for writing!\n");
        return;
    }
    fprintf(file, "TASKS :\n");
    fclose(file);

    i = 1;
    int j;
    char tsk[100];
    char desc[150];
    char prio[100]; 
    int iD = 1;

    while (i < l)
    {

        if ((i - 1)/3 + 1 == toDelete)
        {
            FILE *bin = fopen("bin.txt", "r");
            if (bin == NULL)
            {
                // If bin.txt doesn't exist, create it
                bin = fopen("bin.txt", "w");
                if (bin == NULL)
                {
                    printf("Error creating bin file!\n");
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

            //storing deleted task name
            for (j = 0; lines[i][j] != '\0'; j++)
            {
                tsk[j] = lines[i][j + 3];
            }
            tsk[j] = '\0'; // Null-terminate the string
            i++;
            
            //storing deleted task description
            for (j = 0; lines[i][j] != '\0'; j++)
            {
                desc[j] = lines[i][j];
            }
            desc[j] = '\0'; // Null-terminate the string
            i++;
            
            //storing deleted task priority
            for (j = 0; lines[i][j] != '\0'; j++)
            {
                prio[j] = lines[i][j];
            }
            prio[j] = '\0'; // Null-terminate the string
            i++;

            
            int BiD;
            int lineCount = countLinesInFile("bin.txt");
            if (lineCount == 0)
            {
                BiD = 1;
            }
            else
            {
                BiD = lineCount / 3 + 1;
            }
            
            fprintf(bin, "%d. %s%s%s", BiD, tsk, desc, prio); // add deleted task to bin
            fclose(bin);
            continue;
        }

        else{
        FILE *file = fopen("tasks.txt", "a");
        if (file == NULL)
        {
            printf("Error opening file for writing!\n");
            return;
        }          
        //storing task name
        for (j = 0; lines[i][j] != '\0'; j++)            
        {
            tsk[j] = lines[i][j + 3];
        }
        tsk[j] = '\0'; // Null-terminate the string
        i++;
        
        //storing description
        for (j = 0; lines[i][j] != '\0'; j++)          
        {
            desc[j] = lines[i][j];
        }
        desc[j] = '\0'; // Null-terminate the string
        i++;
        
        //storing priority
        for (j = 0; lines[i][j] != '\0'; j++)      
        {
            prio[j] = lines[i][j];
        }
        prio[j] = '\0'; // Null-terminate the string
        i++;
        fprintf(file, "%d. %s%s%s", iD, tsk, desc, prio);
        iD++;
        fclose(file);
        }
        
    }

    
}


// 05 change task status
void changeTaskStatus()
{
    //
    int totalTasks = (countLinesInFile("NotDone.txt")-1) / 3; // Calculate total tasks based on the number of lines
    clearInputBuffer();
    int toChange;
    printf("Enter the task number to change: ");
    scanf("%d", &toChange);
    clearInputBuffer();
    if (toChange < 1 || toChange > totalTasks)
    {
        printf("Invalid task number. Please try again.\n");
        clearInputBuffer();
        return;
    }
    FILE *temp = fopen("NotDone.txt", "r");
    if (temp == NULL)
    {
        printf("No tasks found.\n");
        return;
    }

    // Read all lines from the file into an array
    int i = 0;
    char lines[100][250];
    while (fgets(lines[i], sizeof(lines[i]), temp) && i < l)
    {
        i++;
    }
    fclose(temp);

    int lc = countLinesInFile("NotDone.txt");

    FILE *file = fopen("NotDone.txt", "w");
    if (file == NULL)
    {
        printf("Error opening file for writing!\n");
        return;
    }
    fprintf(file, "TASK STATUS: NOT DONE:\n");
    fclose(file);

    i = 1;
    int j;
    char tsk[100];
    char desc[150];
    char prio[100]; 
    int iD = 1;

    while (i < lc){

        if ((i - 1)/3 + 1 == toChange)
        {
            FILE *done = fopen("Done.txt", "r");
            if (done == NULL)
            {
                // If Done.txt doesn't exist, create it
                done = fopen("Done.txt", "w");
                if (done == NULL)
                {
                    printf("Error creating bin file!\n");
                    return;
                }
                fprintf(done, "TASK STATUS: DONE:\n");
            }
            else
            {
                fclose(done); // Close the file to reopen in append mode later
                done = fopen("Done.txt", "a");
                if (done == NULL)
                {
                    printf("Error opening bin file for appending!\n");
                    return;
                }
            }

            //storing done task name
            for (j = 0; lines[i][j] != '\0'; j++)
            {
                tsk[j] = lines[i][j + 3];
            }
            tsk[j] = '\0'; // Null-terminate the string
            i++;
            
            //storing done task description
            for (j = 0; lines[i][j] != '\0'; j++)
            {
                desc[j] = lines[i][j];
            }
            desc[j] = '\0'; // Null-terminate the string
            i++;
            
            //storing deleted task priority
            for (j = 0; lines[i][j] != '\0'; j++)
            {
                prio[j] = lines[i][j];
            }
            prio[j] = '\0'; // Null-terminate the string
            i++;

            
            int DiD;
            int lineCount = countLinesInFile("bin.txt");
            if (lineCount == 0)
            {
                DiD = 1;
            }
            else
            {
                DiD = lineCount / 3 + 1;
            }
            
            fprintf(done, "%d. %s%s%s", DiD, tsk, desc, prio); // add deleted task to Done.txt
            fclose(done);
            continue;
        }

        else{
        FILE *file = fopen("NotDone.txt", "a");
        if (file == NULL)
        {
            printf("Error opening file for writing!\n");
            return;
        }          
        //storing task name
        for (j = 0; lines[i][j] != '\0'; j++)            
        {
            tsk[j] = lines[i][j + 3];
        }
        tsk[j] = '\0'; // Null-terminate the string
        i++;
        
        //storing description
        for (j = 0; lines[i][j] != '\0'; j++)          
        {
            desc[j] = lines[i][j];
        }
        desc[j] = '\0'; // Null-terminate the string
        i++;
        
        //storing priority
        for (j = 0; lines[i][j] != '\0'; j++)      
        {
            prio[j] = lines[i][j];
        }
        prio[j] = '\0'; // Null-terminate the string
        i++;
        fprintf(file, "%d. %s%s%s", iD, tsk, desc, prio);
        iD++;
        fclose(file);
        }




    }
    
}




// 06 sorting tasks in a file

void sortTasksInFile(FILE *file, int lineCount)
{
    if (file == NULL)
    {
        printf("Error opening file for sorting!\n");
        return;
    }
    // Read all lines from the file into an array
    char lines[100][250];
    int i = 0;
    while (fgets(lines[i], sizeof(lines[i]), file) && i < 100)
    {
        i++;
    }
    fclose(file);

    //sorting tasks based on priority and writing them in a different file
    FILE *sortedFile = fopen("SortedTasks.txt", "w");
    fprintf(sortedFile, "SORTED TASKS :\n");
    int Sid; 
    // Sort the lines based on priority
    for(int p=5; p>=1; p--){
        for(i=3; i<lineCount; i+=3){
            char priority[5];
            sscanf(lines[i], "...Priority level: %s", priority);
            if (atoi(priority) == p)
            {
                //fprintf("--* Priority level: %s --*\n", priority);
                Sid = 1;
                fprintf(sortedFile, "\n--* PRIORITY: %d *--\n", p);
                fprintf(sortedFile, "%d", Sid);
                for (int j=1; lines[i-2][j] != '\0'; j++)
                {
                    fprintf(sortedFile, "%c", lines[i-2][j]);
                }
                
                fprintf(sortedFile, "%s",lines[i-1]);
                Sid++;
            }
        }
    }
    fclose(sortedFile); 
    viewTasks(fopen("SortedTasks.txt", "r"));
    printf("\nTasks sorted successfully! \n");  
        
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
            printf("type 'view all tasks' to view all tasks\n");
            printf("type 'delete' to delete a task\n");
            printf("type 'view bin' to view deleted tasks\n");
            printf("type 'change status' to change task status to done\n");
            printf("type 'check' to check status of tasks\n");
            printf("type 'sort' to sort tasks based on priority\n");
            printf("=========================================================\n");

            char command[20];
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
                l = countLinesInFile("tasks.txt");
            }

            else if (strcmp(command, "view all tasks") == 0)
            {
                FILE *file = fopen("tasks.txt", "r");
                if (file == NULL)
                {
                    printf("No tasks found.\n");
                    continue;
                }
                viewTasks(file);
                printf("\nNo of tasks: %d and No of lines in task_file: %d", (l-1)/3, l);
                fclose(file);
            }
            else if (strcmp(command, "delete") == 0)
            {
                deleteTask();
                printf("Task deleted successfully!\n");
                l = countLinesInFile("tasks.txt");
            }
            else if (strcmp(command, "view bin") == 0)
            {
                FILE *binFile = fopen("bin.txt", "r");
                if (binFile == NULL)
                {
                    printf("No deleted tasks found.\n");
                    continue;
                }
                viewTasks(binFile);
                printf("\nNo of deleted tasks: %d", (countLinesInFile("bin.txt")-1)/3);
                fclose(binFile);
            }
            else if (strcmp(command, "change status") == 0)
            {
                changeTaskStatus();
                printf("Task status changed successfully!\n");
            }

            else if (strcmp(command, "check") == 0)
            {
                printf("Check staus type (Done/Not Done): ");
                char status[20];
                if (fgets(status, sizeof(status), stdin) == NULL)
                {
                    printf("Error reading status!\n");
                    continue;
                }
                
                if (strcmp(status, "Done\n") == 0)
                {
                    FILE *doneFile = fopen("Done.txt", "r");
                    if (doneFile == NULL)
                    {
                        printf("No tasks marked as done.\n");
                        continue;
                    }
                    viewTasks(doneFile);
                    printf("\nNo of tasks done: %d", (countLinesInFile("Done.txt")-1)/3);
                    fclose(doneFile);
                }
                else if (strcmp(status, "Not Done\n") == 0)
                {
                    FILE *notDoneFile = fopen("NotDone.txt", "r");
                    if (notDoneFile == NULL || countLinesInFile("NotDone.txt") <= 1)
                    {
                        printf("No tasks pending.\n");
                        continue;
                    }
                    viewTasks(notDoneFile);
                    printf("\nNo of tasks pending: %d", (countLinesInFile("NotDone.txt")-1)/3);
                    fclose(notDoneFile);
                }
                else
                {
                    printf("Invalid status type. Please enter 'Done' or 'Not Done'.\n");
                }
            }

            else if (strcmp(command, "sort") == 0)
            {
                printf("Which task you want to sort? Press \n1 for completed tasks\n2 for pending tasks\n3 for all tasks\n");
                int sortChoice;
                printf("Enter your choice: ");
                scanf("%d", &sortChoice);
                clearInputBuffer();
                if (sortChoice == 1)
                {
                    FILE *doneFile = fopen("Done.txt", "r");
                    if (doneFile == NULL)
                    {
                        printf("No tasks marked as done.\n");
                        continue;
                    }
                    int lineCount = countLinesInFile("Done.txt");
                    sortTasksInFile(doneFile, lineCount);
                }
                else if (sortChoice == 2)
                {
                    FILE *notDoneFile = fopen("NotDone.txt", "r");
                    if (notDoneFile == NULL || countLinesInFile("NotDone.txt") <= 1)
                    {
                        printf("No tasks pending.\n");
                        continue;
                    }
                    int lineCount = countLinesInFile("NotDone.txt");
                    sortTasksInFile(notDoneFile, lineCount);
                }
                else if (sortChoice == 3)
                {
                    FILE *allTasksFile = fopen("tasks.txt", "r");
                    if (allTasksFile == NULL)
                    {
                        printf("No tasks found.\n");
                        continue;
                    }
                    int lineCount = countLinesInFile("tasks.txt");
                    sortTasksInFile(allTasksFile, lineCount);
                    
                }
                else
                {
                    printf("Invalid choice. Please enter 1, 2, or 3.\n");
                }
            }

            else
            {
                printf("Invalid command. Please try again.\n");
                clearInputBuffer();
            }
        }
    }
    printf("\nNo of tasks: %d and No of lines in task_file: %d", (l-1)/3, l);
    return 0;
}
