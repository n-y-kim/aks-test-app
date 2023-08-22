import gettext

# Get the text from the file '../README.md' to translate
with open('../README.md', 'r') as f:
    text = f.read()

t = gettext.translation('ko-kr', 'locale', languages=['ko'] ,fallback=True)
_ = t.gettext

print(_(text))