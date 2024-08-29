/** @file music_manager.c
 *  @brief A small program to analyze songs data.
 *  @author Mike Z.
 *  @author Felipe R.
 *  @author Hausi M.
 *  @author Juan G.
 *  @author Angadh S.
 *  @author Wesley Ducharme
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "list.h"
#include "emalloc.h"

#define MAX_LINE_LEN 200

/**
 * @brief Song structure
 *
 * @field formatted_date A date following a format.
 * @field track_name The name of the track.
 * @field artists The names of the artists who made the song.
 * @field rel-year The year of release.
 * @field rel_month The month of release.
 * @field re_day The day of release.
 * @field streams The number of times streamed.
 * @field playlists_spotify The number of spotify playlists the song is in.
 * @field playlists_apple The number of apple playlists the song is in.
 */
typedef struct{
    char formatted_date[50];
    char track_name[100];
    char artists[100];
    int rel_year;
    int rel_month;
    int rel_day;
    long int streams;
    int playlists_spotify;
    int playlists_apple;
} Song;

/**
 * @brief Arguments structure
 * 
 * @field file_name The name of the file.
 * @field filter How the information should be filtered.
 * @field value The value each filtered item should contain.
 * @field order_by The variable that the items should be ordered by.
 * @field order The order of which the variables should be organized.
 * @field limit The number of items that should be contained in the output.
 * 
 * @Note on limit: Should no limit be passed by command line, then limit will be 0 and by extension this program treats limit being 0 as there being no limit.
 */
typedef struct {
    char file_name[50];
    char filter[50];
    char value[50];
    char order_by[100];
    char order[100];
    int limit;
} Arguments;

/**
 * Function: get_arguments
 * -----------------------
 * @brief Parses the command line arguments
 * 
 * @param argc The number of arguments.
 * @param argv[] the list of arguments passed by the command line.
 *
 * @return Arguments The structure of arguments.
 */
Arguments get_arguments(int argc, char *argv[]) {
    Arguments args;

    char *file_name = strtok(argv[1], "=");
    file_name = strtok(NULL, "=");
    strcpy(args.file_name, file_name);

    char *filter = strtok(argv[2], "=");
    filter = strtok(NULL, "=");
    strcpy(args.filter, filter);

    char *value = strtok(argv[3], "=");
    value = strtok(NULL, "=");
    strcpy(args.value, value);

    char *order_by = strtok(argv[4], "=");
    order_by = strtok(NULL, "=");
    //Makes the order_by argument the same string as it's respective column
    if (strcmp(order_by, "STREAMS") == 0) {
        strcpy(args.order_by, "streams");
    } else if (strcmp(order_by, "NO_SPOTIFY_PLAYLISTS") == 0){
        strcpy(args.order_by, "in_spotify_playlists");
    } else {
        strcpy(args.order_by, "in_apple_playlists");
    }

    char *order = strtok(argv[5], "=");
    order = strtok(NULL, "=");
    strcpy(args.order, order);

    //make limit = 0 if there is no limit argument
    if (argc == 7) {
        char *limit = strtok(argv[6], "=");
        limit = strtok(NULL, "=");
        args.limit = atoi(limit);
    } else {
    args.limit = 0;
    }

    return args;
}

/**
 * Function: formatted_date
 * ------------------------
 * @brief Formattes the date information.
 *
 * @param year The released year.
 * @param month The released month.
 * @param day The released day.
 *
 * @return char* The formatted date.
 */
char* formatted_date(int year, int month, int day){
    char* formatted_date = (char*)emalloc(50 * sizeof(char));
    sprintf(formatted_date, "%d-%d-%d", year, month, day);
    return formatted_date;
}

/**
 * Function: make_song_struct
 * --------------------------
 * @brief Makes a Song structure from the infrmation in the line.
 * 
 * @param *line A pointer to the current line.
 *
 * @return Song A Song structure.
 *
 */
Song make_song_struct(const char *line) {
    Song song;
    sscanf(line, "%100[^,],%100[^,],%*d,%d,%d,%d,%d,%ld,%d", song.track_name, song.artists, 
           &song.rel_year, &song.rel_month, &song.rel_day, &song.playlists_spotify, &song.streams, &song.playlists_apple);
    return song;
}

/**
 * Function: sort_nodes
 * -------------------
 *  @brief Puts information in the current song structure into a node and puts it into it's appropriate spot based on the arguments.
 *
 *  @param args The Arguments structure of command line arguments.
 *  @param song The Song structure of the current song.
 *  @param **list A pointer to the pointer of the head of the linked list.
 */
void sort_nodes(Arguments args, Song song, node_t **list){
    //check how its filtered
    if (strcmp(args.filter, "ARTIST") == 0) {
        //check the values it being filtered by
        if(strstr(song.artists, args.value) != NULL) {
            node_t *new_node_ptr = new_node(song.formatted_date, song.track_name, song.artists, song.streams);
            //sort in a specific order based on the value
            if(strcmp(args.value, "Dua Lipa") == 0) {
                *list = add_inorder_asc(*list, new_node_ptr);
            } else {
                *list = add_inorder_desc(*list, new_node_ptr);
            }
        }
    } else {
        if (song.rel_year == atoi(args.value)) {
            node_t *new_node_ptr;
            if (strcmp(args.order_by, "in_spotify_playlists") == 0) {
                new_node_ptr = new_node(song.formatted_date, song.track_name, song.artists, song.playlists_spotify);
            } else {
                new_node_ptr = new_node(song.formatted_date, song.track_name, song.artists, song.playlists_apple);
            }
            *list = add_inorder_desc(*list, new_node_ptr);
        }
    }
    
}


/**
 * Function: read_file_to_list
 * ---------------------------
 * @brief Reads the input file, processes the lines and makes the linked list with helper functions.
 *
 * @param args An Arguments structure of parssed command line arguments.
 * 
 * @return node_t* A pointer to the head of the linked list.
 */
node_t* read_file_to_list(Arguments args) {
    FILE *input_file = fopen(args.file_name, "r");

    node_t *list = NULL;
    char line[MAX_LINE_LEN];

    fgets(line, sizeof(line), input_file);

    while (fgets(line, sizeof(line), input_file) != NULL) {
        Song song = make_song_struct(line);

        char *form_date = formatted_date(song.rel_year, song.rel_month, song.rel_day);
        strcpy(song.formatted_date, form_date);
        free(form_date);

        sort_nodes(args, song, &list);
    }
    fclose(input_file);
    return list;
}

/**
 * Function: print_node
 * --------------------
 * @brief Allows to print out the content of a node.
 *
 * @param p The pointer of the node to print.
 * @param arg The pointer to the output.csv file.
 *
 */
void print_node(node_t *p, FILE* out_file)
{
    fprintf(out_file, "%s,%s,%s,%ld\n", p->date, p->track_name, p->artists, p->order_by);
}

/**
 * Function: print_to_file
 * -----------------------
 *  @brief Prints the contents of each node in the linked list to a csv file.
 *
 *  @param args The structure of arguments passed by the command line.
 *  @param node The head of the linked list.
 */
void print_to_file(Arguments args, node_t *node) {
    FILE* out_file = fopen("output.csv", "w");
    fprintf(out_file, "released,track_name,artist(s)_name,%s\n", args.order_by);
    apply(node, print_node, out_file, args.limit);
    fclose(out_file);
}

/**
 * Function: free_space
 * --------------------
 *  @brief Frees the space allocated for the list.
 *
 *  @param list pointer to the head of the list.
 */
void free_space(node_t *list){
    node_t *temp_n = NULL;
    for (; list != NULL; list = temp_n){
        temp_n = list->next;
        free(list->date);
        free(list->track_name);
        free(list->artists);
        free(list);
     }
}

/**
 * Function: main
 * --------------
 * @brief The main function and entry point of the program.
 *
 * @param argc The number of arguments passed to the program.
 * @param argv The list of arguments passed to the program.
 * @return int 0: No errors; 1: Errors produced.
 *
 */
int main(int argc, char *argv[]){
    // Getting the arguments from the command line
    Arguments args = get_arguments(argc, argv);

    // Making the linked list
    node_t *list = read_file_to_list(args);    
    
    // Printing out the content of the sorted list to output.csv
    print_to_file(args, list);

    // Releasing the space allocated for the list and other emalloc'ed elements
    free_space(list);
    
    exit(0); 
}
