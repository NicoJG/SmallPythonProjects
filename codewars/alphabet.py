def alphabet_position(text):
    return ' '.join(f'{ord(c)-ord("a")+1}' for c in text.lower() if ord('a')<=ord(c)<=ord('z'))

print(alphabet_position("The sunset sets at twelve o' clock."))