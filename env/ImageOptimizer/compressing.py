from __future__ import print_function
import os
import sys


from werkzeug.utils import secure_filename
from PIL import Image
from tinify import tinify
from flask import Flask , render_template , request, send_file, send_from_directory

tinify.key = "KHdQmr04kWs6b4tfpm5bYgQHVzVTBS3v"
filed=''

app = Flask(__name__)   #web is apppip install --upgrade tinify

@app.route('/')  #end point   #staic is public template is not

def bootstrap():
 
    return render_template('upload.html')
@app.route('/uploader', methods=['GET', 'POST'])  #end point
def upload():
    global filed
    if request.method == "POST":
        f=request.files.getlist('file1')
        #f.save(f.filename)
        g=request.form.get('Services')
        h=request.form.get('height')
        w=request.form.get('width')
        q=request.form.get('quality')
        print(g)
       
        
        if g=="Hosted":
            cop=request.form.get('tservice')
            if cop=="Compress":
                filed=Hostoptcomp(f,q)
                
            
            if cop=="Resize":
                filed=Hostoptres(f,h,w,q)
           
            
            
        if g=="Tinify":
            cop=request.form.get('tservice')
            if cop=="Compress":
                filed=Tinicompopt(f)
                
                
            
            if cop=="Resize":
                cop=request.form.get('tservice')
                filed=Tiniresopt(f,h,w)

        
               
        return download_file(filed)
        
def Tinicompopt(f):
    tinify.key = "KHdQmr04kWs6b4tfpm5bYgQHVzVTBS3v"
    for x in range(0,len(f)):
    
    
        result = f[x].filename[::-1].find('/')
        typ=f[x].filename[-3:]
        typ=typ.lower()
        print(typ)
        o=f[x].filename[-result-1:-4]+ "."+typ
    
            
      
        source =tinify.from_file(path=f[x])
        source.to_file(o)
        return  o
                

def Tiniresopt(f,h,w):
    tinify.key = "KHdQmr04kWs6b4tfpm5bYgQHVzVTBS3v"
    h=int(h)
    w=int(w)
    for x in range(0,len(f)):
    
        result = f[x].filename[::-1].find('/')
        typ=f[x].filename[-3:]
        typ=typ.lower()
        print(typ)
        o=f[x].filename[-result-1:-4]+"."+typ
            
            
        source = tinify.from_file(path=f[x])
        if (h!=0 and w!=0):
            resized = source.resize(
                method="fit",
                width=w,
                height=h
            )

        else:
            resized = source.resize(
                method="fit",
                width=150,
                height=100
            )
        resized.to_file(o)
        return o
def Hostoptres(f,h,w,q):
    h=int(h)
    w=int(w)
    q=int(q)
    for x in range(0,len(f)):
        result = f[x].filename[::-1].find('/')
        typ=f[x].filename[-3:]
        typ=typ.lower()
        print(typ)
        o=f[x].filename[-result-1:-4]+"."+typ
        im = Image.open(f[x])
        print('o')
        print(im.format, im.size, im.mode)
        y=im.size
        print(y[0])
        if (h!=0 and w!=0):
            foo = im.resize((int(h),int(w)),Image.ANTIALIAS)
        else:
            foo = im.resize((int(y[0]*0.5),int(y[1]*0.5)),Image.ANTIALIAS)
        if q==0:
            q=70
        foo.save(o,optimize=True,quality=q)
        return o
def Hostoptcomp(f,q):
    q=int(q)

    for x in range(0,len(f)):
    
    
        result = f[x].filename[::-1].find('/')
        typ=f[x].filename[-3:]
        typ=typ.lower()
        print(typ)
        o=f[x].filename[-result-1:-4]+"."+typ
        im = Image.open(f[x])
        if q==0:
            q=70
        
        im.save(o,optimize=True,quality=q) 
        return o

            
       

@app.route('/download')
def download_file(filed):
    return send_from_directory(directory='../../', filename=filed, as_attachment=True )

    #return send_file(filed,as_attachment=True)
    
    
    


app.run(debug=True)
