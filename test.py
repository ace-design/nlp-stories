import subprocess
dataset = ["g02","g03", "g04", "g05", "g08", "g10", "g11", "g12", "g13", "g14", "g16", "g17", "g18", "g19", "g21", "g22", "g23", "g24", "g25", "g26", "g27", "g28"]
# for data in dataset:
#     print(data)
#     line = "python nlp/nlp_tools/chatgpt/convert_chatgpt_output_format.py nlp/nlp_tools/chatgpt/gpt-stories/output/gpt-3.5-turbo-0613/" +data +\
#         " " + data + "_chatgpt"
#     subprocess.run(line)


# name = ["federalspending", "loudoun", "recycling", "openspending", "frictionless", "scrumalliance", "nsf", "camperplus", "planningpoker", "datahub", "mis", "cask", "neurohub", "alfred", "badcamp", "rdadmp", "archivesspace", "unibath", "duraspace", "racdam", "culrepo", "zooniverse"]
# for i in range(len(dataset)):
#     line = "python .\\setup_data\\find_intersecting_stories.py inputs\\individual_backlog\\dataset\\" + dataset[i] + "-" + name[i] + \
#         ".txt inputs\\individual_backlog\\ecmfa_vn\\fixed\\" + dataset[i] + ".json inputs\\individual_backlog\\valid_visual_narrator_stories\\" + \
#             dataset[i] + ".txt inputs\\individual_backlog\\chatgpt_stories\\" + dataset[i] + "_chatgpt.txt " + dataset[i] 
#     subprocess.run(line)

# for data in dataset:
#     print(data)
#     line = "python setup_data/merge_data.py  inputs\\global\\intersecting_stories\\global.txt inputs\\individual_backlog\\intersecting_stories\\"+data+".txt"
#     subprocess.run(line)

for data in dataset:
    print(data)
    line = "python setup_data/merge_data.py  nlp\\nlp_outputs\\global\\nlp_outputs_original\\chatgpt\\chatgpt_global.json nlp\\nlp_outputs\\individual_backlog\\nlp_outputs_original\\chatgpt\\" + data +"_chatgpt.json"
    subprocess.run(line)

    