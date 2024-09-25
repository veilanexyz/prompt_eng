import os

def get_recs_data() -> str:
    folder_path = "../gpt-prompting-guide" 
    combined_text = ""
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    combined_text += f.read() + "\n" 
    save_path = os.path.join(os.getcwd(), "combined_text.md")
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(combined_text)

    return combined_text

get_recs_data()