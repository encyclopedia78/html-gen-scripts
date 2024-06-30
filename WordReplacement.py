import re
from WordToReplace import prepositions, interrogative_pronouns
import sys
import io

# Standardausgabe auf UTF-8 setzen
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def replace_words_with_html_input_tag(text, words_to_replace):
    # Erstelle ein Wörterbuch zur Zuordnung von Wörtern zu ihren ersetzenden Nummern
    replacement_dict = {word: str(i + 1)
                        for i, word in enumerate(words_to_replace)}
    # Definiere die regulären Ausdrücke für die Delimiter
    # pattern = r' |-'
    pattern = r' '
    words = re.split(pattern, text)

    modified_words = []
    count = 1

    for word in words:
        if word.lower() in words_to_replace:
            modified_words.append(
                f"<input type=\"text\" id=\"{str(count)}\" class=\"wortInput\" placeholder=\"...\" data-correct-answer=\"{word}\">")
            count += 1
        else:
            modified_words.append(word)

    return ' '.join(modified_words)


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def wrap_lines_in_html_p_tags(text):
    """
    Converts each line of the input text into an HTML paragraph.

    Args:
        text (str): The input text with multiple lines.

    Returns:
        str: The modified text with each line wrapped in <p>...</p> tags.
    """

    lines = text.split('\n')
    html_paragraphs = [
        f'<p>{line}</p>' for line in lines if line.strip() != '']
    return '\n'.join(html_paragraphs)


def write_file(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)


def main(input_file, output_file, words_to_replace):
    text = read_file(input_file)
    replaced_text = replace_words_with_html_input_tag(text, words_to_replace)
    modified_text = wrap_lines_in_html_p_tags(replaced_text)
    write_file(output_file, modified_text)
    template_file_path = "template.html"
    placeholder_text = "<!-- insert text here -->"
    output_file_path = "output.html"
    # Call the function to replace the placeholder in the template and write to a new file
    replace_placeholder(template_file_path, modified_text,
                        placeholder_text, output_file_path)


def replace_placeholder(template_path, html_code_string, placeholder, output_path):
    """
    Replaces a placeholder in an HTML template with a provided HTML code string and writes the result to a new file.

    Parameters:
    template_path (str): The file path to the HTML template.
    html_code_string (str): The HTML code string to insert into the template.
    placeholder (str): The placeholder text in the template that will be replaced.
    output_path (str): The file path where the updated HTML content will be written.

    Returns:
    None: The function writes the updated content to the specified output file.
    """

    # Read the template content from the specified file
    with open(template_path, 'r', encoding='utf-8') as file:
        template_content = file.read()

    # Replace the specified placeholder with the provided HTML code string
    updated_content = template_content.replace(placeholder, html_code_string)

    # Write the updated content to the specified output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)


if __name__ == "__main__":
    input_file = 'input.txt'  # Pfad zur Eingabedatei
    output_file = 'output.txt'  # Pfad zur Ausgabedatei
    # Liste der zu ersetzenden Wörter
    words_to_replace = prepositions + interrogative_pronouns

    main(input_file, output_file, words_to_replace)
