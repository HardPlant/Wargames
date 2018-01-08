#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/*
 * A simple program for encrypting files (or stdin) using the XOR operation.
 * Such encryption is very insecure as there are only 254 valid key values,
 * but is still much more secure than ROT13, where there is only 1 valid key.
 *
 * Using a key value of 0 or 256 is equivalent to no encryption, and is
 * therefore not allowed. Other values are too large to fit into one byte
 * and therefore cannot be properly XORed with a byte.
 */

static void usage(const char *const);

int main(int argc, char *argv[])
{
    FILE *in = NULL;
    FILE *out = NULL;
    int k = 0;
    int c;

    while ((c = getopt(argc, argv, "i:o:k:h")) != -1) {
        switch (c) {
        case 'i':
            in = fopen(optarg, "r");
            break;
        case 'o':
            out = fopen(optarg, "w");
            break;
        case 'k':
            k = atoi(optarg);
            break;
        case 'h':
            usage(argv[0]);
            return EXIT_FAILURE;
        }
    }

    in = in ? in : stdin;
    out = out ? out : stdout;

    if (k <= 0 || k > 255) {
        fprintf(stderr, "%s: must specify a valid key via -k\n",
            argv[0]);
        fprintf(stderr, "%s: valid key values are from 1 to 255\n",
            argv[0]);
        return EXIT_FAILURE;
    }

    while ((c = fgetc(in)) != EOF) {
        fputc(c ^ k, out);
    }

    return EXIT_SUCCESS;
}

void usage(const char *const s)
{
    fprintf(stderr, "usage: %s -k key [-i input] [-o output]\n", s);
}
