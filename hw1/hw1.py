import spacy

nlp = spacy.load("en_core_web_sm")

def getConversationOutput(readFile, writeFile):
    read_f = open(readFile, "r")
    write_f =open(writeFile, "w")

    speaker_pronoun_usage = dict()
    counter = 0
    for line in read_f:
        counter = counter + 1

        speaker, line = line.split(" (", 1)
        
        line = line.split("M):  ", 1)
        line = line[1]
        line = line.replace("\n", "")
        doc = nlp(line)
        write_f.write("turn "+str(counter)+"\n")
        assert doc.has_annotation("SENT_START")
        for sent in doc.sents:
            write_f.write("    sentence: "+sent.text+"\n")

            output_col1 = []
            output_col2 = []
            output_col3 = []

            for token in sent:
                output_col1.append("    token: "+token.text+10*" ")
                output_col2.append("pos tag: "+token.pos_+10*" ")
                output_col3.append("lemma: "+token.lemma_+"\n")

            for ent in sent.ents:
                output_col1.append("    named_entities: "+ent.text+"  ")
                output_col2.append("type: "+ent.label_+"\n")

            max_length_col1 = len(max(output_col1, key=len))
            max_length_col2 = len(max(output_col2, key=len))

            for i in range(len(output_col1)):
                if len(output_col1[i]) < max_length_col1:
                    output_col1[i] = output_col1[i]+(" "*(max_length_col1-len(output_col1[i])))

            for j in range(len(output_col2)):
                if len(output_col2[j]) < max_length_col2:
                    output_col2[j] = output_col2[j]+(" "*(max_length_col2-len(output_col2[j])))
            
            curr_speaker_pron_counter = 0
            for item in range(len(output_col1)):
                output = output_col1[item] + output_col2[item]
                if item <= len(output_col3)-1:
                    output = output + output_col3[item]
                else:
                    output = output.rstrip() + "\n"

                if "PRON" in output_col2[item]:
                    curr_speaker_pron_counter = curr_speaker_pron_counter + 1

                write_f.write(output)
            
            if speaker in speaker_pronoun_usage:
                speaker_pronoun_usage[speaker] = speaker_pronoun_usage[speaker] + curr_speaker_pron_counter
            else:
                speaker_pronoun_usage[speaker] = curr_speaker_pron_counter
    
    read_f.close()
    write_f.close()
    return speaker_pronoun_usage

def displayDataTable(pronounsDict1, pronounsDict2, writeFile):
    #print(pronounsDict1)
    #print(pronounsDict2)
    #print("\n")

    male_name_list = ["luke", "ted", "david", "matthew", "jake", "rick", "josh", "tony", "aaron", "michael", "nick", "george", "john"]
    female_name_list = ["judith", "tia", "meg", "vicky", "eva", "julie", "rita", "leah", "caroline", "cintihia", "ariel", "macy", "lynn", "rebecca", "cinthia", "mara", "amy", "michelle"] 
 

    table_dict = dict()

    for name in pronounsDict1:
        if name in male_name_list:
            table_dict[name+" (Group A)"] = ("Male", pronounsDict1[name])
        elif name in female_name_list:
            table_dict[name+" (Group A)"] = ("Female", pronounsDict1[name])
        else:
            table_dict[name+" (Group A)"] = ("Other", pronounsDict1[name])

    for name in pronounsDict2:
        if name in male_name_list:
            table_dict[name+" (Group B)"] = ("Male", pronounsDict2[name])
        elif name in female_name_list:
            table_dict[name+" (Group B)"] = ("Female", pronounsDict2[name])
        else:
            table_dict[name+" (Group B)"] = ("Other", pronounsDict2[name])
        
    #print(table_dict)

    max_length = 0
    for entry in table_dict:
        max_val_length = max([len(entry), len(table_dict[entry][0]), len(str(table_dict[entry][1]))])
        if max_val_length > max_length:
            max_length = max_val_length
    
    max_length = max_length + 2 # increases spacing
    #Printing the table
    write_f = open(writeFile, "w")

    male_output_cols = []
    female_output_cols = []
    num_pronouns_used_by_males = 0
    num_pronouns_used_by_females = 0
    for entry in table_dict:
        if table_dict[entry][0] == "Male":
            num_pronouns_used_by_males = num_pronouns_used_by_males + table_dict[entry][1]
            male_output_cols.append(entry + ((max_length-len(entry)) * " ") + str(table_dict[entry][1]) + ((max_length-len(str(table_dict[entry][1]))) * " "))
        elif table_dict[entry][0] == "Female":
            num_pronouns_used_by_females = num_pronouns_used_by_females + table_dict[entry][1]
            female_output_cols.append(entry + ((max_length-len(entry)) * " ") + str(table_dict[entry][1]) + ((max_length-len(str(table_dict[entry][1]))) * " "))

    write_f.write(2*((max_length * " ") + "# pronouns" + ((max_length - len("# pronouns")) * " "))+"\n")
    bigger_list_size = max([len(male_output_cols), len(female_output_cols)])
    for index in range(bigger_list_size):
        curr_row_output = ""
        if index < len(male_output_cols):
            curr_row_output = curr_row_output + male_output_cols[index]
        if index < len(female_output_cols):
            if index >= len(male_output_cols): #male output not given
                curr_row_output = curr_row_output + (len(max(male_output_cols, key=len)) * " ")
            curr_row_output = curr_row_output + female_output_cols[index] + "\n"
        write_f.write(curr_row_output)

    write_f.write("\nAverage number of prounouns used by males: " + str(num_pronouns_used_by_males / len(male_output_cols)))
    write_f.write("\nAverage number of prounouns used by females: " + str(num_pronouns_used_by_females / len(female_output_cols)))
    
    write_f.close()

speakerPronounsGroupA = getConversationOutput("10/Feb17_GroupA.txt", "groupAOutput.txt")
speakerPronounsGroupB = getConversationOutput("10/Feb17_GroupB.txt", "groupBOutput.txt")
displayDataTable(speakerPronounsGroupA, speakerPronounsGroupB, "pt3Output.txt") 