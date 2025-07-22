#include<stdio.h>
#include<stdlib.h>
#define MAX_SIZE 5
int rear=0,a[MAX_SIZE];
void insert(int item)
{
    if(rear>=MAX_SIZE)
    printf("\n*QUEUE IS FULL*\n");
    else
    {
        a[rear]=item;
        rear++;
    }
}
void del()
{
    int i;
    if(rear==0)
    printf("\n*QUEUE IS ALREADY EMPTY*\n");
    else
    {
    printf("\nDeleted element is : %d",a[0]);
    for(i=0;i<=rear;i++)
    {
        a[i]=a[i+1];
    }
    rear--;
    }
}
void display()
{
    int i;
    printf("\n");
    printf("[FRONT] : ");
    for(i=0;i<MAX_SIZE;i++)
    {
        if(a[i]==0)
        {
        printf("[ ] : ");
        }
        else
        {
        printf("[%d] : ",a[i]);
        }
    }
    printf("[REAR]");
}
void display_menu()
{
        printf("\n\n *QUEUE MENU*\n ");
        printf("\n Enter 0 to display menu ");
        printf("\n enter 1 to insert item ");
        printf("\n enter 2 to delete ");
        printf("\n Enter 3 to display ");
        printf("\n Enter 4 to exit ");
}
int main()
{
    int choice,k;
    printf("\nENTER 0 TO IF YOU WANT TO DISPLAY MENU ELSE\n");
    printf("ENTER 1 TO INSERT ITEM\n");
    printf("ENTER 2 TO DELETE ITEM\n");
    printf("ENTER 3 TO DISPLAY QUEUE\n");
    printf("ENTER 4 TO EXIT\n");
    while(1)
    {
        printf("\n\nenter your choice : ");
        scanf("%d",&choice);
        switch(choice)
        {
            case 1: if(rear==MAX_SIZE)
                    {
                    printf("\n*QUEUE IS FULL*\n");
                    }
                    else
                    {
                    printf("Enter value : ");
                    scanf("%d",&k);
                    insert(k);
                    }
                    break;
            case 2: del();
                    break;
            case 3: display();
                    break;
            case 0: display_menu();
                    break;
            case 4: exit(0);
            default: printf("\nPLEASE ENTER A VALID CHOICE\n");
        }
    }
}
