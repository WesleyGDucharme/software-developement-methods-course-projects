/** @file listy.h
 *  @brief Function prototypes for the linked list.
 */
#ifndef _LINKEDLIST_H_
#define _LINKEDLIST_H_

#define MAX_WORD_LEN 50

/**
 * @brief An struct that represents a node in the linked list.
 */
typedef struct node_t
{
    char *date;
    char *track_name;
    char *artists;
    long int order_by;
    struct node_t *next;
} node_t;

/**
 * Function protypes associated with a linked list.
 */
node_t *new_node(char *date, char *track_name, char *artists, long int order_by);
node_t *add_front(node_t *, node_t *);
node_t *add_end(node_t *, node_t *);
node_t *add_inorder_asc(node_t *, node_t *);
node_t *add_inorder_desc(node_t *, node_t *);
node_t *peek_front(node_t *);
node_t *remove_front(node_t *);
void apply(node_t *, void (*fn)(node_t *, FILE *), FILE* arg, int limit);

#endif
