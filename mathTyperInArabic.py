from PIL import Image , ImageDraw , ImageFont #6.1.0
import os, sys, re, time
from random import randint,choice
from resizeimage import resizeimage


class paper():
    def __init__(self):
        self.arabic ={"0":"٠","1":"١","2":"٢","3":"٣","4":"٤","5":"٥","6":"٦","7":"٧","8":"٨","9":"٩","*":"×","x":"س","y":"ص"}
        
        self.A4 = 2480, 3508
        self.vsmfnt = ImageFont.truetype(os.path.join(os.getcwd()+ "\\ar.ttf") , 50)
        self.smfnt = ImageFont.truetype(os.path.join(os.getcwd()+ "\\ar.ttf") , 75)
        self.fnt = ImageFont.truetype(os.path.join(os.getcwd()+ "\\tst.ttf") , 130)         #// the original used font.
        self.img = Image.new(mode = 'RGBA' , size = self.A4 , color = "white")    
        self.draw = ImageDraw.Draw(self.img)
        
        self.replace = lambda dict, text: re.sub("|".join(map(re.escape, dict.keys())),
                 lambda m: dict[m.string[m.start():m.end()]],
                 text)
        self.draw.rectangle([(0,0), (2300,500)], outline="black", width=1)
        
        self.uniqued = {0:0}       #don't change it.
        self.uniquen = {0:0}        #don't change it.
        self.d_sign_width = 0   #don't change it.
        self.simple_eq_size = (0,0) #don't change it.
        self.dominsaver = False #don't change it.
        self.width_cyborg = 0   #don't change it.
        self.sqrt_width = 0  #don't change it.
        self.last = ''
    def robot(self, pos, formula, commander="", hmargin=10,cage=False,show=False):
        sorted = self.sorter(formula)
        #print(sorted)
        container = []
        for i in sorted:
            if i[:2] =="f(":
                if commander=="":
                    try:
                        self.fraction( (pos[0]-self.width_cyborg, pos[1]) , i, commander)
                        self.width_cyborg += self.d_sign_width + hmargin
                    except:
                        print("probably, the formula is incorrect!")
                        sys.exit()
                else:
                    if len(sorted) ==1: return self.fraction(pos, i, commander)
                    container.append(("f", self.fraction(pos, i, commander), i))
            elif i[:2] == "s(":
                if commander =="":
                    try:
                        self.root( (pos[0]-self.width_cyborg, pos[1]), i, commander)
                        self.width_cyborg += self.sqrt_width + hmargin
                    except:
                        print("probably, the formula is incorrect!")
                        sys.exit()
                else:
                    if len(sorted) ==1: return self.root(pos, i, commander)
                    container.append(("s", self.root(pos, i, commander), i))
            else:
                if commander == "":
                    self.simple( (pos[0]-self.width_cyborg, pos[1]+self.simple_eq_size[1]//4+2), i, commander)
                    self.width_cyborg += self.simple_eq_size[0]+hmargin
                else:
                    if len(sorted) ==1: return self.simple(pos, i, commander)
                    container.append(("n", self.simple(pos, i, commander), i))

        if commander!="":
            return self.merger(*container)

 
        if show:
            self.img.save("test.png")
            os.startfile("test.png")
    
    def merger(self, *args, margin_top=-9, margin_center=10):
        #print(self.uniquen)
        #print([i for i in max(self.uniqued.values())])
        height = max([i for i in self.uniquen.values()])+max([i for i in self.uniqued.values()])

        size = (sum([i[1].size[0] for i in args]+[margin_center*(len(args)-1)]), height)
        pos = size[:]
        margin_r = 0
        Img = Image.new(mode = "RGBA" , size = size , color="red").copy()
        Img.putalpha(0)
        Draw = ImageDraw.Draw(Img)
        for i in args:
            margin_r += i[1].size[0]+margin_center
            #if i[0] == "s":Img.paste(i[1], (pos[0]-margin_r, 0), i[1])

            if i[0] == "s":

                Img.paste(i[1], (pos[0]-margin_r, size[1]-max(self.uniqued.values())-self.uniquen[i[2]]), i[1])

            elif i[0] == "f":Img.paste(i[1], (pos[0]-margin_r, size[1]-max(self.uniqued.values())-self.uniquen[i[2]]), i[1])
            else:Img.paste(i[1], (pos[0]-margin_r, size[1]-max(self.uniqued.values())-i[1].size[1]//2+margin_top), i[1])
        self.uniqued = {0:0}
        self.uniquen = {0:0}
        return Img

    def cage(self, size, *args, show=False, debug=False):
        """
            simply this function is only for merging many fragments of math function
            into one holdable piece so it be easier to use it over the different places
            in math as using root over a fraction as example. 
            > size  : size of the container box.
            > *args : the fragments that forms the after all formula.

        """
        col = "red"
        if debug:
            def rando():
                c = choice(["red", "green", "blue", "yellow", "orange", "gray", "purple"])
                return c if c!= self.last else rando()
            col = rando()
            self.last = col


        Img = Image.new(mode = "RGBA" , size = size , color=col)
        if not debug:Img.putalpha(0)
        Draw = ImageDraw.Draw(Img)
        for i in args:
            if i[0] == "p":
                Img.paste(*i[1:])
            else:
                Draw.text(*i[1:])
        if show:
            Img.save("test.png")
            os.startfile("test.png")
        return Img


    def sorter(self, formula, s=0):
        """
            formula : the target formula to be parsed.
            s, e : just a initiate values [don't change it ever].
            res : just a container of all results [don't change it ever].
        """
        e, res = len(formula), [] # just to clear the list.
        iseven = lambda s:True if s.count("(") == s.count(")") else False
        crack =lambda s: re.search("([fs]\(.*\)|[0-9½+\-*]|[abxyz])" ,s)
        def recursion(formula, s):
            # this is a contained recursion function .
            for i in range(s, e+1):
                if iseven(formula[s:i]) and crack(formula[s:i]):
                    match = crack(formula[s:i])
                    res.append(match[0])
                    recursion(formula, i)
                    break
        recursion(formula, s)
        ### merging normal (+ - * 0-9)  formulas ###
        f, tmp= [], []
        for i, j in enumerate(res):
            if j.count("(") != 0:
                if len(tmp)>0:f.append("".join(tmp))
                f.append(j)
                tmp= []
            else:
                tmp.append(j)
                if i == len(res)-1 and len(tmp)>0:f.append("".join(tmp)) #ending case
        if len("".join(f)) != len(formula):print("the outcome != the income, Fix me!")
        return f 
    def fixp(self, pos, txt="1", size=(0,0), size_given=False):
        """
            pos: the targeted position u want to write text on.
            txt: the desired text u want to be written.
            Debug: it's just for testing purposes don't turn it on.
            return [(the fixed position), (the text real size)]
        """
        txt = self.replace(self.arabic, txt)                         #this step translates the numbers to arabic .#this size contains extra offsets .
        raw_size = self.draw.textsize(text=txt, font=self.fnt) if not size_given else size
        offset = self.fnt.getoffset(txt) 
        real_size = (raw_size[0]-offset[0], raw_size[1]-offset[1])

        return  [(pos[0]-raw_size[0], pos[1]-raw_size[1]), real_size]

    def simple(self, pos, formula, commander="", margin_top=0):
        formula = "".join(re.findall("[0-9]+|[+\-*]+|[½]|[abxyz]", formula)[::-1]) #fix into arabic order
        formula = self.replace(self.arabic, formula)
        size = self.draw.textsize(text=formula, font=self.fnt)
        self.simple_eq_size = size
        if commander != "":
            return self.cage(size, ["t", (0,0), formula, "black", self.fnt])
        pos = self.fixp((pos[0], pos[1]+margin_top), formula)[0]
        self.draw.text(pos, text=formula, fill="black", font=self.fnt )

    def fraction(self, pos, frac="(1+2)/(3*2)", commander='', allow_scalling=True, n_margin=0, d_margin=0):
        """
                     >> tutorial: <<
            pos               : position for writing .
            frac              : pure fraction fourmela. ex:"5+5/3*4".
            n_margin, d_margin: numerator & denominator margins from the division sign.       ##### fix it make it auto detected.
            return_only_width : True to return only width of fraction.
            nw, nd, dsign     : numerator & denominator & division sign widths.
            length            : division sign length.
            
        """

        nd = frac.split("/")

        for i,j in enumerate(nd):
            leven = lambda x: True if x.count("(")-x.count(")") == 1 else False
            reven = lambda x: True if x.count(")")-x.count("(") == 1 else False
            l, r = "/".join(nd[:i+1]), "/".join(nd[i+1:])
            if leven(l) and reven(r):n, d= l[2:], r[:-1]


        nc, dc = n, d

        ###########################
        if self.dominsaver:
            n_margin = n_margin
            d_margin = d_margin
        elif not self.dominsaver: #especial case (n_margin & d_margin).
            d_margin = 10
            n_margin = 0
            
            self.dominsaver = True
        ###########################
        #print(n)
        n = self.robot((0,0), n, commander="fraction")
        d = self.robot((0,0), d, commander="fraction")

        if nc[:2]=="f(" and allow_scalling:
            nw, nh = n.size[0], n.size[1]
            n = resizeimage.resize_thumbnail(n, [nw-20, nh-20])

        if dc[:2]=="f(" and allow_scalling:
            dw, dh = d.size[0], d.size[1]
            d = resizeimage.resize_thumbnail(d, [dw-20, dh-20])


        def figure(n, d, length): 
            figure.nw = n.size
            figure.dw = d.size
            figure.dsign = self.draw.textsize(text='_'*length, font=self.fnt)
            return length if figure.dsign[0] > max([figure.nw[0], figure.dw[0]]) else figure(n, d, length+1)
        
        length = figure(n, d, 1)

        self.d_sign_width = figure.dsign[0]

        size = (self.draw.textsize(text='_'*length, font=self.fnt)[0], figure.nw[1]+figure.dw[1]+n_margin+d_margin)
        nf, df = ((figure.dsign[0]-figure.nw[0])//2, 0), ((figure.dsign[0]-figure.dw[0])//2,figure.nw[1]+n_margin+d_margin)
        
        #if commander=="fraction0":df = ((figure.dsign-figure.dw[0])//2,figure.nw[1]+n_margin+d_margin)

        if nc[:2]=="f(":nf = ((figure.dsign[0]-figure.nw[0])//2, 0)

        ds_offset = self.fnt.getoffset( "_"*length) #(devision sign) this is pain in the ass, screw it.
        frac = self.cage(size, ["p", n, nf, n], ["p", d, df, d], ["t", (0, figure.nw[1]+n_margin-ds_offset[1]), "_"*length, "black", self.fnt], show=False)
        if commander != "":
            self.uniqued["f("+nc+"/"+dc+")"] = figure.dw[1]+d_margin
            self.uniquen["f("+nc+"/"+dc+")"] = figure.nw[1]+n_margin
            return frac

        pos = (pos[0]-figure.dsign[0], pos[1]-figure.nw[1]-n_margin-figure.dsign[1]+ds_offset[1])
        self.img.paste(frac,pos, frac )


    def root(self, pos, formula, commander="", Parenthesis=True, sqrt="\u00BD", d_s_margin_fixer=3,  uder_root_margin_right= 20,margin_top=25):
            """
                pos         : ect..
                formula        : formula of the root
                margin_top  : margin space to top.
                Parenthesis : ect.
                return_only_width : ect..
                sqrt              : sqrt sign (don't change it) default= "\u00BD".
            """
            formula = formula[2: -1]
            pos = pos[0], pos[1]+margin_top

            cformula = formula
            formula = self.replace(self.arabic, formula)[::-1]
            if Parenthesis:formula=self.replace({"(":")",")":"("}, formula) #fix Parenthesis
            else:formula=formula.replace("(","").replace(")","")            #remove Parenthesis
            
            formula = formula[2: -1]
            formula = self.robot((0,0), cformula, commander="root")
            sqrt_sign = self.robot((0,0), sqrt, commander="root")

            def figure(formula, n):
                figure.sqrt = self.draw.textsize(text=sqrt, font=self.fnt)
                figure.formw = formula.size
                figure.ceilw = self.draw.textsize(text="_"*n, font=self.fnt)
                return n if figure.ceilw[0] > figure.formw[0] else figure(formula, n+1)
            length = figure(formula, 1)
            self.sqrt_width = figure.ceilw[0]+figure.sqrt[0]
            
            height = figure.sqrt
            
            
            if figure.sqrt[1] < formula.size[1]:
                fsize = formula.size
                ssize = sqrt_sign.size
                sqrt_sign = sqrt_sign.resize((ssize[0],fsize[1]), Image.ANTIALIAS)
                height = fsize[1]

            size = (figure.ceilw[0]+figure.sqrt[0]+20, height+20)
            
            sqrtp = (size[0]-sqrt_sign.size[0], size[1]-sqrt_sign.size[1])
            divsignp = (size[0]-sqrt_sign.size[0]-figure.ceilw[0], size[1]-sqrt_sign.size[1]-figure.ceilw[1]+d_s_margin_fixer)
            
            formulap = (size[0]-sqrt_sign.size[0]-formula.size[0]-uder_root_margin_right, size[1]-formula.size[1])
            root=   self.cage(
                                    size,
                                    ["p", sqrt_sign, sqrtp, sqrt_sign],
                                    ["t", divsignp, "_"*length, "black", self.fnt],
                                    ["p", formula, formulap, formula]
                                )
            ceil_offset = self.fnt.getoffset("_"*length)

            if commander != "":
                try:
                    self.uniqued["s("+cformula+")"] = self.uniqued[cformula]+figure.ceilw[1]-ceil_offset[1] 
                    self.uniquen["s("+cformula+")"] = self.uniquen[cformula] +margin_top
                except:
                    pass
                return root

            pos = self.fixp(pos, size=size, size_given=True)[0]
            pos = (pos[0], pos[1]+root.size[1]//4)
            self.img.paste(root, pos, root) #i struggled a lot at this pathetic step xD
            




        




if __name__ == "__main__":

    #paper().robot((2300,500), "f(s(f(x/f(5*9/s(25))))/2)+s(f(25/55))", show=True)
    #paper().robot((2300,500), "f(s(f(44x/f(1/8)))+f(1/3)/55y)", show=True)
    #paper().robot((2300,500), "f(1/f(1/2))55y+s(25)", show=True)
    paper().robot((2300,500), "f(f(1/f(1/9)+f(1/f(1/9)))+f(1/2)/f(1/f(1/9)+f(1/f(1/9)))+f(1/2))", show=True)
    #paper().robot((2300,500), "54+s(25)", show=True)
