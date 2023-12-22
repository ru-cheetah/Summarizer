from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelWithLMHead
from newspaper import Article
import pdfplumber

app = Flask(__name__)

# Load pre-trained T5 tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('T5-base')
model = AutoModelWithLMHead.from_pretrained('T5-base', return_dict=True)

# Download NLTK punkt tokenizer
# nltk.download('punkt')  # Uncomment if not already downloaded

def generate_custom_text_summary(user_input):
    try:
        # Tokenize and encode the user input for custom text
        inputs = tokenizer.encode("summarize: " + user_input, return_tensors='pt', max_length=512, truncation=True)
        output = model.generate(inputs, min_length=70, max_length=120)
        summary = tokenizer.decode(output[0])
        return summary
    except Exception as e:
        # Handle errors, log, or return an appropriate response
        return f"Error: {str(e)}"

def generate_url_summary(url_input):
    try:
        # Generate summary for the provided URL using newspaper3k
        article = Article(url_input)
        article.download()
        article.parse()
        article.nlp()
        summary = article.summary
        return summary
    except Exception as e:
        # Handle errors, log, or return an appropriate response
        return f"Error: {str(e)}"

def summarize_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        extracted_page = pdf.pages[17]  # Assuming you want to summarize the first page
        extracted_text = extracted_page.extract_text()

    inputs = tokenizer([extracted_text], truncation=True, return_tensors='pt')

    # Generate Summary
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, early_stopping=True, min_length=0, max_length=1024)
    summarized_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

    return summarized_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def generate_summary():
    user_input = request.form.get('comment_custom_area')
    url_input = request.form.get('comment_link_or_url')

    if user_input is not None and user_input.strip() != "":
        summary = generate_custom_text_summary(user_input)
        return jsonify({'summary': summary, 'input_type': 'custom_text'})

    elif url_input:
        summary = generate_url_summary(url_input)
        return jsonify({'summary': summary, 'input_type': 'url'})

    elif 'attachment' in request.files:
        pdf_file = request.files['attachment']
        pdf_path = f"uploads/{pdf_file.filename}"
        pdf_file.save(pdf_path)

        # Generate PDF summary
        pdf_summary = summarize_pdf(pdf_path)
        return jsonify({'summary': pdf_summary, 'input_type': 'pdf'})

    return jsonify({'error': 'Invalid input'})

if __name__ == '__main__':
    app.run(debug=True)

