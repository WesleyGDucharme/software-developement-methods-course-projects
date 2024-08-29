/** @file song_analyzer.c
 *  @brief A pipes & filters program that uses conditionals, loops, and string processing tools in C to process song
 *  data and printing it in a different format.
 *  @author Felipe R.
 *  @author Hausi M.
 *  @author Angadh S.
 *  @author Juan G.
 *  @author Wesley Ducharme
 *  @Date: 2024/02/07
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/**
 * @brief The maximum line length.
 *I made this bigger as I was getting some duplicate song structures of lines that went past 132 due to their names being too big.
 */
#define MAX_LINE_LEN 500

//Song structure
typedef struct{
    char track_name[100];
    char artists[100];
    int artist_count;
    int release_year;
    int in_playlists;
    char streams[50];
    char key[50];
    char mode[50]; 
} Song;

//Arguments structure
typedef struct{
    int q_number;
    char file_name[50];
} Arguments;

 /**
 *Function: get_arguments
 *Arg  1: the count of arguments passed by the command line
 *Arg 2: the list of arguments passed by the command line
 *Returns an Arguments structure
 *Purpose: gets the actual value of the arguments passed by the command line
 */
Arguments get_arguments(int argc, char *argv[]){
   
    char *question_arg_token = strtok(argv[1], "=");
    question_arg_token = strtok(NULL, "=");

    char *file_arg_token = strtok(argv[2], "=");
    file_arg_token = strtok(NULL, "=");

    Arguments args;
    // gets the correct question number by subtracting its axii number by 48
    args.q_number = *question_arg_token - 48;
    strcpy(args.file_name, file_arg_token);
    return args;
}

/**
 *Function: make_song_struct
 *Arg 1: char pointer that points to a read csv line
 *Returns the Song structure
 *Purpose: Organizes the csv line into a Song structure
 */
Song make_song_struct(const char *line) {
    Song song;
    //organizes the information in the line to be a Song structure
    sscanf(line, "%100[^,],%100[^,],%d,%d,%d,%50[^,],%50[^,],%50[^\n]", song.track_name, song.artists, &song.artist_count, &song.release_year, &song.in_playlists, song.streams, song.key, song.mode);
    return song;
}

/**
 * Function: read_and_fill
 * Arg 1: the name of the input file
 * Arg 2: an array that is to be filled
 * Returns the size of the array as int.
 * Purpose: reads the inputed csv file and calls make_song_struct() to organize the info on each line into a Song structure and then puts those structures into an array
 */
int read_and_fill(const char *in_file, Song song_array[]) {
    FILE *input_file = fopen(in_file, "r");

    char line[MAX_LINE_LEN];
    //gets rid of the first line in the csv.
    fgets(line, sizeof(line), input_file);
    int i = 0;
    //makes each line a Song structure and puts them in an array.
    while (fgets(line, sizeof(line), input_file) != NULL){
   	Song cur_song;
    	cur_song = make_song_struct(line);
    	song_array[i] = cur_song;
    	i++;
    }

    fclose(input_file);
    return i;
}

/**
 *Function q1_q2_output
 *Arg 1: question number
 *Arg 2: array filled with Song structures
 *Arg 3: size of the array
 *Purpose: processes the data in the array as specified by question 1 or 2
 */
void q1_q2_output(int q_number, Song song_arr[], int array_size) {
    FILE* output_file = fopen("output.csv", "w");
    fprintf(output_file, "Artist(s),Song\n");

    char *target_name;
    if (q_number == 1){
    target_name = "Rae Spoon";
    } else{
    target_name = "Tate McRae";
    }

    for(int i = 0; i<array_size; i++){
	if (strcmp(song_arr[i].artists, target_name) == 0){
	    fprintf(output_file, "%s,%s\n", song_arr[i].artists, song_arr[i].track_name);
	}
    }
    fclose(output_file);   
}

/**
 *Function: remove_carriage
 *Arg 1: a char that points to a string with a carriage character
 *Purpose: remove the carriage character
 */
void remove_carriage(char *str) {
    int length = strlen(str);
    while (length > 0 && (str[length - 1] == '\r' || str[length - 1] == '\n')) {
        str[length - 1] = '\0';
        length--;
    }
}

/**
 *Function: q3_output
 *Arg 1: array filled with Song structures
 *Arg 2: size of the array
 *Purpose: processes the data in the array as specified by question 3
 */
void q3_output(Song song_arr[], int array_size) {
    FILE* output_file = fopen("output.csv", "w");
    fprintf(output_file, "Artist(s),Song\n");

    char *target_name;
    char *scale;
    target_name = "The Weeknd";
    scale = "Major";
    for(int i = 0; i<array_size; i++){
	//removes the carriage character from the mode of the song so the comparison can be done
	remove_carriage(song_arr[i].mode);
	if ((strcmp(song_arr[i].artists, target_name) == 0) && (strcmp(song_arr[i].mode, scale) == 0)){
	    fprintf(output_file, "%s,%s\n", song_arr[i].artists, song_arr[i].track_name);
	}
    }
    fclose(output_file);
}

/**
 *Function q4_output
 *Arg 1: array filled with Song structures
 *Arg 2: size of the array
 *Purpose: processes the data in the array as specified by question 4
 */
void q4_output(Song song_arr[], int array_size) {
    FILE* output_file = fopen("output.csv", "w");
    fprintf(output_file, "Artist(s),Song\n");

    for(int i = 0; i<array_size; i++){
    	if ((song_arr[i].in_playlists > 5000) && ((strcmp(song_arr[i].key, "D") == 0) || (strcmp(song_arr[i].key, "A") == 0))){
	    fprintf(output_file, "%s,%s\n", song_arr[i].artists, song_arr[i].track_name);
	    }
    }
    fclose(output_file);
}

/**
 *Function: q5_output
 *Arg 1: array filled with Song structures
 *Arg 2: size of the array
 *Purpose: processes the data in the array as specified by question 5
 */
void q5_output(Song song_arr[], int array_size) {
    FILE* output_file = fopen("output.csv", "w");
    fprintf(output_file, "Artist(s),Song\n");
    char *targ_name;
    targ_name = "Drake";

    // loop through the array
    for(int i = 0; i<array_size; i++){
	char artists_copy[sizeof(song_arr[i].artists)];
	strcpy(artists_copy, song_arr[i].artists);

        char *name_token = strtok(artists_copy, " ");
	//check to see if the target artist is present and release year
        while (name_token != NULL) {
	    if((strcmp(name_token, targ_name) == 0) && ((song_arr[i].release_year == 2021) || (song_arr[i].release_year == 2022))){
	        fprintf(output_file, "%s,%s\n", song_arr[i].artists, song_arr[i].track_name);
		break;
	    }
	    name_token = strtok(NULL, " ");
	}
    }
    fclose(output_file);
}


/**
 *Function: process_data
 *Arg 1: question number
 *Arg 2: array filled with Song structures
 *Arf 3: the size of the array
 *Purpose: calls functions to process the data in the array depending on the question number.
 */
void process_data(int q_number, Song song_arr[], int array_size) {
    if((q_number == 1) || (q_number ==2)) {
	q1_q2_output(q_number, song_arr, array_size);
    } else if(q_number == 4) {
        q4_output(song_arr, array_size);
    } else if(q_number == 3) {
	q3_output(song_arr, array_size);
    } else {
        q5_output(song_arr, array_size);
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
int main(int argc, char *argv[]) {
    // TODO: your code.
    Song song_array[1000];
    Arguments args = get_arguments(argc, argv);
    int arr_size = read_and_fill(args.file_name, song_array);
    process_data(args.q_number, song_array, arr_size);
   
    exit(0);
}
