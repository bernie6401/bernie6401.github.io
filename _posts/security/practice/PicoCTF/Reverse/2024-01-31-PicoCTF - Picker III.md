---
title: PicoCTF - Picker III
tags: [PicoCTF, CTF, Reverse]

category: "Security > Practice > PicoCTF > Reverse"
---

# PicoCTF - Picker III
## Source code
:::spoiler Source Code
```python!

import re



USER_ALIVE = True
FUNC_TABLE_SIZE = 4
FUNC_TABLE_ENTRY_SIZE = 32
CORRUPT_MESSAGE = 'Table corrupted. Try entering \'reset\' to fix it'

func_table = ''

def reset_table():
  global func_table

  # This table is formatted for easier viewing, but it is really one line
  func_table = \
'''\
print_table                     \
read_variable                   \
write_variable                  \
getRandomNumber                 \
'''

def check_table():
  global func_table

  if( len(func_table) != FUNC_TABLE_ENTRY_SIZE * FUNC_TABLE_SIZE):
    return False

  return True


def get_func(n):
  global func_table

  # Check table for viability
  if( not check_table() ):
    print(CORRUPT_MESSAGE)
    return

  # Get function name from table
  func_name = ''
  func_name_offset = n * FUNC_TABLE_ENTRY_SIZE
  for i in range(func_name_offset, func_name_offset+FUNC_TABLE_ENTRY_SIZE):
    if( func_table[i] == ' '):
      func_name = func_table[func_name_offset:i]
      break

  if( func_name == '' ):
    func_name = func_table[func_name_offset:func_name_offset+FUNC_TABLE_ENTRY_SIZE]
  
  return func_name


def print_table():
  # Check table for viability
  if( not check_table() ):
    print(CORRUPT_MESSAGE)
    return

  for i in range(0, FUNC_TABLE_SIZE):
    j = i + 1
    print(str(j)+': ' + get_func(i))


def filter_var_name(var_name):
  r = re.search('^[a-zA-Z_][a-zA-Z_0-9]*$', var_name)
  if r:
    return True
  else:
    return False


def read_variable():
  var_name = input('Please enter variable name to read: ')
  if( filter_var_name(var_name) ):
    eval('print('+var_name+')')
  else:
    print('Illegal variable name')


def filter_value(value):
  if ';' in value or '(' in value or ')' in value:
    return False
  else:
    return True


def write_variable():
  var_name = input('Please enter variable name to write: ')
  if( filter_var_name(var_name) ):
    value = input('Please enter new value of variable: ')
    if( filter_value(value) ):
      exec('global '+var_name+'; '+var_name+' = '+value)
    else:
      print('Illegal value')
  else:
    print('Illegal variable name')


def call_func(n):
  """
  Calls the nth function in the function table.
  Arguments:
    n: The function to call. The first function is 0.
  """

  # Check table for viability
  if( not check_table() ):
    print(CORRUPT_MESSAGE)
    return

  # Check n
  if( n < 0 ):
    print('n cannot be less than 0. Aborting...')
    return
  elif( n >= FUNC_TABLE_SIZE ):
    print('n cannot be greater than or equal to the function table size of '+FUNC_TABLE_SIZE)
    return

  # Get function name from table
  func_name = get_func(n)

  # Run the function
  eval(func_name+'()')


def dummy_func1():
  print('in dummy_func1')

def dummy_func2():
  print('in dummy_func2')

def dummy_func3():
  print('in dummy_func3')

def dummy_func4():
  print('in dummy_func4')

def getRandomNumber():
  print(4)  # Chosen by fair die roll.
            # Guaranteed to be random.
            # (See XKCD)

def win():
  # This line will not work locally unless you create your own 'flag.txt' in
  #   the same directory as this script
  flag = open('flag.txt', 'r').read()
  #flag = flag[:-1]
  flag = flag.strip()
  str_flag = ''
  for c in flag:
    str_flag += str(hex(ord(c))) + ' '
  print(str_flag)

def help_text():
  print(
  '''
This program fixes vulnerabilities in its predecessor by limiting what
functions can be called to a table of predefined functions. This still puts
the user in charge, but prevents them from calling undesirable subroutines.

* Enter 'quit' to quit the program.
* Enter 'help' for this text.
* Enter 'reset' to reset the table.
* Enter '1' to execute the first function in the table.
* Enter '2' to execute the second function in the table.
* Enter '3' to execute the third function in the table.
* Enter '4' to execute the fourth function in the table.

Here's the current table:
  '''
  )
  print_table()



reset_table()

while(USER_ALIVE):
  choice = input('==> ')
  if( choice == 'quit' or choice == 'exit' or choice == 'q' ):
    USER_ALIVE = False
  elif( choice == 'help' or choice == '?' ):
    help_text()
  elif( choice == 'reset' ):
    reset_table()
  elif( choice == '1' ):
    call_func(0)
  elif( choice == '2' ):
    call_func(1)
  elif( choice == '3' ):
    call_func(2)
  elif( choice == '4' ):
    call_func(3)
  else:
    print('Did not understand "'+choice+'" Have you tried "help"?')

```
:::
## Recon
這一題算有趣，但想了超久就放棄直接看[^pico-reverse-picker-iii-wp]，我原本還想說要怎麼用function pointer之類的東西，看來還是想的太複雜了，既然write_variable function可以新增一個全域變數，就代表我們可以直接覆蓋掉getRandomNumber這個string，變成win function，所以當我們直接call getRandomNumber function的時候其實是在call getRandomNumber這個global variable，此時就會直接call win()，我覺得有一點點通靈的性質，實在想不出來
## Exploit
```bash!
$ nc saturn.picoctf.net 62200
==> 3
Please enter variable name to write: getRandomNumber
Please enter new value of variable: win
==> 4
0x70 0x69 0x63 0x6f 0x43 0x54 0x46 0x7b 0x37 0x68 0x31 0x35 0x5f 0x31 0x35 0x5f 0x77 0x68 0x34 0x37 0x5f 0x77 0x33 0x5f 0x67 0x33 0x37 0x5f 0x77 0x31 0x37 0x68 0x5f 0x75 0x35 0x33 0x72 0x35 0x5f 0x31 0x6e 0x5f 0x63 0x68 0x34 0x72 0x67 0x33 0x5f 0x63 0x32 0x30 0x66 0x35 0x32 0x32 0x32 0x7d
```

Flag: `picoCTF{7h15_15_wh47_w3_g37_w17h_u53r5_1n_ch4rg3_c20f5222}`
## Reference
[^pico-reverse-picker-iii-wp]:[picker III WP - akshayrkapadia](https://gitlab.com/akshayrkapadia/CTF/-/blob/main/PicoCTF/ReverseEngineering/Picker-III/Picker-III.txt)