import csv
import math
import random
import sys


# The program receives two csv input files as program parameters. The first input file are all the emails that are in
# the set, with one email for each line. The first line of the file must be the word "Email". The second input file
# are the emails that are going to be tested if they are in the set or not. The program will produce a csv file with
# the results.
#
# The Bloom Filter is a data structure designed to tell you, rapidly and memory-efficiently, whether an element is
# present in a set.

class BloomFilter:
    def __init__(self, inputfile1, inputfile2):

        # Receives inputs files.
        self.input = inputfile1
        self.input2 = inputfile2

        # Opens first input file and store the content of the file in the lines variable.
        with open(self.input) as self.file:
            self.reader = csv.reader(self.file)
            self.lines = []
            for line in self.reader:
                self.lines.append(line[0])

            # Removes the word "Email" from the lines variable.
            self.lines.pop(0)

        # Opens second input file and store the content of the file in the lines2 variable.
        with open(self.input2) as self.file2:
            self.reader = csv.reader(self.file2)
            self.lines2 = []
            for line in self.reader:
                self.lines2.append(line[0])

            # removes the word "Email" from the lines variable.
            self.lines2.pop(0)

        # Counts the number of items and assigns it to Nitems variable.
        self.Nitems = 0
        for line in self.lines:
            self.Nitems += 1

        # Assigns necessary variables and calculates them.

        # The percent wanted for probability of false positives.
        self.Percent = 0.0000001

        # Number of bits in the filter.
        self.bits = math.ceil((self.Nitems * math.log(self.Percent)) / (math.log(1 / (math.pow(2, math.log(2))))))

        # Number of hash functions.
        self.Nhashing = round((self.bits / self.Nitems) * math.log(2))

        # List of the bits in the Bloom Filter.
        self.bloomlist = [0] * self.bits

        # Boolean list that determines if each element is probably in the DB or is not in the DB.
        self.boolList = []

        # List of dictionarys, each dictionary stores the values of the hashing for each character of the elements.
        # Every dictionary has different values for each element since they use different hashing functions.
        self.mydicts = []

    # Calculates the hashing for each character of the element passed in the variable word, stores it in
    # the respective dictionary, and then joins all the calculated numbers to return the value of the hashing
    # of the word in the number variable.
    #
    # @param word  element to be hashed
    # @param track  index for the dictionary in the dictionary list
    def hashing(self, word, track):
        number = ''
        for n in word:

            # Verifies if the character is in the dictionary and if not add it to the dictionary
            if not self.mydicts[track].__contains__(n):
                randnum = random.randint(1, 9)
                self.mydicts[track][n] = randnum
                number += str(randnum)
            else:
                number += str(self.mydicts[track][n])

        # Adds the element to be hashed to the dictionary, assigns the complete calculated hashing value to it
        # and returns it
        self.mydicts[track][word] = int(number)
        return int(number)

    # Uses the hashing function to get the hash value of every element in the file, multiplies it by module of the bits
    # of the bloom filter, and using that activates the bits to the bloomlist variable in their respective position.
    def Bloom_filter(self):
        for n in range(self.Nhashing):

            # For every hashing function adds a new dictionary to the dictionary list
            self.mydicts.append(dict())

            # Loops through every element of the file, calculates its hashing value, and activate the bit in its
            # respective position
            for word in self.lines:
                self.hashing(word, n)
                hash_num = self.mydicts[n][word] % self.bits
                self.bloomlist[hash_num] = 1

    # Checks if the elements in the second input files are in the first input file and adds to the boolList variable
    # True if its in the file and false if its not in the file.
    def check_Bloom_list(self):
        for word in self.lines2:
            wordIn = False

            for n in range(self.Nhashing):

                if self.mydicts[n].__contains__(word):

                    # Gets the position of the element in the respective dictionary.
                    pos = self.mydicts[n][word] % self.bits
                    if self.bloomlist[pos] == 1:
                        wordIn = True
                    else:
                        wordIn = False
                        break
            self.boolList.append(wordIn)

    # Creates the output file containing each entry of whether it is or it's not in the DB.
    def Produce_Result_File(self):
        with open('results.csv', 'w', newline='') as newfile:
            writer = csv.writer(newfile)
            writer.writerow(['Email', 'Result'])

            track = 0
            for word in self.lines2:
                if self.boolList[track] == True:
                    writer.writerow([word, 'Probably in the DB'])
                else:
                    writer.writerow([word, 'Not in the DB'])
                track += 1


def main(args: list):
    # Instantiates the bloom filter and runs it.
    B = BloomFilter(args[0], args[1])
    B.Bloom_filter()
    B.check_Bloom_list()
    B.Produce_Result_File()


main(sys.argv[1:])
