class Wer():


    def __init__(self):
        # Values of operation types
        self.OPERATION_TYPE_OK = 0
        self.OPERATION_TYPE_SUB = 1
        self.OPERATION_TYPE_INS = 2
        self.OPERATION_TYPE_DEL = 3
        
        # Penalties
        self.DEL_PENALTY = 1
        self.INS_PENALTY = 1
        self.SUB_PENALTY = 1


    def create_all_zeroes_matrix(self, number_columns, number_rows):
        # List containing lists
        return [[0 for inner in range(number_columns)] for outer in range(number_rows)]


    def print_details(self, type_of_operation, r, h):
        i = len(r)
        j = len(h)
        number_of_substitutions = 0
        number_of_deletions = 0
        number_of_insertions = 0
        number_of_correct_words = 0
        words = []
        while i > 0 or j > 0:
            if type_of_operation[i][j] == self.OPERATION_TYPE_OK:
                number_of_correct_words += 1
                i-=1
                j-=1
                words.append("OK\t\t" + r[i]+"\t\t"+h[j])
            elif type_of_operation[i][j] == self.OPERATION_TYPE_SUB:
                number_of_substitutions +=1
                i-=1
                j-=1
                words.append("SUB\t\t" + r[i]+"\t\t"+h[j])
            elif type_of_operation[i][j] == self.OPERATION_TYPE_INS:
                number_of_insertions += 1
                j-=1
                words.append("INS\t\t" + "****" + "\t\t" + h[j])
            elif type_of_operation[i][j] == self.OPERATION_TYPE_DEL:
                number_of_deletions += 1
                i-=1
                words.append("DEL\t\t" + r[i]+"\t\t"+"****")
        
        words = reversed(words)
        print("OPERATION\tREFERENCE\tHYPOTHESIS")
        for word in words:
            print(word)
        print("#cor " + str(number_of_correct_words))
        print("#sub " + str(number_of_substitutions))
        print("#del " + str(number_of_deletions))
        print("#ins " + str(number_of_insertions))


    def wer(self, reference, hypothesis, details=False):
        r = reference.split()
        h = hypothesis.split()
        # Create matrix with all 0 values, len(r) * len(h) size 
        distance = self.create_all_zeroes_matrix(len(h)+1, len(r)+1)
        # type_of_operation will hold the operations that is done
        type_of_operation = self.create_all_zeroes_matrix(len(h)+1, len(r)+1)

        # Source prefixes can be transformed into empty string by dropping
        # all words (deletion)
        for i in range(1, len(r)+1):
            distance[i][0] = i # DEL_PENALTY * i
            type_of_operation[i][0] = self.OPERATION_TYPE_DEL
             
        # Target prefixes can be transformed from empty source prefix
        # by inserting every words (insertion)
        for j in range(1, len(h) + 1):
            distance[0][j] = j # INS_PENALTY * j
            type_of_operation[0][j] = self.OPERATION_TYPE_INS
         
        # computation
        for i in range(1, len(r) + 1):
            for j in range(1, len(h) + 1):
                if r[i-1] == h[j-1]:
                    distance[i][j] = distance[i-1][j-1]
                    type_of_operation[i][j] = self.OPERATION_TYPE_OK
                else:
                    substitutionCost = distance[i-1][j-1] + self.SUB_PENALTY # penalty is always 1
                    insertionCost    = distance[i][j-1] + self.INS_PENALTY   # penalty is always 1
                    deletionCost     = distance[i-1][j] + self.DEL_PENALTY   # penalty is always 1
                     
                    distance[i][j] = min(substitutionCost, insertionCost, deletionCost)

                    if distance[i][j] == substitutionCost:
                        type_of_operation[i][j] = self.OPERATION_TYPE_SUB
                    elif distance[i][j] == insertionCost:
                        type_of_operation[i][j] = self.OPERATION_TYPE_INS
                    else:
                        type_of_operation[i][j] = self.OPERATION_TYPE_DEL

        # Check all operations:
        if details:
            self.print_details(type_of_operation, r, h)

        result_percentage = 100 * (1 - round (distance[len(r)][len(h)] / len(r), 3))
        
        return "Recognition is {} %".format(str(result_percentage))