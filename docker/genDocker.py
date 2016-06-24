#!/usr/bin/env python

from sh import docker, cheatset

def gen(doc, begin_mark='Commands'):
    result = []
    flag = False
    for line in doc:
        if line.startswith(begin_mark) or \
                (flag and len(line.strip()) == 0):
            flag = not flag
        elif flag:
            cmd = line.strip().split(" ", 2)
            #print cmd[0], cmd[2]
            result.append((cmd[0], cmd[2]))
    return result


if __name__ == '__main__':
    f = file('Docker.rb', 'w')
    # begin of doc
    f.write("cheatsheet do\n\ttitle 'Docker'\n" +
        "\tdocset_file_name 'Docker'\n" +
        "\tkeyword 'docker'\n" +
        "\tsource_url 'http://cheat.kapeli.com'\n\n")

    # contents
    doc = docker('--help')
    result = gen(doc)

    for cmd, note in result:
        f.write("\tcategory do\n")
        f.write("\t\tid '" + cmd + "'\n\n")

        # category notes
        f.write("\t\tentry do\n")
        f.write("\t\t\tnotes \"__" + note.strip() + "__\"\n")
        f.write("\t\tend\n\n")
        
        # sub options
        doc = docker(cmd, '--help')
        r = gen(doc, "Options")
        for option, sub_note in r:
            f.write("\t\tentry do\n")
            f.write("\t\t\tname \"" + option.strip() + "\"\n")
            f.write("\t\t\tnotes \"\n")
            f.write("\t\t\t```\n")
            f.write("\t\t\t\t" + sub_note.strip().replace("\"", "\\\"") + "\n")
            f.write("\t\t\t```\"\n")
            f.write("\t\tend\n")

        f.write("\tend\n\n")
            #print cmd, note
            #doc = docker(cmd, '--help')
            #gen(doc, 'Options')

    # end of doc
    f.write("\tnotes <<-'END'\n" +
        "\t\t* Converted and extended by " +
        "[jhezjkp](https://github.com/jhezjkp)." +
        "\n\tEND\n\nend""")
    f.close()

    # gen preview cheatset
    cheatset("generate", f.name)
