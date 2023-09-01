import tika
tika.initVM()
from tika import parser



parsed = parser.from_file('222.pdf')
print(parsed['content'])