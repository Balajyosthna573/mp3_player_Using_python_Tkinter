from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root = Tk()
root.title("Audio Player")
root.geometry("600x500")


pygame.mixer.init()

def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

def play_time():
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    song = playlist.get(ACTIVE)
    song = f'C:/Users/80e300-G50/PycharmProjects/mp3_player/music/{song}.mp3'
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length

    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    if int(song_slider.get()) == int(song_length):
        stop()

    elif paused:
        pass
    else:
        next_time = int(song_slider.get()) + 1
        song_slider.config(to=song_length, value=next_time)

        converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

    if current_time>0:
        status_bar.config(text=f'Time Elapsed: {converted_current_time} : {converted_song_length }')
    status_bar.after(1000, play_time)


def slide(x):
    song = playlist.get(ACTIVE)
    song = f'C:/Users/80e300-G50/PycharmProjects/mp3_player/music/{song}.mp3'

    pygame.mixer.music.load(song)

    pygame.mixer.music.play(loops=0, start=song_slider.get())


def add_song():
    song = filedialog.askopenfilename(initialdir="music/", title="Choose A song", filetypes=(("mp3 Files", "*.mp3"),))
    song = song.replace("C:/Users/80e300-G50/PycharmProjects/mp3_player/music/", "")
    song = song.replace(".mp3", "")
    playlist.insert(END, song)

def add_many_song():
    songs = filedialog.askopenfilenames(initialdir="music/", title="Choose A song", filetypes=(("mp3 Files", "*.mp3"),))

    for song in songs:
        song = song.replace("C:/Users/80e300-G50/PycharmProjects/mp3_player/music/", "")
        song = song.replace(".mp3", "")
        playlist.insert(END, song)

def delete_song():
    playlist.delete(ANCHOR)

def delete_all_songs():
    playlist.delete(0, END)

def play():
    global stopped
    stopped = False
    song = playlist.get(ACTIVE)
    song = f'C:/Users/80e300-G50/PycharmProjects/mp3_player/music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()


global stopped
stopped = False
def stop():

    pygame.mixer.music.stop()
    playlist.selection_clear(ACTIVE)
    status_bar.config(text=f'Time Elapsed: 00:00 : 00:00 ')
    song_slider.config(value=0)
    global stopped
    stopped = True

global paused
paused = False
def pause(is_paused):

    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


def next_song():
    status_bar.config(text='')
    song_slider.config(value=0)
    next_one = playlist.curselection()
    next_one = next_one[0] + 1
    song = playlist.get(next_one)
    song = f'C:/Users/80e300-G50/PycharmProjects/mp3_player/music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0, END)
    playlist.activate(next_one)
    playlist.selection_set(next_one, last=None)


def previous_song():
    status_bar.config(text='')
    song_slider.config(value=0)
    previous_one = playlist.curselection()
    previous_one = previous_one[0] - 1
    song = playlist.get(previous_one)
    song = f'C:/Users/80e300-G50/PycharmProjects/mp3_player/music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0, END)
    playlist.activate(previous_one)
    playlist.selection_set(previous_one, last=None)



main_frame = Frame(root)
main_frame.pack(pady=40)
playlist = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
playlist.grid(row=0, column=0)

volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=2, padx=16 )

volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient = VERTICAL, value=1, command=volume)
volume_slider.pack(pady=25)

song_slider = ttk.Scale(main_frame, from_=0, to=100, orient = HORIZONTAL, value=0, length=360,  command=slide)
song_slider.grid(row=3, column=0, pady=20)


backward_img = PhotoImage(file='images/back50.png')
forward_img = PhotoImage(file='images/forward50.png')
play_img = PhotoImage(file='images/play50.png')
pause_img = PhotoImage(file='images/pause50.png')
stop_img = PhotoImage(file='images/stop50.png')


frame = Frame(main_frame)
frame.grid(row=2, column= 0)

backward = Button(frame, image=backward_img, borderwidth=0, command = previous_song)
forward = Button(frame, image=forward_img, borderwidth=0, command = next_song)
play = Button(frame, image=play_img, borderwidth=0, command=play)
pause_btn = Button(frame, image=pause_img, borderwidth=0, command=lambda: pause(paused))
stop = Button(frame, image=stop_img, borderwidth=0, command=stop)

backward.grid(row=0, column=0, padx=10, pady=20)
forward.grid(row=0, column=1, padx=10, pady=20)
play.grid(row=0, column=2, padx=10, pady=20)
pause_btn.grid(row=0, column=3, padx=10, pady=20)
stop.grid(row=0, column=4, padx=10, pady=20)

menu = Menu(root)
root.config(menu=menu)



add_song_menu = Menu(menu,tearoff=0)
menu.add_cascade(label="Choose Songs", menu=add_song_menu)
add_song_menu.add_command(label="Select", command=add_song)
add_song_menu.add_command(label="Select All", command=add_many_song)

remove_song_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete", command=delete_song)
remove_song_menu.add_command(label="Delete all", command=delete_all_songs)

status_bar = Label(root, text="", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

label = Label(root, text="")
label.pack(pady=20)


root.mainloop()