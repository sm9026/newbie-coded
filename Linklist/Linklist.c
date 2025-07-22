#include<stdio.h>
#include<stdlib.h>
struct node
{
	int data;
	struct node *next;
};
struct node *head=NULL;
void insert_last()
{
	int k;
	struct node *ptr,*s;
	printf("Enter value of node : ");
	scanf("%d",&k);
	ptr=(struct node*)malloc(sizeof(struct node));
	ptr->data=k;
	ptr->next=NULL;
	if(head==NULL)
	{
		head=ptr;
	}
	else
	{
		s=head;
		while(s->next!=NULL)
		{
			s=s->next;
		}
		s->next=ptr;
	}
}
void insert_first()
{
	int k;
	struct node *ptr;
	printf("Enter value of node : ");
	scanf("%d",&k);
	ptr=(struct node*)malloc(sizeof(struct node));
	ptr->data=k;
	if(head==NULL)
	{
		head=ptr;
		head->next=NULL;
    }
    else
    {
    	ptr->next=head;
    	head=ptr;
	}
}
void display()
{
	struct node *s;
	if(head==NULL)
	{
		printf("Sorry but the linklist is empty :)");
		exit(0);
	}
	else
	{
		s=head;
		printf("Elements are : \n");
		while(s!=NULL)
		{
			printf("- %d -",s->data);
			s=s->next;
		}
	}
}
void delend()
{
	struct node *ptr,*s;
	if(head==NULL)
	{
		printf("\n*LIST IS EMPTY*\n");
		exit(0);
	}
	else if(head->next==NULL)
	{
		s=head;
		head=NULL;
		printf("\nDeleted data is : %d",s->data);
		free(s);
	}
	else
	{
		s=head;
		while(s->next!=NULL)
		{
			ptr=s;
			s=s->next;
		}
		ptr->next=NULL;
		printf("\nDeleted element is : %d",s->data);
		free(s);
	}
}
void delete_any()
{
	int k,i=1;
	struct node *ptr,*s;
		if(head==NULL)
		{
		 	printf("\n*LIST IS EMPTY*\n");
		 	exit(0);	
		}
		else if(head->next==NULL)
		{
			s=head;
			head=NULL;
			printf("\nDeleted the only element that is : %d\n",s->data);
			free(s);
		}
		else
		{
			printf("\nEnter the position you want to delete :");
	        scanf("%d",&k);
		 	s=head;
			while(i<k)
			{
				if(s->next==NULL)
				{
					printf("\n*YOUR GIVEN POSITION DOESNT EXIST*\n");
					exit(0);
				}
				else
				{
					ptr=s;	
		 			s=s->next;	
		 			i++;
		 		}
		    }
		    ptr->next=s->next;
		    printf("\nDeleted element is : %d\n",s->data);
		    free(s);
		}
}
void display_menu()
{
		printf("\n\n *LINKLIST MENU*\n ");
		printf("\n Enter 0 to display menu ");
		printf("\n Enter 1 to insert first ");
		printf("\n Enter 2 to insert last ");
		printf("\n Enter 3 to display ");
		printf("\n Enter 4 to delete from end ");
		printf("\n Enter 5 to delete any position ");
		printf("\n Enter 6 to exit\n ");
		
}
int main()
{
	int choice;
	printf("\nENTER 0 TO GET DISPLAY MENU: ");
	while(1)
	{   
		scanf("%d",&choice);
		switch(choice)
		{
			case 1: insert_first();
					break;
			case 2: insert_last();
					break;
			case 3: display();
					break;
			case 4: delend();
					break;
			case 5: delete_any();
					break;
			case 0: display_menu();
					break;
			case 6: exit(0);					
			
			default: printf("\nPlease enter a valid choice");		
		}
		printf("\n your value -> ");
	}
	return 0;
}	
