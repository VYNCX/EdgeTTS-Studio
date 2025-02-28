import re

def load_edge_tts_shortnames(file_path):
    
    shortnames = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r"ShortName:\s*(\S+)", line)
            if match:
                shortnames.append(match.group(1))
    return shortnames

# Usage example
  # Update path if needed
tts_shortnames = load_edge_tts_shortnames
file_path = "./inference/edge-tts-list/edge-tts-list.txt"
# Print all shortnames
#print(tts_shortnames)