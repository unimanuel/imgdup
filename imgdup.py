import os
import shutil #for copying files

# for testing without input
# prefix = 'depth'
# updown = True
# multiple = 4

def calcNewNumUpDown(num, listlen, multiple, up):
    newnums = []
    if (not up): #count back down
        for i in range(multiple):
            if (i % 2 == 1):
                newnum = listlen + listlen * (i)  - num - 1
                newnums.append(newnum)
            else:
                newnum = num + listlen * (i)
                newnums.append(newnum)
    return newnums
    
def calcNewNumRepeat(num, listlen, multiple, up):
    newnums = []
    for i in range(multiple):
        newnum = num * multiple + i
        newnums.append(newnum)
    return newnums

def getListDir(filetypeending):
    listdir1 = os.listdir()
    # Use only png filenames
    imglistdir1 = [i for i in listdir1 if i.partition('.')[2] == filetypeending]
    return imglistdir1

#Get info from user
revertinp = input("Revert renames? (yes/no):")
if revertinp.lower() == 'yes' or revertinp.lower() == 'y':
    filetypeendinp = input("Enter file ending (png/jpg):")
    filetypeend = filetypeendinp.lower()
    prefixinp = input("Enter original file prefix:")
    revert = True
    prefix = prefixinp.lower()
    updown = '__'
    multiple = '___'
else:
    revert = False
    filetypeendinp = input("Enter file ending (png/jpg):")
    filetypeend = filetypeendinp.lower()
    prefixinp = input("Enter file prefix:")
    orderinp = input("Enter updown or repeat:")
    multipleinp = input("Enter multiplier:")
    prefix = prefixinp.lower()
    updown = True if orderinp.lower() == 'updown' else False
    multiple = int(multipleinp)

print('filetypeend:',filetypeend)
print('prefix:',prefix)
print('updown:',updown)
print('multiple:',multiple)

if (revert):
    print('About to proceed with renaming files to revert old_ prefix. Make sure original filenames are available!')
else:
    print('About to proceed with renaming and copying files.')
areyousureinp = input("Are you sure? (yes/no):")
if areyousureinp.lower() != 'yes' and areyousureinp.lower() != 'y':
    print('Terminating program...')
    exit()
    
# get file list
imglistdir = getListDir(filetypeend)
imglistdirlen = len(imglistdir)
print('imglistdirlen:', imglistdirlen)

print('renaming files...')
for suffile in imglistdir:
    fileb4period, period, suf = suffile.partition('.')[0:3]
    if (suf != filetypeend):
        print('rename ignoring:',suffile)
        continue
    prepre, pre, numstr = fileb4period.partition(prefix)
    if (revert):
        if (prepre == 'old_'):
            os.rename(suffile, fileb4period[4:] + period + suf) #revert old rename
    else:
        os.rename(suffile, 'old_' + fileb4period + period + suf) #rename to old
    
if (revert):
    print('Revert finished. Terminating program...')
    exit()
# refresh file list because of above renames.
imglistdir = getListDir(filetypeend)
imglistdirlen = len(imglistdir)
print('imglistdirlen', imglistdirlen)

newprefix = 'old_' + prefix
print('creating new files...')
for suffile in imglistdir:
    print(suffile)
    fileb4period, period, suf = suffile.partition('.')[0:3]
    if (suf != filetypeend):
        print('ignoring:',suffile)
        continue
    prepre, pre, numstr = fileb4period.partition(newprefix)
    print('numstr',numstr)
    numlen = len(numstr)
    num = int(numstr)
    if (len(prepre) > 0):
        print('prepre',prepre)
        raise Exception("There is a string before", newprefix)
    if (updown):
        print('full filename:', suffile,'updown mode...')
        newfilenums = calcNewNumUpDown(num, imglistdirlen, multiple, False)
        for newfilenum in newfilenums:
            newfilename = prefix + str(newfilenum).zfill(numlen) + '.' + filetypeend
            print('copying to newfilename', newfilename)
            shutil.copy2(suffile, newfilename) #copy2 keeps metadata
    else: #repeat same file next to each other
        print('full filename:', suffile, 'repeat mode...')
        newfilenums = calcNewNumRepeat(num, imglistdirlen, multiple, False)
        for newfilenum in newfilenums:
            newfilename = prefix + str(newfilenum).zfill(numlen) + '.' + filetypeend
            print('copying to newfilename', newfilename)
            shutil.copy2(suffile, newfilename) #copy2 keeps metadata
print('End of line.')
    
