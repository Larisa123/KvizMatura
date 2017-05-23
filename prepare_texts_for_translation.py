"""Uporabno v primeru spremenitve števila vseh vprašanj ali vsebine vprašanj"""


for subject in ["GEO", "MAT"]:
    data = "TextFiles/" + subject + "data.txt"
    output_data =  "TextFiles/" + subject + "data_transl.txt"
    with open(data, "r") as input_file, open(output_data, "w") as output_file:
        lines = [line.strip() for line in input_file] # zapisano v obliki Vprasanje;odg1:odg2:odg3;odgovorPravilen

        print("", file=output_file) # main.py vzame datoteke s prazno prvo vrstico - tako sva pač napisale in je sedaj treba to upoštevati

        for line in lines:
            if len(line) > 1:
                question, possible_answers, correct_answer = line.split(";")
                sentences = [question] + [possible_answer for possible_answer in possible_answers.split(":")] + [correct_answer] # da so v pravem vrstnem redu

                new_line = "_({});_({}):_({}):_({});_({})".format(
                    sentences[0],
                    sentences[1],
                    sentences[2],
                    sentences[3],
                    sentences[4]
                )
                print(new_line, file=output_file)



