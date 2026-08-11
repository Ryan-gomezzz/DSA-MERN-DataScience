s = "  Hello, World! 123\n"
t = "python"
sep = ", "

print("original:", repr(s))

print("capitalize:", s.capitalize())
print("casefold:", s.casefold())
print("center:", repr(s.center(30, "*")))
print("count:", s.count("l"))
print("encode:", s.encode("utf-8"))
print("endswith:", s.endswith("\n"))
print("expandtabs:", "A\tB".expandtabs(4))
print("find:", s.find("World"))
print("format:", "{} {}".format("Hello", "again"))
print("format_map:", "{greeting}, {name}".format_map({"greeting": "Hi", "name": "Sam"}))
print("index:", s.index("World"))
print("isalnum:", "abc123".isalnum())
print("isalpha:", "abc".isalpha())
print("isascii:", s.isascii())
print("isdecimal:", "123".isdecimal())
print("isdigit:", "²³".isdigit())
print("isidentifier:", "var_name".isidentifier())
print("islower:", "hello".islower())
print("isnumeric:", "四".isnumeric())
print("isprintable:", "Hello".isprintable())
print("isspace:", "   ".isspace())
print("istitle:", "Hello World".istitle())
print("isupper:", "HELLO".isupper())
print("join:", sep.join(["one", "two", "three"]))
print("ljust:", repr("Hi".ljust(10, "-")))
print("lower:", s.lower())
print("lstrip:", repr(s.lstrip()))
print("maketrans/translate:",
      "abc".translate(str.maketrans("abc", "123")))
print("partition:", s.partition("World"))
print("replace:", s.replace("World", "Python"))
print("rfind:", s.rfind("l"))
print("rindex:", s.rindex("l"))
print("rjust:", repr("Hi".rjust(10, "-")))
print("rpartition:", s.rpartition("World"))
print("rsplit:", "a b c".rsplit(" ", 1))
print("rstrip:", repr(s.rstrip()))
print("split:", "a,b,c".split(","))
print("splitlines:", "a\nb\nc".splitlines())
print("startswith:", s.startswith("  He"))
print("strip:", repr(s.strip()))
print("swapcase:", "Hello".swapcase())
print("title:", "hello world".title())
print("upper:", s.upper())
print("zfill:", "42".zfill(5))



#This is what a set look slike 
s = {1, 2, 2, 3}
print(s)  # {1, 2, 3}

#DIctionaries:

# create dictionaries
d = {"name": "Alice", "age": 30}
empty = {}
from_keys = dict.fromkeys(["a", "b", "c"], 0)

# access values
print(d["name"])         # Alice
print(d.get("age"))      # 30
print(d.get("city", "N/A"))  # N/A

# assignment / update
d["city"] = "Paris"
d["age"] = 31

# delete items
del d["city"]
age = d.pop("age")       # removes and returns 31
print(age)

# remove last inserted item
last = d.popitem()       # removes last key/value pair
print(last)

# membership
print("name" in d)       # True
print("age" in d)        # False

# iteration
for key in d:
    print("key:", key)

for value in d.values():
    print("value:", value)

for key, value in d.items():
    print("item:", key, value)

# common methods
d = {"name": "Bob", "age": 25}
print(d.keys())          # dict_keys(['name', 'age'])
print(d.values())        # dict_values(['Bob', 25])
print(d.items())         # dict_items([('name', 'Bob'), ('age', 25)])

# copy
copy1 = d.copy()
copy2 = dict(d)

# merge/update
d.update({"age": 26, "city": "London"})
print(d)

# setdefault
value = d.setdefault("country", "UK")
print(value)             # UK
print(d["country"])      # UK

# clear
d.clear()
print(d)                 # {}

# create with constructor
d2 = dict(name="Carol", score=95)

# nested dictionary
nested = {"person": {"name": "Dana", "age": 22}, "grades": [90, 92, 88]}

# dictionary comprehension
squares = {x: x * x for x in range(5)}
print(squares)           # {0:0, 1:1, 2:4, 3:9, 4:16}

# fromkeys example
defaults = dict.fromkeys(["x", "y", "z"], 0)
print(defaults)          # {'x': 0, 'y': 0, 'z': 0}