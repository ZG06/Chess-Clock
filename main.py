from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivy.clock import Clock

# Setting the default app window size to 700x300 dp
Window.size = (dp(700), dp(300))


class ChessclockApp(MDApp): 
   dialog = None # Dialog state
   disabled1_now = None # State of first timer
   disabled2_now = None # State of second timer
   counter1 = 0 # Counts how many timer timer1 function has been called
   counter2 = 0 # Counts how many timer timer2 function has been called
   timer1_init_time = '' # Timer1 time after selecting a mode
   timer2_init_time = '' # Timer2 time after selecting a mode
   timer1_time = 0 # Time of timer1
   timer2_time = 0 # Time of timer2
   mode = '' # Timers' mode

   def on_start(self):
      # Disable the pause button before starting the timers
      self.root.ids.pause.disabled = True

   def build(self):
      self.theme_cls.theme_style = 'Dark' # Default theme style
      self.theme_cls.primary_palette = 'BlueGray' # Default primary palette
      self.timer1_init_time = '5:00' # Setting the initial timer1 time after starting the app
      self.timer2_init_time = '5:00' # Setting the initial timer1 time after starting the app
      return Builder.load_file('chessclock.kv')

   def timer1_pressed(self):
      # Starting timer1
      self.timer1()
      # Disabling first timer and enabling second one
      self.root.ids.timer1.disabled = True
      self.root.ids.timer2.disabled = False

      if self.root.ids.pause.disabled == True:
         # Enabling the pause button when timer1 is started
         self.root.ids.pause.disabled = False

      Clock.unschedule(self.update_timer2)

   def timer2_pressed(self):
      # Starting timer2
      self.timer2()
      # Disabling second timer and enabling first one
      self.root.ids.timer2.disabled = True
      self.root.ids.timer1.disabled = False

      if self.root.ids.pause.disabled == True:
         # Enabling the pause button when timer1 is started
         self.root.ids.pause.disabled = False

      Clock.unschedule(self.update_timer1)

   def reset(self):
      # Enabling the timers
      self.root.ids.timer1.disabled = False
      self.root.ids.timer2.disabled = False

      # Pausing the timers
      Clock.unschedule(self.update_timer1)
      Clock.unschedule(self.update_timer2)

      # Reseting values of the timers
      self.root.ids.timer1.text = self.timer1_init_time
      self.root.ids.timer2.text = self.timer2_init_time

      # Disabling the pause button after timers' reset
      self.root.ids.pause.icon = 'pause'
      self.root.ids.pause.disabled = True
      self.timer1_time = self.timer1_init_time
      self.timer2_time = self.timer2_init_time

      self.counter1 = 0
      self.counter2 = 0

   def pause(self):
      timer1 = self.root.ids.timer1
      timer2 = self.root.ids.timer2
      self.disabled1_now = self.root.ids.timer1.disabled # State of first timer before pausing
      self.disabled2_now = self.root.ids.timer2.disabled # State of second timer before pausing

      # Pausing the timers
      self.root.ids.timer1.disabled = True
      self.root.ids.timer2.disabled = True
      Clock.unschedule(self.update_timer1)
      Clock.unschedule(self.update_timer2)
      
      # Changing "pause" icon of the pause button to "play" icon
      self.root.ids.pause.icon = 'play'

   def resume(self):
      self.root.ids.timer1.disabled = self.disabled1_now # State of first timer before pausing
      self.root.ids.timer2.disabled = self.disabled2_now # State of first timer after pausing

      if self.root.ids.timer1.disabled == True:
         # Starting first timer after resuming
         self.timer1()

      if self.root.ids.timer2.disabled == True:
         # Starting second timer after resuming
         self.timer2()

      # Changing the icon to 'pause' when resuming
      self.root.ids.pause.icon = 'pause'

   def stop_timers(self):
      # Stopping the timers
      Clock.unschedule(self.update_timer1)
      Clock.unschedule(self.update_timer2)
      # Pausing the timers
      self.pause()
      # Disabling the pause button after stopping the timers
      self.root.ids.pause.disabled = True

   def settings(self):
      if self.root.ids.timer1.disabled == False and self.root.ids.timer2.disabled == False:
         pass
      else:
         self.pause()
      # Creating dialog with different clock modes
      if not self.dialog:
         self.dialog = MDDialog(
            md_bg_color = '#363333',
            radius = [7, 20, 7, 20],
            title = 'Modes',
            type = 'custom',
            content_cls = MDGridLayout(
               MDRaisedButton( # 1 minute game
                  text = '1 min',
                  elevation = 3,
                  md_bg_color = '#007d57',
                  on_release = self.mode_setting
               ),

               MDRaisedButton( # 3 minute game
                  text = '3 min',
                  elevation = 3,
                  md_bg_color = '#007d57',
                  on_release = self.mode_setting
               ),

               MDRaisedButton( # 5 minute game
                  text = '5 min',
                  elevation = 3,
                  md_bg_color = '#007d57',
                  on_release = self.mode_setting
               ),

               MDRaisedButton( # 10 minute game
                  text = '10 min',
                  elevation = 3,
                  md_bg_color = '#007d57',
                  on_press = self.mode_setting
               ),

               spacing = '66dp',
               padding = '20dp',
               size_hint_y = None,
               height = "80dp",
               cols = 4,
               rows = 2,
            ),
            buttons = [
               MDFlatButton(
                  text = 'Close', on_release = self.dialog_cls, # Dialog close button
                  font_size = 16,
                  font_name = 'fonts/OpenSans-SemiBold.ttf'
               ),
            ],
            
         )
      # Opening the dialog
      self.dialog.open()

   def dialog_cls(self, obj):
      # Closing the dialog
      self.dialog.dismiss()

   def mode_setting(self, obj):
      # Reseting both timers after the mode has been picked
      self.reset()
      # Closing the dialog
      self.dialog.dismiss()
      # Setting a picked mode
      self.mode = f'{obj.text.replace("min", "").strip()}:00'
      self.root.ids.timer1.text = self.mode
      self.root.ids.timer2.text = self.mode
      
      # Setting initial time after picking a mode
      self.timer1_init_time = self.root.ids.timer1.text
      self.timer2_init_time = self.root.ids.timer2.text

      # Disabling the pause button after timers' reset
      self.root.ids.pause.disabled = True
      # Changing the icon to 'pause' after timers' reset
      self.root.ids.pause.icon = 'pause'

   def timer1(self):
      # Assigning the value of timer1 text variable to timer1_time if it hasn't been called yet
      if self.counter1 == 0:
         self.timer1_time = self.root.ids.timer1.text
         self.counter1 += 1
      # Starting timer1
      Clock.schedule_interval(self.update_timer1, .1)

   def timer2(self):
      # Assigning the value of timer2 text variable to timer2_time if it hasn't been called yet
      if self.counter2 == 0:
         self.timer2_time = self.root.ids.timer2.text
         self.counter2 += 1
      # Starting timer2
      Clock.schedule_interval(self.update_timer2, .1)

   def update_timer1(self, *args):
      minutes_before = f'{self.timer1_time.split(":")[0]}' # minutes on timer1 before operating with them
      seconds_before = f'{self.timer1_time.split(":")[1]}' # seconds on timer1 before operating with them

      if minutes_before == '0' and seconds_before[:4] == '00.1':
         # Stops the timer if first one reaches 0:00
         self.stop_timers()
      if seconds_before[:4] == '00.1' or seconds_before == '00':
         # Setting seconds to 59 if they reach 0
         self.timer1_time = f'{int(minutes_before)-1}:{59.9}'
         return 0
      if float(seconds_before[:4]) > 10.0:
         # Operating with seconds if they are bigger than 10
         self.timer1_time = f'{minutes_before}:{float(seconds_before)-0.1}'
      if float(seconds_before[:4]) <= 10.0 and float(seconds_before) > 0:
         # Adding zero before seconds if they are less than 10
         self.timer1_time = f'{minutes_before}:0{float(seconds_before)-0.1}'

      minutes = f'{self.timer1_time.split(":")[0]}' # Minutes on timer2 after operating with them
      seconds = f'{self.timer1_time.split(":")[1][:2]}' # Seconds on timer2 after operating with them

      # Changing the timer2 label after operating with the time
      self.root.ids.timer1.text = f'{minutes}:{seconds}' 

   def update_timer2(self, *args):
      minutes_before = f'{self.timer2_time.split(":")[0]}' # minutes on timer2 before operating with them
      seconds_before = f'{self.timer2_time.split(":")[1]}' # seconds on timer2 before operating with them

      if minutes_before == '0' and seconds_before[:4] == '00.1':
         # Stops the timer if second one reaches 0:00
         self.stop_timers()
      if seconds_before[:4] == '00.1' or seconds_before == '00':
         # Setting seconds to 59 if they reach 0
         self.timer2_time = f'{int(minutes_before)-1}:{59.9}'
         return 0
      if float(seconds_before[:4]) > 10.0:
         # Operating with seconds if they are bigger than 10
         self.timer2_time = f'{minutes_before}:{float(seconds_before)-0.1}'
      if float(seconds_before[:4]) <= 10.0 and float(seconds_before) > 0:
         # Adding zero before seconds if they are less than 10
         self.timer2_time = f'{minutes_before}:0{float(seconds_before)-0.1}'

      minutes = f'{self.timer2_time.split(":")[0]}' # Minutes on timer2 after operating with them
      seconds = f'{self.timer2_time.split(":")[1][:2]}' # Seconds on timer2 after operating with them

      # Changing the timer2 label after operating with the time
      self.root.ids.timer2.text = f'{minutes}:{seconds}'


if __name__ == '__main__':
   ChessclockApp().run()
