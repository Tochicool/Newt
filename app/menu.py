import random, math, pygame

def Goodbye():
  print('Thank you for using Newton\'s Laboratory.')
  print('Please send us any feedback at tochicool@gmail.com')
  waitFor = input()
  quit()

def MainMenu():
  print('NEWTON\'S LABORATORY')
  print('   1) Motion')
  print('   2) Forces')
  print('   3) Energy')
  print('   4) Materials')
  print('   5) Newton\'s Laws')
  print('   6) Free simulation')
  print('   7) Exit')

  while True:
    menuItem = int( input( 'Please enter the number of the of the item you are visiting' ) )

    if menuItem == 7:
      Goodbye()
    elif menuItem == 6:
      __import__('FreeSim')
    else:
      print('WORK IN PROGESS.')
      print('Please check back later.')


                   
MainMenu()

