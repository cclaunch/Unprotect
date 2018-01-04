__author__ = 'Carl Claunch'
import easygui

def SplitDiskAddr(daddr):
    # provide a two byte field, in little endian format
    # that provides a real disk address
    #     sector is first 4 bits of the second word
    #     Head is next to last bit of the first word
    #     track is the sum of the first 5 bits of the
    #     first word plus 32 times the bottom 4 bits
    #     of the second word
    #
    #     returns tuple of track#, head#, sector#
    Sector = daddr[1]//16
    Head = (daddr[0] & 4) // 4
    Track =  daddr[0] // 8
    Track += (daddr[1] & 15) * 32
    return (Track, Head, Sector)

def DoDiskSeek(disk, Track, Head, Sector):
    # will seek the file 'disk' to the location
    # in the file corresponding to the track
    # head and sector of the disk file
    newsect = Track * 24 + Head * 12 + Sector
    disk.seek(newsect*modulo+6)
    return

path = easygui.fileopenbox()
print('Removing protection from file',path)
disk = open(path,'rb+')

modulo = 534

# seek to absolute sector 1, first word of data record
# which is page 1 of Sys.Boot
Track = 0
Head = 0
Sector = 0
DoDiskSeek(disk,Track,Head,Sector)
label = disk.read(16)

# jump to page 2 of Sys.Boot file
(Track, Head, Sector) = SplitDiskAddr(label[0:2])
DoDiskSeek(disk,Track,Head,Sector)
label = disk.read(16)

# skip over words we don't need until we get to the password block
disk.read(256)
zap = disk.tell()

# read in password block
(pflaga, pflagb) = disk.read(2)

if pflaga == 255 and pflagb == 255:
    print('This is a password protected disk')
    disk.seek(zap)
    pflaga = 0
    disk.write(pflaga.to_bytes(2, byteorder='big'))
    print('The cartridge is now unprotected')
else:
    print('This cartridge was not password protected')
disk.close()

