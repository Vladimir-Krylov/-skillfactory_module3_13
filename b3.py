class Tag:
    def __init__(self, tag, klass=None, is_single=False, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []
        self.indn = ""

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr] = value

    def __enter__(self):
        self.indn += "\t"
        return self

    def __exit__(self, type, value, traceback):
        self.text = self.AddTag()

    def __add__(self, other):
        other.indn = self.indn + "\t"
        self.children.append(other)
        return self

    def __iadd__(self, other):
        other.indn = self.indn + "\t"
        self.children.append(other)
        return self

    def AddTag(self):
        attrs = ""
        for attribute, value in self.attributes.items():
            attrs += (f' {attribute}="{value}"')

        if self.children:
            opening = f"{self.indn}<{self.tag}{attrs}>\n"

            internal = f"{self.text}"
            for child in self.children:
                internal += child.text
            ending = f"{self.indn}</{self.tag}>\n"
            return opening + internal + ending
        else:
            if self.is_single:
                return f"{self.indn}<{self.tag}{attrs}/>\n"
            else:
                return f"{self.indn}<{self.tag}{attrs}>{self.text}</{self.tag}>\n"


class TopLevelTag(Tag):
    """
    Фактически, разница между TopLevelTag и Tag в трех пунктах:
     - Объекты класса TopLevelTag скорее всего не содержат внутреннего текста;
     - Всегда парные;
     - Должна быть возможность задать атрибуты в Tag, но в данном задании для 
       TopLevelTag это необязательное условие.

    Первый учитывать нельзя, так как "скорее всего", что ничего не гарантирует
    Второй и так учитывается в Tag так как он может быть и парным в том числе
    Третий "необязательное условие", так что тоже учитываем.

    Таким образом, классы получаются эквивалентны и нет смысла дублировать 
    определение функции AddTag для экономии одного if (для второго условия).

    Так как по условию у нас все-так должно быть три класса, 
    оставил его как наследника Tag, но пустым.
    """
    pass


class HTML(Tag):
    def __init__(self, output):
        self.indn = ""
        self.text = ""
        self.children = []
        self.output = outputter1(output)

    def __enter__(self):
        return self

    def AddTag(self):
        if self.children:
            for child in self.children:
                self.text += child.text
        return (f"<html>\n{self.text}</html>")

    def __exit__(self, type, value, traceback):
        self.text = self.AddTag()
        self.output(self.text)


def outputter1(outputtype):
    if outputtype:

        def outputter2(string):
            with open(outputtype, "w", encoding="utf8") as x:
                x.write(string)
                print(f"file {outputtype} is created")

        return outputter2
    else:

        def outputter2(string):
            print(string)

        return outputter2


if __name__ == "__main__":
    """
    Если output = None, будет вывод на экран.
    Или вместо None можно указать имя файла
    """
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text", )) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                body += div
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

            doc += body
