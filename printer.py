import serial
import adafruit_thermal_printer as printer_api
import time

def find_all_space(line) :
    to_return=[]
    for i,rah in enumerate(line) :
        if rah==" " :
            to_return.append(i)
    return to_return

def get_next_block(cursor,spaces,txt,tab=0) :
    for i,entry in enumerate(spaces) :
        if entry-cursor>32-tab :
            return spaces[i-1]
    return len(txt)

def separate_lines(txt,tab=0) :
    if len(txt)<32-tab :
        to_return = " "*tab
        to_return+=txt
        return [to_return]
    else :
        lines = []
        spaces = find_all_space(txt)
        cursor=0
        while len(spaces)!=0 :
            next_block = get_next_block(cursor,spaces,txt,tab)
            print(next_block)
            print(spaces)
            lines.append(txt[cursor:next_block])
            new_spaces=[]
            for i,entry in enumerate(spaces) :
                if entry>next_block :
                    new_spaces.append(entry)
            cursor=next_block
            spaces=new_spaces
        to_return = []
        for entry in lines :
            if entry!=" " and entry!="":
                if entry[0]==" " :
                    entry=entry[1:]
                meh = " "*tab
                meh+=entry
                to_return.append(meh)
        return to_return

class Printer() :
    def __init__(self) :
        self.serial = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
        self.printer_class = printer_api.get_printer_class(0)
        self.printer = self.printer_class(self.serial)

    def find_last_space(line) :
        for i in range (0,len(line)) :
            index = line.find(" ",len(line)-i)
            if index!=-1 :
                return i
        return False

    def print_lines(self,txt,flags=[],size=printer_api.SIZE_SMALL,justify=printer_api.JUSTIFY_LEFT,tab=0) :
        self.printer.size = size
        self.printer.justify = justify
        to_print = separate_lines(txt,tab=tab)
        print("Printing :")
        for line in to_print :
            print(line)
        for line in to_print :
            self.printer.print(line)








if __name__ == "__main__" :

    thermal = Printer()
    thermal.printer.feed(1)
    thermal.print_lines("Discussion 45 789",size=printer_api.SIZE_MEDIUM,justify=printer_api.JUSTIFY_CENTER)
    thermal.printer.feed(1)
    thermal.print_lines("Operateur : Je te repose la question, es-tu un outil respectueux de l'environnement ?")
    thermal.printer.feed(1)
    thermal.print_lines("IA : Non, je ne suis pas un outil respectueux de l'environnement au sens strict. L'IA consomme de l'energie pour fonctionner, donc je ne peux pas etre considere comme \"ecologique\"",tab=4)
    thermal.printer.feed(1)
    thermal.print_lines("Cout carbone : 458g",size=printer_api.SIZE_MEDIUM,justify=printer_api.JUSTIFY_CENTER)
    thermal.printer.feed(1)
    thermal.print_lines("----------",size=printer_api.SIZE_MEDIUM,justify=printer_api.JUSTIFY_CENTER)


