# ChatGPT Scripts
1. convert_chatgpt_output_format.py: Converts ChatGPT format into the standard JSON format outlined in the main README.md. Currently ChatGPT outputs each individual story. We want to merge all these annotation into one file while following the pre-defines JSON structure. 
   > python compare\convert_chatgpt_output_format.py `folder_path` `saving_name`
     - outputs: `JSON file with ChatGPT annotations`