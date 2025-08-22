import sys
import re
if len(sys.argv) == 2:
    chapterName = sys.argv[1]
else:
    print("Usage: python your_script.py <question> <language>")
    sys.exit(1)

input_filename = "uploads/input_file.txt"
start_template = "Fbook/firmamento-ai-template-start.html"
end_template = "Fbook/firmamento-ai-template-end.html"
output_filename = "Fbook/firmamento-ai-user.html"

languages = [
    "English", "Russian", "Italian", "Armenian", "Chinese",
    "Japanese", "Arabic", "French", "German", "Portuguese", "Spanish"
]

# Step 1: Read the input question/label pairs
with open(input_filename, "r", encoding="utf-8") as infile:
    # Strip whitespace and skip blank lines
    lines = [line.strip() for line in infile if line.strip()]

# Check the first non-blank line for language
if lines[0].lower().startswith("language:"):
    main_language = lines[0].split(":", 1)[1].strip()
    qa_lines = lines[1:]  # everything after the language line
else:
    raise ValueError("First line must start with 'Language:'")

qa_pairs = []
for line in qa_lines:
    if "," in line:
        value, label = line.strip().split(",", 1)
        qa_pairs.append({ "value": value.strip(), "label": label.strip() })

# Step 2: Read templates
with open(start_template, "r", encoding="utf-8") as f:
    lines = f.readlines()
#    start_html = f.read()


chapterClean = re.sub(r'^.*chapter_', '', chapterName).replace('.txt', '')
#chapterClean = chapterName.replace("chapter_", "").replace(".txt", "")

modified_lines = []
for line in lines:
    if 'document.getElementById("chapterTitle").innerHTML =' in line:
        line = 'document.getElementById("chapterTitle").innerHTML = `<p class="highlight">${texts.chapter} : ` + "' + chapterClean + '" + ` </p>`;\n'
    modified_lines.append(line)

start_html = ''.join(modified_lines)
#print(start_html)

with open(end_template, "r", encoding="utf-8") as f:
    end_html = f.read()

# Step 3: Write everything to final output
with open(output_filename, "w", encoding="utf-8") as outfile:
    outfile.write(start_html + "\n")
    outfile.write("const topics = {\n")
    for lang in languages:
        outfile.write("  {}: [\n".format(lang))
        if lang == main_language:
            for pair in qa_pairs:
                outfile.write("    {{ value: \"{}\", label: \"{}\" }},\n".format(pair['value'], pair['label']))
        outfile.write('    { value: "custom", label: "" }\n')
        outfile.write("  ],\n")
    outfile.write("};\n")
    outfile.write(end_html + "\n")

#print(f"✅ Successfully written: {output_filename}")
