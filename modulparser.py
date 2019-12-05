from bs4 import BeautifulSoup

def deuglyfy(string):
    delstrings = ["&nbsp;", "\t", "\r", "\n", "  ", "\xa0"]
    modulname = string.strip()
    for x in delstrings:
        modulname = modulname.replace(x, "")
    return modulname

def parse_courses(response):
    soup = BeautifulSoup(response, 'html.parser')
    relevant = soup.find_all("tr", {"class": "tbdata"})
    uglmodule = [x.find("td").contents[0] for x in relevant]
    module = [deuglyfy(x) for x in uglmodule]
    return module

def parse_grades(response):
    soup = BeautifulSoup(response, 'html.parser')
    relevant = soup.find_all("tr", "tbdata")
    grades = [deuglyfy(x.find_all("td")[2].contents[0])for x in relevant]
    return grades

def parse_all(response):
    return dict(zip(parse_courses(response), parse_grades(response)))

if __name__ == "__main__":
    pass
    # with open("testdaten.txt") as f:
    #     text = f.read()
    # print(parse_courses(text))
    # print(parse_grades(text))
    # print(parse_all(text))