/*gcc -fopenmp -o code range_partition2.c
./code.exe*/
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define DATA_SIZE 100000
#define NUM_THREADS 4

typedef struct {
    int key;
    int value;
    int thread_id; // Added to track which thread processed the result
} TableRow;

TableRow table1[DATA_SIZE];
TableRow table2[DATA_SIZE];
TableRow join_results[DATA_SIZE];
TableRow join_results2[DATA_SIZE]; // For non-partitioned results
int result_count = 0;
int result_count2 = 0;

omp_lock_t lock;

// Function to generate random data for Table 2
void generate_random_data(TableRow* table) {
    for (int i = 0; i < DATA_SIZE; i++) {
        table[i].key = i + 1;
        table[i].value = rand() % DATA_SIZE + 1; // Random values between 1 and DATA_SIZE
    }
}

// Write two tables to a file
void write_tables_to_file(const char* filename) {
    FILE* file = fopen(filename, "w");
    if (!file) {
        perror("Error opening file for writing");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < DATA_SIZE; i++) {
        fprintf(file, "%d %d\n", table1[i].key, table1[i].value);
    }
    fprintf(file, "===\n"); // Separator between two tables
    for (int i = 0; i < DATA_SIZE; i++) {
        fprintf(file, "%d %d\n", table2[i].key, table2[i].value);
    }

    fclose(file);
}

// Read tables from a file
void read_tables_from_file(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("Error opening file for reading");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < DATA_SIZE; i++) {
        fscanf(file, "%d %d", &table1[i].key, &table1[i].value);
    }

    char separator[4];
    fscanf(file, "%s", separator); // Read separator

    for (int i = 0; i < DATA_SIZE; i++) {
        fscanf(file, "%d %d", &table2[i].key, &table2[i].value);
    }

    fclose(file);
}

// Perform range join
void range_join(int start, int end, int thread_id) {
    for (int i = start; i < end; i++) {
        for (int j = 0; j < DATA_SIZE; j++) {
            if (table1[i].value == table2[j].value) {
                omp_set_lock(&lock);
                join_results[result_count].key = table1[i].value;
                join_results[result_count].value = table2[j].value;
                join_results[result_count].thread_id = thread_id; // Record thread ID
                result_count++;
                omp_unset_lock(&lock);
            }
        }
    }
}

// Perform non-partitioned join
void non_partitioned_join() {
    for (int i = 0; i < DATA_SIZE; i++) {
        for (int j = 0; j < DATA_SIZE; j++) {
            if (table1[i].value == table2[j].value) {
                join_results2[result_count2].key = table1[i].value;
                join_results2[result_count2].value = table2[j].value;
                join_results2[result_count2].thread_id = -1; // No specific thread
                result_count2++;
            }
        }
    }
}

// Write join results to a file
void write_results_to_file(const char* filename, TableRow* results, int count) {
    FILE* file = fopen(filename, "w");
    if (!file) {
        perror("Error opening file for writing results");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < count; i++) {
        fprintf(file, "%d %d (Processed by Core %d)\n",
                results[i].key, results[i].value, results[i].thread_id);
    }

    fclose(file);
}

int main() {
    // Initialize Table 1 with consistent data
    for (int i = 0; i < DATA_SIZE; i++) {
        table1[i].key = i + 1;
        table1[i].value = i + 1;
    }

    // Generate random data for Table 2
    generate_random_data(table2);

    // Write tables to file
    const char* input_file = "tables.txt";
    write_tables_to_file(input_file);

    // Read tables back from file
    read_tables_from_file(input_file);

    // Initialize lock
    omp_init_lock(&lock);

    // Measure and perform parallel join with range partitioning
    double start_time = omp_get_wtime();
    #pragma omp parallel num_threads(NUM_THREADS)
    {
        int thread_id = omp_get_thread_num();
        int chunk_size = DATA_SIZE / NUM_THREADS;
        int start = thread_id * chunk_size;
        int end = (thread_id == NUM_THREADS - 1) ? DATA_SIZE : start + chunk_size;

        range_join(start, end, thread_id);
    }
    double end_time = omp_get_wtime();
    double range_partition_time = end_time - start_time;

    // Write range partitioned results to file
    const char* output_file = "join_results.txt";
    write_results_to_file(output_file, join_results, result_count);

    // Measure and perform non-partitioned join
    start_time = omp_get_wtime();
    non_partitioned_join();
    end_time = omp_get_wtime();
    double non_partition_time = end_time - start_time;

    // Write non-partitioned results to file
    const char* output_file2 = "join_results2.txt";
    write_results_to_file(output_file2, join_results2, result_count2);

    // Print timing comparison
    printf("Time for range partitioned join: %f seconds\n", range_partition_time);
    printf("Time for non-partitioned join: %f seconds\n", non_partition_time);
    printf("Join results written to %s and %s\n", output_file, output_file2);

    // Destroy lock
    omp_destroy_lock(&lock);

    return 0;
}

