import nltk
from tika import parser
import io

# nltk.download('punkt') # perform on first run

def pdf_to_txt(pdf_file_name, out_txt_file_name):
    content = parser.from_file(pdf_file_name)
    with open(out_txt_file_name, 'w') as file:
        file.write(content['content'])


# use this method to find which proteins have been mentioned in the paper
def intersection(lst1, lst2):
    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def detect_genes(gene_names_file, paper_file_name):
    with open(gene_names_file, 'r') as gene_file:
        content = ''.join(gene_file.readlines())

        # create a regex tokenizer that captures whole words, words with hyphens, full commas and forward slashes
        tokenizer = nltk.RegexpTokenizer(r'\w[\w-][\w.][\w/]+')

        gene_names = tokenizer.tokenize(content)

        paper_file = io.open(paper_file_name, 'rU', encoding='utf-8')
        content = ''.join(paper_file.readlines())
        paper_text = tokenizer.tokenize(content)

        result = intersection(gene_names, paper_text)

        return result


if __name__ == "__main__":
    gene_names_file = 'gene-names.txt'
    paper_file_name = 'corpus/1.txt'

    detect_genes(gene_names_file, paper_file_name)
