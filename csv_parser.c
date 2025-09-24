#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FILENAME "data.csv"
#define MAX_FILE_SIZE 1024
#define MAX_LINE 100

typedef struct
{
    int column_count;
    char **columns;
} CSVRow;

typedef struct Node
{
    CSVRow row;
    struct Node *next;
} Node;

int load(char *filename, Node **head);
int save(char *filename, Node *head);
void free_list(Node *head);
void free_csv_row(CSVRow *row);
char **split_csv_line(const char *line, int *count);

int main()
{
    Node *head = NULL;
    load(FILENAME, &head);
    char line[MAX_LINE];

    // Print results
    Node *cur = head;
    while (cur)
    {
        for (int i = 0; i < cur->row.column_count; i++)
        {
            printf("%s%s", cur->row.columns[i],
                   (i < cur->row.column_count - 1) ? " | " : "");
        }
        printf("\n");
        cur = cur->next;
    }

    free_list(head);
    return 0;
}

// Split a CSV line into an array of strings
char **split_csv_line(const char *line, int *count)
{
    char *temp = strdup(line);
    if (!temp)
        return NULL;

    int capacity = 4; // start small, grow if needed
    char **fields = malloc(capacity * sizeof(char *));
    if (!fields)
    {
        free(temp);
        return NULL;
    }

    *count = 0;
    char *token = strtok(temp, ",");
    while (token)
    {
        if (*count >= capacity)
        {
            capacity *= 2;
            char **new_fields = realloc(fields, capacity * sizeof(char *));
            if (!new_fields)
            {
                free(fields);
                free(temp);
                return NULL;
            }
            fields = new_fields;
        }
        fields[*count] = strdup(token);
        (*count)++;
        token = strtok(NULL, ",");
    }

    free(temp);
    return fields;
}

void free_csv_row(CSVRow *row)
{
    for (int i = 0; i < row->column_count; i++)
    {
        free(row->columns[i]);
    }
    free(row->columns);
}

void free_list(Node *head)
{
    while (head)
    {
        Node *next = head->next;
        free_csv_row(&head->row);
        free(head);
        head = next;
    }
}

int load(char *filename, Node **head)
{
    Node *tail = NULL;
    char buffer[MAX_FILE_SIZE];
    char *data;
    char line[MAX_LINE];
    FILE *fp = fopen(FILENAME, "r");
    if (NULL == fp)
    {
        printf("No file to load.\n");
        return -1;
    }
    while (fgets(line, sizeof(line), fp))
    {
        line[strcspn(line, "\r\n")] = '\0'; // strip newline

        int count;
        char **fields = split_csv_line(line, &count);
        if (!fields)
            continue;

        Node *new_node = malloc(sizeof(Node));
        new_node->row.column_count = count;
        new_node->row.columns = fields;
        new_node->next = NULL;

        if (!*head)
            *head = tail = new_node;
        else
        {
            tail->next = new_node;
            tail = new_node;
        }
    }

    fclose(fp);

    return 0;
}

int save(char *filename, Node *head)
{
    return 0;
}
