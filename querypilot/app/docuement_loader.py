def load_document(file_path):
    try:
        with open(file_path, "r") as file:
            text = file.read()
        return text.strip()
    except FileNotFoundError:
        return None


# Test your function
path = "querypilot/documents/deui.txt"
text = load_document(path)
if text is not None:
    print(text)
else:
    print("Document not found")