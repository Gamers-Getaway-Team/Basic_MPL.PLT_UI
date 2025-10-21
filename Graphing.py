import customtkinter as tk
import matplotlib.pyplot as plt
import numpy as np

settings = {
    'Title': '',
    'X-Label': '',
    'Y-Label': '',
    'Rows': 1,
    'Columns': 1,
    'Grid': True,
    'Legend': True,
}

class main (tk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('1000x800')
        self.title('GG Team ploting Utility')
        self.configure(fg_color='grey')
        
        self.control_Panel = tk.CTkFrame(self)
        self.new_Plot_Button = tk.CTkButton(self.control_Panel, text='Add plot', command=lambda: self.newPlot()).pack(side='left')
        self.control_Panel.pack(fill='x')
        
        self.plot_List_Panel = tk.CTkScrollableFrame(self, fg_color='black')
        self.plot_List_Panel.pack(expand=True, fill='both')
        self.plot_Array = []
        self.plot_Array.append(plot_Panel(self.plot_List_Panel))
        self.plot_Array[0].pack(anchor='n', expand=True, fill='x')
        
    def newPlot(self):
        self.plot_Array.append(plot_Panel(self.plot_List_Panel))
        self.plot_Array[len(self.plot_Array) - 1].pack(anchor='n', expand=True, fill='x', pady=2)
    
    def removePlot(self, plot_ID):
        self.plot_Array[plot_ID - 1].destroy()
        self.plot_Array.pop(plot_ID - 1)
        
            
class plot_Panel(tk.CTkFrame):
    _subplot_ID = 0
    _plot_ID = 0
    def __init__(self, master, subplot_Master='', plot_Panel_Title_Color='lightblue'):
        super().__init__(master)
        if subplot_Master != '':
            self.ID = len(subplot_Master.subplots) + 1
            self.subplot_Master = subplot_Master
            self.primary = 'SubPlot'
        else:
            plot_Panel._plot_ID += 1
            self.ID = plot_Panel._plot_ID
            self.primary = 'Plot'
        
        self.subplots = []
        self.settings = settings.copy()
        self.plot = plt
        
        self.top_Panel = tk.CTkFrame(self)
        self.show_Details_Button = tk.CTkButton(self.top_Panel, text='Collapse', command=lambda: self.showDetails())
        self.show_Details_Button.pack(side='left')
        self.plot_Panel_Title = tk.CTkLabel(self.top_Panel, text=f'{self.primary} {self.ID}', font=('Times New Roman', 14), fg_color=plot_Panel_Title_Color).pack(expand=True, side='left', fill='both')
        self.remove_plot_Button = tk.CTkButton(self.top_Panel, text='Remove', fg_color='red', hover_color='darkred', command=lambda: self.removeSelf()).pack(side='right')
        self.top_Panel.pack(expand=True, fill='x')
        
        self.bottom_Panel = tk.CTkFrame(self)
        self.options_Panel = tk.CTkFrame(self.bottom_Panel)
        self.title_Entry = tk.CTkEntry(self.options_Panel, placeholder_text='Title of Plot')
        self.title_Entry.bind('<KeyRelease>', lambda null: self.settings.update({'Title': self.title_Entry.get()}))
        self.title_Entry.pack()
        self.X_Name_Entry = tk.CTkEntry(self.options_Panel, placeholder_text='X-Axis Name')
        self.X_Name_Entry.bind('<KeyRelease>', lambda null: self.settings.update({'X-Label': self.X_Name_Entry.get()}))
        self.X_Name_Entry.pack()
        self.Y_Name_Entry = tk.CTkEntry(self.options_Panel, placeholder_text='Y-Axis Name')
        self.Y_Name_Entry.bind('<KeyRelease>', lambda null: self.settings.update({'Y-Label': self.Y_Name_Entry.get()}))
        self.Y_Name_Entry.pack()
        self.grid_Toggle = tk.CTkCheckBox(self.options_Panel, text='Grid')
        self.grid_Toggle.select()
        self.grid_Toggle.pack(fill='x', pady=1, padx=1)
        self.legend_Toggle = tk.CTkCheckBox(self.options_Panel, text='Legend')
        self.legend_Toggle.select()
        self.legend_Toggle.pack(fill='x', pady=1, padx=1)
        self.add_Line_Button = tk.CTkButton(self.options_Panel, text='Add Line', command=lambda: self.newLine()).pack(pady=2)
        if self.primary != 'SubPlot':
            self.rows_Entry = tk.CTkEntry(self.options_Panel, placeholder_text='# Rows')
            self.rows_Entry.bind('<KeyRelease>', lambda null: self.settings.update({'Rows': int(self.rows_Entry.get())}) if self.rows_Entry.get().isdigit() else 1)
            self.rows_Entry.pack()
            self.columns_Entry = tk.CTkEntry(self.options_Panel, placeholder_text='# Columns')
            self.columns_Entry.bind('<KeyRelease>', lambda null: self.settings.update({'Columns': int(self.columns_Entry.get())}) if int(self.columns_Entry.get()) else 1)
            self.columns_Entry.pack()
            self.add_SubPlot_button = tk.CTkButton(self.options_Panel, text='Add SubPlot', command=lambda: self.newSubplot()).pack(pady=2)
            self.plot_Button = tk.CTkButton(self.options_Panel, text='Plot', fg_color='green', hover_color='darkgreen', command=lambda:self.plotLines()).pack(pady=2)
            self.plot_All_Button = tk.CTkButton(self.options_Panel, text='Plot All Plots', fg_color='green', hover_color='darkgreen', state='disabled', command=lambda: self.plotAllPlots())
            self.plot_All_Button.pack(pady=2)
        self.options_Panel.pack(side='left', anchor='n', pady=5)
        
        self.lines_Panel = tk.CTkScrollableFrame(self.bottom_Panel, fg_color='grey', height=400)
        self.lines_Panel.pack(expand=True, fill='both')
        self.lines_Array = [line_Entry(self.lines_Panel, self)]
        self.lines_Array[0].pack(expand=True, fill='both', pady=5)
        
        self.subplots_Panel = tk.CTkScrollableFrame(self.bottom_Panel, fg_color='grey')
        self.bottom_Panel.pack(expand=True, side='bottom', fill='x')
        
    def showDetails(self):
        if not self.bottom_Panel.winfo_ismapped():
            self.bottom_Panel.pack(expand=True, fill='x')
            self.show_Details_Button.configure(text='Collapse')
        else:
            self.bottom_Panel.pack_forget()
            self.show_Details_Button.configure(text='Expand')
        
    def newLine(self):
        self.lines_Array.append(line_Entry(self.lines_Panel, self, len(self.lines_Array) + 1))
        self.lines_Array[len(self.lines_Array) - 1].pack(expand=True, fill='both', pady=5)
        
    def newSubplot(self):
        self.plot_All_Button.configure(state='normal')
        self.subplots.append(plot_Panel(self.subplots_Panel, self, plot_Panel_Title_Color='purple'))
        self.subplots[len(self.subplots) - 1].pack(expand=True, fill='x', padx=5)
        self.settings.update({'Columns': self.settings['Columns'] + 1})
        self.columns_Entry.delete(0, tk.END)
        self.columns_Entry.insert(0, str(self.settings['Columns']))
        if not self.subplots_Panel.winfo_ismapped():
            self.subplots_Panel.pack(expand=True, fill='x', anchor='s')
    
    def removeLine(self, line_ID):
        self.lines_Array[line_ID - 1].destroy()
        self.lines_Array.pop(line_ID - 1)
    
    def removeSubPlot(self, subplotID):
        self.subplots[subplotID - 1].destroy()
        self.subplots.pop(subplotID - 1)
        if self.settings['Columns'] > 1:
            self.settings.update({'Columns': self.settings['Columns'] - 1})
        self.columns_Entry.delete(0, tk.END)
        self.columns_Entry.insert(0, str(self.settings['Columns']))
        if len(self.subplots) == 0:
            self.subplots_Panel.pack_forget()
            self.plot_All_Button.configure(state='disabled')
    
    def plotLines(self, withSubPlots=False):
        self.plot.clf()
        self.plot.subplot(self.settings['Rows'], self.settings['Columns'], 1)
        self.plot.title(self.settings['Title'])
        self.plot.xlabel(self.settings['X-Label'])
        self.plot.ylabel(self.settings['Y-Label'])
        self.plot.grid(visible=self.settings['Grid'])
        for line in self.lines_Array:
            if line.is_Ready:
                self.plot.plot(line.X_Values, line.Y_Values, label=line.line_Settings['Name'], color=line.line_Settings['Color'], marker=line.line_Settings['Marker'], linestyle=line.line_Settings['Type'])
        if self.settings['Legend'] == True:
            self.plot.legend()
        if not withSubPlots:
            self.plot.show()
        
    def plotAllPlots(self):
        self.plot.clf()
        self.plotLines(True)
        for subplot in self.subplots:
            self.plot.subplot(self.settings['Rows'], self.settings['Columns'], subplot.ID + 1)
            self.plot.title(subplot.settings['Title'])
            self.plot.xlabel(subplot.settings['X-Label'])
            self.plot.ylabel(subplot.settings['Y-Label'])
            self.plot.grid(visible=subplot.settings['Grid'])
            for line in subplot.lines_Array:
                if line.is_Ready:
                    self.plot.plot(line.X_Values, line.Y_Values, label=line.line_Settings['Name'], color=line.line_Settings['Color'], marker=line.line_Settings['Marker'], linestyle=line.line_Settings['Type'])
            if self.settings['Legend'] == True:
                self.plot.legend()
            self.plot.show()
             
    def removeSelf(self):
        if self.primary != 'SubPlot':
            app.removePlot(self.ID)
        else:
            self.subplot_Master.removeSubPlot(self.ID)

class line_Entry(tk.CTkFrame):
    def __init__(self, master, parent, _line_ID=1):
        super().__init__(master)
        self.ID = _line_ID
        
        self.is_Ready = False
        self.X_Values = []
        self.Y_Values = []
        self.line_Settings = {
            'Name': f'line {self.ID}',
            'Color': 'b',
            'Type': '-',
            'Marker': '.'
        }
        
        self.top_Panel = tk.CTkFrame(self)
        self.show_Details_Button = tk.CTkButton(self.top_Panel, text='Collapse', command=lambda: self.showDetails())
        self.show_Details_Button.pack(side='left')
        self.line_Label = tk.CTkLabel(self.top_Panel, text=f'--- Line {self.ID} {parent.primary} {parent.ID} ---', fg_color='lightgreen')
        self.line_Label.pack(expand=True, side='left', fill='x')
        self.remove_Line_Button = tk.CTkButton(self.top_Panel, text='Remove', fg_color='red', hover_color='darkred', command=lambda: parent.removeLine(self.ID)).pack(side='right')
        self.top_Panel.pack(expand=True, fill='x')
        
        self.bottom_Panel = tk.CTkFrame(self)
        self.options_Panel = tk.CTkFrame(self.bottom_Panel)
        self.line_Name_Entry = tk.CTkEntry(self.options_Panel, placeholder_text='Line Name *Optional')
        self.line_Name_Entry.bind('<KeyRelease>', lambda null: self.line_Settings.update({'Name': self.line_Name_Entry.get()}))
        self.line_Name_Entry.grid()
        self.plot_Line_Button = tk.CTkButton(self.options_Panel, text='plot Line', command=lambda: parent.plotLine())
        self.plot_Line_Button.grid(column=0, row=1)
        self.line_Color_Label = tk.CTkLabel(self.options_Panel, text='Line Color: ').grid(column=1, row=0)
        self.line_Color = tk.CTkOptionMenu(self.options_Panel, values=['Blue', 'Red', 'Green', 'Yellow'], command=lambda null: self.updateLineSettings())
        self.line_Color.grid(column=2, row=0)
        self.line_Type_Label = tk.CTkLabel(self.options_Panel, text='Line Type: ', anchor='e').grid(column=1, row=1)
        self.line_Type = tk.CTkOptionMenu(self.options_Panel, values=['Solid', 'Dotted'], command=lambda null: self.updateLineSettings())
        self.line_Type.grid(column=2, row=1)
        self.maker_Type_Label = tk.CTkLabel(self.options_Panel, text='Marker Type: ', anchor='e').grid(column=3, row=0)
        self.marker_Type = tk.CTkOptionMenu(self.options_Panel, values=['Point', 'Circle'], command=lambda null: self.updateLineSettings())
        self.marker_Type.grid(column=4, row=0)
        self.status_Label = tk.CTkLabel(self.options_Panel, text='Ready: ').grid(column=3, row=1, sticky='e')
        self.status_Bool_Label = tk.CTkLabel(self.options_Panel, text=f'{self.is_Ready}', text_color='red')
        self.status_Bool_Label.grid(column=4, row=1, sticky='w')
        self.options_Panel.pack(fill='x', pady=1)
        self.bottom_Panel.pack(expand=True, fill='x')
        
        self.X_Axis_Frame = tk.CTkFrame(self.bottom_Panel)
        self.X_Values_Label = tk.CTkLabel(self.X_Axis_Frame, text='No X Values Entered', anchor='w')
        self.X_Values_Label.pack(fill='x')
        self.X_Values_Entry = tk.CTkEntry(self.X_Axis_Frame, placeholder_text='X Values I.e. 1,2,3')
        self.X_Values_Entry.bind('<KeyRelease>', lambda null: self.correctAndCheck(self.X_Values_Entry.get(), 'x'))
        self.X_Values_Entry.pack(fill='x')
        self.X_Axis_Frame.pack(fill='x')
        
        self.Y_Axis_Frame = tk.CTkFrame(self.bottom_Panel)
        self.Y_Values_Label = tk.CTkLabel(self.Y_Axis_Frame, text='No Y Values Entered', anchor='w')
        self.Y_Values_Label.pack(fill='x')
        self.Y_Values_Entry = tk.CTkEntry(self.Y_Axis_Frame, placeholder_text='Y Values I.e. 1,2,3')
        self.Y_Values_Entry.bind('<KeyRelease>', lambda null: self.correctAndCheck(self.Y_Values_Entry.get(), 'y'))
        self.Y_Values_Entry.pack(fill='x')
        self.Y_Axis_Frame.pack(fill='x')
        
        self.bottom_Panel.pack(expand=True, fill='x')
        
    def showDetails(self):
        if not self.bottom_Panel.winfo_ismapped():
            self.bottom_Panel.pack(expand=True, fill='x')
            self.show_Details_Button.configure(text='Collapse')
        else:
            self.bottom_Panel.pack_forget()
            self.show_Details_Button.configure(text='Expand')
        
    def updateLineSettings(self):
        self.line_Settings.update({'Color': self.line_Color.get().lower(), 'Type': self.line_Type.get().lower()})
        match self.line_Color.get():
            case 'Blue':
                self.line_Settings.update({'Color': 'b'})
            case 'Red':
                self.line_Settings.update({'Color': 'r'})
            case 'Green':
                self.line_Settings.update({'Color': 'g'})
            case 'Yellow':
                self.line_Settings.update({'Color': 'y'})
                
        match self.marker_Type.get():
            case 'Point':
                self.line_Settings.update({'Marker': '.'})
            case 'Circle':
                self.line_Settings.update({'Marker': 'o'})
        
    def correctAndCheck(self, values, axis):
        if values == '':
            total = 0
        raw = values
        raw = raw.strip(' ')
        raw_Split = raw.split(',')
        corrected = []
        for check in raw_Split:
            try:
                corrected.append(float(check))
                total = len(corrected)
            except:
                return
        match axis:
            case 'x':
                self.X_Values_Label.configure(text=f'X Values Loaded: {total}')
                self.X_Values=corrected
            case 'y':
                self.Y_Values_Label.configure(text=f'Y Values Loaded: {total}')
                self.Y_Values=corrected
        self.readyToplot()
        
    def readyToplot(self):
        if len(self.X_Values) != 0 and len(self.Y_Values) != 0 and len(self.X_Values) == len(self.Y_Values):
            self.is_Ready = True
            self.status_Bool_Label.configure(text=f'{self.is_Ready}', text_color='green')
        else:
            self.is_Ready = False
            self.status_Bool_Label.configure(text=f'{self.is_Ready}', text_color='red')

app = main()

app.mainloop()
