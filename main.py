from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import Entry
from tkinter import filedialog as fd
from tkinter.filedialog import askopenfile,asksaveasfilename
import tkinter as tk
import tkinter.font as font
import time
import os
from matplotlib import pyplot as plt
plt.style.use("ggplot")
import numpy as np
import csv 
import datetime

#Initial HMS variables
timeHours, timeMinutes, timeSeconds = 0, 0, 0
# Initial number of displayCounter instances
instances = 0

class Acc_Tool(object):
	def motivation_button(self):
		self.motivation_label=Label(self.selection_frame, text="Motivation: ")
		self.motivation_label.grid(column=2, row=2,padx=5)
		
		self.motivation_menu = Menubutton(self.selection_frame, text="Menu: ")
		self.motivation_menu.grid(column=2, row=2, padx=5)
		self.motivation_menu.menu = Menu(self.motivation_menu)
		self.motivation_menu["menu"]= self.motivation_menu.menu

		self.motivation_menu.menu.add_command(label="Quotes", command= self.quotes)
		self.motivation_menu.menu.add_command(label="Sleep", command= self.sleep)

	def activity_button_menu(self):
		self.activity_label=Label(self.selection_frame, text= "Activities: ")
		self.activity_label.grid(column=0, row=2, padx=5)

		self.activity_menu = Menubutton(self.selection_frame, text="Menu: ")
		self.activity_menu.grid(column=1, row=2, padx=5)
		self.activity_menu.menu = Menu(self.activity_menu)
		self.activity_menu["menu"]= self.activity_menu.menu

		self.activity_menu.menu.add_command(label="Reading", command= self.reading)
		self.activity_menu.menu.add_command(label="Programming", command= self.coding)
		self.activity_menu.menu.add_command(label="Exercising", command= self.exercising)

	def reading(self):
		self.reading_label= Label(self.selection_frame,foreground="red",text="Reading Option: ")
		self.reading_label.grid(column=0,row=3,padx=5)

		self.reading_menu = Menubutton(self.selection_frame, text="Options: ")
		self.reading_menu.grid(column=1, row=3,padx=5)
		self.reading_menu.menu = Menu(self.reading_menu)
		self.reading_menu["menu"]= self.reading_menu.menu

		self.reading_menu.menu.add_command(label="Timer", command=self.pomdoro_timer)
		self.reading_menu.menu.add_command(label="Taking Notes",command=lambda:[self.reading_notes(),self.taking_notes()])

	def coding(self):
		self.coding_label= Label(self.selection_frame,foreground="blue",text="Programming Option: ")
		self.coding_label.grid(column=0, row=6,padx=5)

		self.coding_menu = Menubutton(self.selection_frame, text="Options: ")
		self.coding_menu.grid(column=1, row=6,padx=5)
		self.coding_menu.menu = Menu(self.coding_menu)
		self.coding_menu["menu"]= self.coding_menu.menu

		self.coding_menu.menu.add_command(label="Timer", command=lambda:[self.pomdoro_timer(),self.coding_timer()])
		self.coding_menu.menu.add_command(label="Taking Notes",command=lambda:[self.coding_notes(),self.taking_notes()])
		self.coding_menu.menu.add_command(label="A list of goals",command=self.coding_goals)

	def exercising(self):
		self.exercising_label= Label(self.selection_frame,foreground="green",text="Exercising Option: ")
		self.exercising_label.grid(column=0, row=10,padx=5)

		self.exercising_menu = Menubutton(self.selection_frame, text="Options: ")
		self.exercising_menu.grid(column=1, row=10,padx=5)
		self.exercising_menu.menu = Menu(self.exercising_menu)
		self.exercising_menu["menu"]= self.exercising_menu.menu

		self.exercising_menu.menu.add_command(label="Mobility", command=self.mobility)
		self.exercising_menu.menu.add_command(label="Running", command=self.running)

	def quotes(self):
		self.quotes_window = Toplevel()
		self.quotes_window.title("Quotes Window")
		# how to take a json list maybe 
		# or a regular text file and convert it's contents to a readable list
		# separated with commas or maybe new lines
		# then add this list to text 

		quotes_list= ["Programming testing can be used to show the presence of bugs, but never to show their absence! by Edgar Dijkstra\n\n\n", 
		"No amount of experimentation can ever prove me right; a single experiment can prove me wrong by Alber Einstein"]
		self.quotes_label= Label(self.quotes_window,text=quotes_list)
		self.quotes_label.pack()
	def sleep(self):
		self.sleep_label=Label(self.selection_frame,text="I'll have a sleep function here;timer,and a sys for pc to sleep")
		self.sleep_label.grid(column=2,row=4,padx=5)

	def displayCounter(self):
			self.notifLabel = Label(self.window_timer,text="")
			self.notifLabel.grid(column=2, row=3)
			self.workHours, self.workMinutes, self.workSeconds, self.breakHours, self.breakMinutes, self.breakSeconds = hmsdata
			self.isWorking = True
			self.textNotifData = ('Get to work!', '')
			global timeHours, timeMinutes, timeSeconds
			timeHours, timeMinutes, timeSeconds = self.workHours, self.workMinutes, self.workSeconds
			self.tick()

	# Called once per second
	def tick(self):
		global timeHours, timeMinutes, timeSeconds
		try:
			# if the countdown is running
			if (timeHours >= 0 and timeMinutes >= 0 and timeSeconds >= 0):
				# Here where I stopped 
				# Set the HMS data to be displayed
				self.timeDisplayData = str(timeHours) + ":" + str(timeMinutes) + ":" + str(timeSeconds)
				# Set and display the data
				self.notifString = self.textNotifData[0] + " " + str(self.timeDisplayData)
				self.notifLabel.config(text=self.notifString)
				# If the counter is done
				if (timeHours == 0 and timeMinutes == 0 and timeSeconds == 0):
					# Get data tuple from time_up() function
					self.textNotifData = self.time_up()
					self.isWorking = not self.isWorking
					if(self.isWorking):
						timeHours, timeMinutes, timeSeconds = self.workHours, self.workMinutes, self.workSeconds
					else:
						timeHours, timeMinutes, timeSeconds = self.breakHours, self.breakMinutes, self.breakSeconds
				else:
					if(timeSeconds > 0):
						timeSeconds -= 1
					elif(timeMinutes > 0):
						timeMinutes -= 1
						timeSeconds = 59
					elif(timeHours > 0):
						timeHours -= 1
						timeMinutes = 59
						timeSeconds = 59
		# Print exception if it occurs
		except Exception as e: #ValueError:
			print(e)
		# Use tkinter's after() function to call tick every second
		self.id=self.window_timer.after(1000, self.tick)

	# Set the state according to the isWorking boolean
	def time_up(self):
		self.workHours, self.workMinutes, self.workSeconds, self.breakHours, self.breakMinutes, self.breakSeconds = hmsdata
		# If the user is working
		if self.isWorking == True:
			return ('Take a break!', 'BreakSound')
		# Else, the user is not working
		else:
			return('Get to work!', 'workSound')

	def instantiate_displayCounter(self):
		global instances
		global hmsdata
		hmsdata = [self.workHoursEntry, self.workMinutesEntry, self.workSecondsEntry, self.breakHoursEntry, self.breakMinutesEntry, self.breakSecondsEntry]
		for i, data in enumerate(hmsdata):
			try:
				hmsdata[i] = int(hmsdata[i].get())
			except ValueError:
				hmsdata[i] = 0

		print("Input = " + str(hmsdata))

		# Only allow one instance of the counter
		if(instances == 0):
			d = self.displayCounter()
			instances += 1
		else:
			pass
	
	def quit(self):
		self.window_timer.destroy()

	def pomdoro_timer(self):
		self.read_timer_label= Label(self.selection_frame,text="Started Timer for Reading !")
		self.read_timer_label.grid(column=1, row=4,padx=5)

		self.window_timer = Toplevel()
		self.window_timer.geometry("700x200")
		self.window_timer.title("Pomdoro Timer")

		headLabel = Label(self.window_timer,text="Pomodoro", font=("Times New Roman", 20))
		headLabel.grid(columnspan=7, row=0,)
		workTextLabel = Label(self.window_timer,text="Work length")
		workTextLabel.grid(column=0, row=1)
		breakTextLabel = Label(self.window_timer,text="Break length")
		breakTextLabel.grid(column=0, row=2)
		workHoursLabel = Label(self.window_timer,text="H")
		workHoursLabel.grid(column=1, row=1)
		breakHoursLabel = Label(self.window_timer,text="H")
		breakHoursLabel.grid(column=1, row=2)
		workMinutesLabel = Label(self.window_timer,text="M")
		workMinutesLabel.grid(column=3, row=1)
		breakMinutesLabel = Label(self.window_timer,text="M")
		breakMinutesLabel.grid(column=3, row=2)
		workSecondsLabel = Label(self.window_timer,text="S")
		workSecondsLabel.grid(column=5, row=1)
		breakSecondsLabel = Label(self.window_timer,text="S")
		breakSecondsLabel.grid(column=5, row=2)

		self.workHoursEntry = Entry(self.window_timer)
		self.workHoursEntry.grid(column=2, row=1)
		self.workMinutesEntry = Entry(self.window_timer)
		self.workMinutesEntry.grid(column=4, row=1)
		self.workSecondsEntry = Entry(self.window_timer)
		self.workSecondsEntry.grid(column=6, row=1)
		self.breakHoursEntry = Entry(self.window_timer)
		self.breakHoursEntry.grid(column=2, row=2)
		self.breakMinutesEntry = Entry(self.window_timer)
		self.breakMinutesEntry.grid(column=4, row=2)
		self.breakSecondsEntry = Entry(self.window_timer)
		self.breakSecondsEntry.grid(column=6, row=2)

		#Start Button
		# myFont = font.Font(family='Helvetica', size=20, weight='bold')
		button1 = Button(self.window_timer,text="Start", command=self.instantiate_displayCounter)
		# button1['font'] = myFont
		button1.grid(column=0, row=3)
		# Destroy Button
		button2= Button(self.window_timer,text="Exit", command=self.quit)
		button2.grid(column=0,row=4)

	def reading_notes(self):
		self.reading_label=Label(self.selection_frame,text="Reading Notes")
		self.reading_label.grid(column=1,row=5,padx=5)

	def open_file(self):
		self.blank.delete("1.0", END)
		file = askopenfile(mode= "r", filetypes= [("text files", "*.txt")])
		if file is not None:
			text = file.read()
			self.blank.insert("1.0", text)
	def save_file(self):
		text = self.blank.get("1.0", "end-1c")
		file = asksaveasfilename(title="Save", filetypes=[("text files", "*.txt")])

		with open(file,"w") as data:
			data.write(text)
	def taking_notes(self):
		window = Toplevel()
		window.geometry("700x700")
		window.title("Notes Editor")

		menubar = Menu(window)
		window.config(menu=menubar)

		filemenu = Menu(menubar, tearoff=0)

		menubar.add_cascade(label="File", menu=filemenu)
		filemenu.add_command(label="Open", command=self.open_file)
		filemenu.add_command(label="Save", command=self.save_file)
		filemenu.add_command(label="Exit", command=window.destroy)

		self.blank = Text(window, font=("arail",20))
		self.blank.pack()

	
	def coding_timer(self):
		self.timer_label=Label(self.selection_frame,text="Timer options, 5,10,15,20,25,30,40,50,60")
		self.timer_label.grid(column=1,row=7,padx=5)
	def coding_notes(self):
		self.notes_for_programming=Label(self.selection_frame,text="Coding Notes")
		self.notes_for_programming.grid(column=1,row=8,padx=5)
	def coding_goals(self):
		goals_dictionary= {"first_goal":"Flask_App", 
		"second_goal":"Tkinter_App", 
		"third_goal":"Personal_Website"}
		a= list(goals_dictionary.values())
		new_elements = []
		new_elements = '\n\n'.join(a)

		self.list_goals=Label(self.selection_frame,text=new_elements)
		self.list_goals.grid(column=1,row=9,padx=5)

	def save_frc_data(self):
		hip_left= self.hip_entry_left.get()
		hip_right=self.hip_entry_right.get()
		shoulder_left=self.shoulder_entry_left.get()
		shoulder_right=self.shoulder_entry_right.get()
		spine_top= self.spine_entry_top.get()
		spine_mid=self.spine_entry_mid.get()
		spine_low=self.spine_entry_lower.get()
		knee_left=self.knee_entry_left.get()
		knee_right=self.knee_entry_right.get()
		ankle_left=self.ankle_entry_left.get()
		ankle_right=self.ankle_entry_right.get()

		frc_dict= {}

		filename = "frc_mobility.csv"


		frc_dict["left_hip"]= hip_left
		frc_dict["right_hip"]= hip_right
		frc_dict["left_shoulder"]= shoulder_left
		frc_dict["right_shoulder"]= shoulder_right
		frc_dict["top_spine"]= spine_top
		frc_dict["mid_spine"]= spine_mid
		frc_dict["lumbar_spine"]= spine_low
		frc_dict["left_knee"]= knee_left 
		frc_dict["right_knee"]= knee_right
		frc_dict["left_ankle"]=ankle_left
		frc_dict["right_ankle"]=ankle_right
		
		fields = ["left_hip","right_hip","left_shoulder","right_shoulder","top_spine","mid_spine","lumbar_spine","left_knee","right_knee","left_ankle","right_ankle"]
		# writing to csv file 
		with open(filename, 'w') as csvfile: 
			# creating a csv dict writer object 
			writer = csv.DictWriter(csvfile, fieldnames = fields) 
			  
			# writing headers (field names) 
			writer.writeheader() 
			
			# writing data rows 
			writer.writerow(frc_dict)


	def FRC(self):
		# Just save all of this to a csv file 

		pass

			# I need to save all this data in a csv file 
			# and able to name it
			# that way I can keep track of it's progress over time 
			# need to learn how to read data from csv files

	def mobility(self):
		self.mobility_exercise=Label(self.selection_frame,text="A list of mobility exercise")
		self.mobility_exercise.grid(column=1,row=11,padx=5)

		self.window_mobility = Toplevel()
		self.window_mobility.geometry("1390x300")
		self.window_mobility.title("FRC Tracker")

		label_title = Label(self.window_mobility,text="FRC-Mobility", font=("Times New Roman", 22))
		label_title.grid(columnspan=7, row=0,)
		hip_label_left = Label(self.window_mobility,text="Left Hip")
		hip_label_left .grid(column=0, row=1)
		hip_label_right = Label(self.window_mobility,text="Right Hip")
		hip_label_right.grid(column=0, row=2)
		shoulder_label_left = Label(self.window_mobility,text="Left Shoulder")
		shoulder_label_left.grid(column=2, row=1)
		shoulder_label_right = Label(self.window_mobility,text="Right Shoulder")
		shoulder_label_right.grid(column=2, row=2)
		spine_label_top = Label(self.window_mobility,text="Cervical Spine")
		spine_label_top.grid(column=4, row=1)
		spine_label_mid = Label(self.window_mobility,text="Thoracic Spine")
		spine_label_mid.grid(column=4, row=2)
		spine_label_lower = Label(self.window_mobility,text="Lower Spine")
		spine_label_lower.grid(column=4, row=3)
		knee_label_left = Label(self.window_mobility,text="Left Knee")
		knee_label_left.grid(column=6, row=1)
		knee_label_right = Label(self.window_mobility,text="Right Knee")
		knee_label_right.grid(column=6, row=2)
		ankle_label_left = Label(self.window_mobility,text="Left Ankle")
		ankle_label_left.grid(column=8, row=1)
		ankle_label_right = Label(self.window_mobility,text="Right Ankle")
		ankle_label_right.grid(column=8, row=2)

		self.hip_entry_left = Entry(self.window_mobility)
		self.hip_entry_left.grid(column=1, row=1)
		self.hip_entry_right = Entry(self.window_mobility)
		self.hip_entry_right.grid(column=1, row=2)
		self.shoulder_entry_left = Entry(self.window_mobility)
		self.shoulder_entry_left.grid(column=3, row=1)
		self.shoulder_entry_right = Entry(self.window_mobility)
		self.shoulder_entry_right.grid(column=3, row=2)
		self.spine_entry_top = Entry(self.window_mobility)
		self.spine_entry_top.grid(column=5, row=1)
		self.spine_entry_mid = Entry(self.window_mobility)
		self.spine_entry_mid.grid(column=5, row=2)
		self.spine_entry_lower = Entry(self.window_mobility)
		self.spine_entry_lower.grid(column=5, row=3)
		self.knee_entry_left = Entry(self.window_mobility)
		self.knee_entry_left.grid(column=7, row=1)
		self.knee_entry_right = Entry(self.window_mobility)
		self.knee_entry_right.grid(column=7, row=2)
		self.ankle_entry_left = Entry(self.window_mobility)
		self.ankle_entry_left.grid(column=9, row=1)
		self.ankle_entry_right = Entry(self.window_mobility)
		self.ankle_entry_right.grid(column=9, row=2)

		save_button = Button(self.window_mobility,text="Save", command=self.save_frc_data)
		save_button.grid(column=0, row=3)

	def graph_run(self):

		y_distance = self.distance_entry_1.get()
		x_time = self.time_entry_1.get()

		float_time = float(x_time)
		float_distance = float(y_distance)
		# take running time and divide it by distance you ran, pace = time/distance
		pace_result = float_time/float_distance

		mydict = {'Day': "12",
		'Distance': 'hello',
		'Time': 'time',
		'Pace': 'float'}

		date_time = datetime.datetime.now()
		day = date_time.strftime("%A" + " %d")

		mydict["Day"]= day
		mydict["Distance"] = float_time
		mydict["Time"] = float_distance
		mydict["Pace"] = float(pace_result)
		fields = ['Day', 'Distance', 'Time', 'Pace']
		# name of csv file 
		filename = "running_records.csv"

		# writing to csv file 
		with open(filename, 'w') as csvfile: 
			# creating a csv dict writer object 
			writer = csv.DictWriter(csvfile, fieldnames = fields) 
			  
			# writing headers (field names) 
			writer.writeheader() 
			
			# writing data rows 
			writer.writerow(mydict) 

		plt.plot(float_distance, float_time, color="blue", marker="o", linestyle="--", label="Total Distance & Time" )
		plt.plot(float_time, pace_result, color='y', marker='o', linewidth= 3, label='Average Pace: ')
		plt.xlabel("Distance(meters)")
		plt.ylabel("Pace(min/meter)")
		plt.title("Distance over time covered by my walks/runs")
		plt.grid(True)
		plt.legend()
		plt.show()

	def running(self):
		self.running_label=Label(self.selection_frame,text="Running Tracker System with graphs")
		self.running_label.grid(column=1,row=12,padx=5)

		self.window_running = Toplevel()
		self.window_running.geometry("535x150")
		self.window_running.title("Running Tracker")

		running_title = Label(self.window_running,text="Running Tracker System", font=("Times New Roman", 22))
		running_title.grid(columnspan=7, row=0,)
		distance_label = Label(self.window_running,text="Distance(meters): ")
		distance_label.grid(column=0, row=1)
		# distance_label_2 = Label(self.window_running,text="Distance2: ")
		# distance_label_2.grid(column=2,row=1)
		time_label = Label(self.window_running,text="Time(minutes): ")
		time_label.grid(column=0, row=2)
		# time_label_2 = Label(self.window_running,text="Time2: ")
		# time_label_2.grid(column=2, row=2)
		# pace_label = Label(self.window_running,text="Pace: ")
		# pace_label.grid(column=0, row=3)

		self.distance_entry_1 = Entry(self.window_running)
		self.distance_entry_1.grid(column=1, row=1)
		# self.distance_entry_2 = Entry(self.window_running)
		# self.distance_entry_2.grid(column=3,row=1)
		self.time_entry_1 = Entry(self.window_running)
		self.time_entry_1.grid(column=1, row=2)
		# self.time_entry_2 = Entry(self.window_running)
		# self.time_entry_2.grid(column=3, row=2)
		# self.pace_entry = Entry(self.window_running)
		# self.pace_entry.grid(column=1, row=3)

		graph_button=Button(self.window_running,text='Draw Me', command=self.graph_run)
		graph_button.grid(column=1,row=4)


	def __init__(self,master):
		frame = Frame(master)
		frame.grid()
		self.file_path = ""
		self.activity_options =["Reading", "Programming", "Exercising"]
		self.motivation_options= ["Phrases", "Quotes", "Notes", "Sleep"]

		self.selection_frame= LabelFrame(root, text="Accountability System", height=200, width=200)
		self.selection_frame.grid(column= 0, row= 0, padx=10, pady=10)

		self.mood_label= Label(self.selection_frame, text="Mood: ")
		self.mood_label.grid(column=0, row=0, padx=5)
		
		self.well_button = Button(self.selection_frame, text="Well", command=self.activity_button_menu)
		self.well_button.grid(column= 1, row= 0, padx=5)
		
		self.tired_button = Button(self.selection_frame, text= "Tired", command=self.motivation_button)
		self.tired_button.grid(column=2,row=0,padx=5)

		l = tk.Label(self.selection_frame, bg='white', width=20, text='checklist')
		l.grid(column=3,row=0,padx=5)

		def print_selection():
			if (var1.get() == 1) & (var2.get() == 0) & (var3.get() == 0):
				l.config(text='I love Reading ')
			elif (var1.get() == 0) & (var2.get() == 1) & (var3.get() == 0):
				l.config(text='I love C++')
			elif (var1.get() == 0) & (var2.get() == 0) & (var3.get() == 1):
				l.config(text= 'I love Exercising')
			elif (var1.get() == 0) & (var2.get() == 0)& (var3.get() == 0) :
				l.config(text='I didnt do anything')
			else:
				l.config(text='I love both')
		
		var1 = IntVar()
		var2 = IntVar()
		var3 = IntVar()
		c1 = Checkbutton(self.selection_frame,text='Reading',variable=var1, onvalue=1, offvalue=0, command=print_selection)
		c1.grid(column=3, row=1,padx=5)
		c2 = Checkbutton(self.selection_frame, text='Programming',variable=var2, onvalue=1, offvalue=0, command=print_selection)
		c2.grid(column=3, row=2,padx=5)
		c3 = Checkbutton(self.selection_frame,text='Exercising', variable=var3, onvalue=1, offvalue=0, command=print_selection)
		c3.grid(column=3,row=3,padx=5)
		
		# add a date ; and a save button that will help you save; timer 
		# also will help you save the checklist
		# start working on developing a little graph
		# where time is the x-axis, and knoweledge is the y-axis
		# that way you can keep track of let's say you learned 3 new things today over 1 hr 
		# you add 3 new things on y-axis and over an hour
		# y =ax+b;
		# need to review that; that would result in a nice graph that you can see over the weekend



if __name__ =="__main__":
	root = Tk()
	root.title("Accountability System")
	Acc_Tool(root)
	root.mainloop()

