"""Prevede text datoteko zapisano v obliki Vpr;odg1:odg2:odg3;odgPrav v python kodo s vsemi stringi primernimi za prevajanje"""

for subject in ["GEO", "MAT"]:
    data = "TextFiles/" + subject + "data.txt"
    output_data =  "TextFiles/" + subject + "data_transl.py"
    with open(data, "r") as input_file, open(output_data, "w") as output_file:
        lines = [line.strip() for line in input_file]

        string = "translatable_words = ["

        for line in lines:
            if len(line) > 1:
                question, possible_answers, correct_answer = line.split(";")
                sentences = [question] + [possible_answer for possible_answer in possible_answers.split(":")] + [correct_answer]

                new_line = "_({});_({}):_({}):_({});_({})".format(
                    sentences[0],
                    sentences[1],
                    sentences[2],
                    sentences[3],
                    sentences[4]
                )

                for sentence in sentences:
                    string += "_(\"{}\"), ".format(sentence)

        finished_string = string[:-2] + "]" #zadnjih dveh ne zelimo, ker je na koncu ", " pred ]
        print(finished_string, file=output_file)



