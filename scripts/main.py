from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from getid import getid
from getdir import getdir
from doi_to_bt import doi_to_bt

import os, sys

sys.path.append(os.path.abspath('..'))

Builder.load_file('screens/main.kv')

class MenuScreen(Screen):

    pass

class Add_new_note(Screen):

    pass

class Set_new_dir(Screen):

    pass

sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(Add_new_note(name='add_note'))
sm.add_widget(Set_new_dir(name='set_dir'))

class kvApp(App):

    def build(self):

        return sm

    def save_dir(self, dir):

        makedir = open('dir.txt','w')

        dir = dir.strip()
        if dir[-1] == "/":
            makedir.write(dir)
        else:
            makedir.write(dir + "/")
        makedir.close()

    def make_toc(self):

        contents = open(getdir() + "Contents.md", 'w')
        files = os.listdir(str(getdir()))

        contents.write("#### Contents" + '\n\n')

        for i in files:
            doc_to_read = open(getdir() + i, 'r').read()
            doc_to_read = doc_to_read.split('\n\n')[0][5:]
            title = doc_to_read.split('\n2')

            id = [int(s) for s in doc_to_read.split() if s.isdigit()]

            if id:
                id.sort()
                id = id[-1]
                contents.write(title[0] + "\n" + '[[' + str(id) + ']]' + "\n\n")

        contents.close()

    def save_dc(self, name, note, extension, keys, doi, autolink):

        id = getid()
        name = name.strip()
        extension = extension.strip()
        keys = keys.strip()

        if doi:

            name = "[A] " + name
            dc = open(getdir() + name + "." + extension, 'w')
            dc.write("#### " + name + '\n' + id)
            #if doi.strip() != "":
            dc.write('\n\n' + "##### " + doi_to_bt(doi))
            dc.write('\n\n' + "##### " + '\n\n' + note + '\n\n' + "##### Links" + '\n')

        else:

            dc = open(getdir() + name + "." + extension, 'w')
            dc.write("#### " + name + '\n' + id + '\n\n' + "##### " + '\n\n' + note \
                     + '\n\n' + "##### Links" + '\n')

        dc.close()

        keys = list(keys.split(','))
        keys = [s.strip() for s in keys]
        keys = [s.lower() for s in keys]

        if autolink and keys:

            for key in keys:

                contents = os.listdir(str(getdir()))

                dc = open(getdir() + name + "." + extension, 'r').read()

                for x in contents:

                    doc_to_read = open(getdir() + x, 'r').read()

                    if key and (str(key) in doc_to_read.lower()) and (str(id) not in doc_to_read) \
                            and (dc.split('\n')[0][5:] not in doc_to_read) and \
                            (doc_to_read.split('\n')[0][5:] != "Contents"):

                        ## Adds current link to all existing documents with keys

                        doc_to_write = open(getdir() + x, 'a')
                        doc_to_write.write('\n' + "[[" + id + "]]" + " -- " + dc.split('\n')[0][5:])
                        doc_to_write.close()

                        ## Adds links of all existing documents with keys to current document

                        doc_to_read_id = doc_to_read.split('\n')[1]

                        dc_link_all = open(getdir() + name + "." + extension, 'a')
                        dc_link_all.write('\n' + doc_to_read_id + " -- " + doc_to_read.split('\n')[0][5:])
                        dc_link_all.close()

if __name__ == '__main__':
    kvApp().run()