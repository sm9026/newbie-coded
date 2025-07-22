#include<stdio.h>
#include<stdlib.h>
#define MAX_SIZE 5

int top=-1;
int a[MAX_SIZE];
void push(int item)
{
	if(top== (MAX_SIZE-1))
	printf("\n*STACK OVERFLOW*\n");
	else
	{
	top++;
    a[top]=item;
	}
}
void pop()
{
	if(top==-1)
	{
		printf("\n*STACK UNDERFLOW*\n");
	}
	else
	{
	printf("\npop-ed element is %d\n",a[top]);
    top--;
	}
}
void display()
{
	int i;
    if(top==-1)
    {
        printf("\n*STACK IS EMPTY*\n");
        return;
    }
    else{
    printf("\nItems : \n");
    for(i=(MAX_SIZE-1);i>top;i--)
        printf("[?]\n");
    for(i=top;i>=0;i--){
	printf("[%d]\n",a[i]);
	}
    }

}
int main()
{
	int choice,k;
	while(1)
	{
	printf("\nenter 0 to exit\n");
    printf("enter 1 to push item\n");
	printf("enter 2 to pop\n");
	printf("enter 3 to display\n");
	printf("enter your choice : ");
	scanf("%d",&choice);
		switch(choice)
		{
			case 1: printf("Enter value : ");
					scanf("%d",&k);
					push(k);
					break;
			case 2: pop();
					break;
			case 3: display();
					break;
            case 0: exit(0);
			default: printf("\nPLEASE ENTER A VALID CHOICE\n");
		}
	}
    return 0;
}
